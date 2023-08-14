# pylint: disable=[W,R,C,import-error, assignment-from-no-return, assignment-from-none]

try:
    from .LoaderFunction import LoaderFunction
    from .Functions import *
    from .ply.ply import lex
    from .ply.ply import yacc
    from .Identifier import Identifier
except ImportError:
    from LoaderFunction import LoaderFunction
    from Functions import *
    from ply.ply import lex
    from ply.ply import yacc
    from Identifier import Identifier
import re, json, glob

example_script = """
// example script: (based on combat.json)

// this is a comment

[engine:list/for_each] (<.enemies>)
{
    [engine:text/match] ([engine:text/replace_pattern] (" +", " ", [engine:text/set_case] (<#text>, "lower")), "search")
    @pattern: [engine:text/set_case] (<element.name>, "lower")
    #{
        [engine:player/attack_enemy](<#player>, <element>)
        break
    }
}

"""
def flatten_list(ls):
    out = []
    for l in ls:
        if isinstance(l, list):
            out += flatten_list(l)
        else:
            out.append(l)
    return out

tokens = (
    "FUNCTION", "VARIABLE", "NUMBER", "STRING", "BOOLEAN",
    "TAG", "WORD", "RETURN", "BREAK", "CONTINUE", "MIN", "MAX"
)

literals = ["=", "-", "+", "*", "/", "(", ")", "[", "]", "{", "}", ",", "#"]

t_ignore = " \t;~`\n"

t_ignore_comment = r"\/\/.*"

t_FUNCTION = r"\[[^\]]+\]"
t_VARIABLE = r"\<[^>]+\>"

t_BOOLEAN = r"(true|false)"
t_TAG = r"@[^\:]+\:"

def t_STRING(t):
    r"(\"[^\"]*\"|'[^']*')"
    t.value = t.value[1:-1]
    return t

def t_WORD(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    if t.value == "return":
        t.type = "RETURN"
    elif t.value == "break":
        t.type = "BREAK"
    elif t.value == "continue":
        t.type = "CONTINUE"
    elif t.value == "min":
        t.type = "MIN"
    elif t.value == "max":
        t.type = "MAX"
    return t

def t_NUMBER(t):
    r"(\d+(\.\d+)?|\.\d+)"
    t.value = float(t.value)
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)

start="expressions"


def p_statement_assign(p):
    'statement : VARIABLE "=" expression'
    p[0] = {"#store": {p[1][1:-1]: p[3]}}
    #names[p[1]] = p[3]

def p_function_call(p):
    '''function_call : FUNCTION parameters scope
                     | FUNCTION parameters tag_list
                     | FUNCTION parameters
                     | FUNCTION'''
    func: LoaderFunction = LoaderFunction.getFunction(Identifier.fromString(p[1][1:-1]))

    if func is None:
        raise Exception(f"function '{p[1][1:-1]}' is not defined")

    f_required = func.script_flags.get("required_args", 0)
    f_optional = func.script_flags.get("optional_args", 0)
    f_args = func.script_flags.get("args", {})
    if len(p) >= 3:
        params = p[2]["parameters"]
    else:
        params = []

    # if (f_required > 0) and len(params) < f_required:
    #     if f_optional == 0:
    #         raise Exception(f"too few parameters passed to function '{func.id.full()}', expected {f_required} but received only {len(params)}")
    #     else:
    #         raise Exception(f"too few parameters passed to function '{func.id.full()}', expected at least {f_required} but received only {len(params)}")

    parameters = {
        "args": {},
        "*args": {},
        "kwargs": {},
        "**kwargs": {},
        "scope": {},
        "tags": {}
    }

    args_name = None
    kwargs_name = None
    scope_name = None

    for arg_name, condition in f_args.items():
        match condition:
            case "required parameter":
                parameters["args"].update({arg_name: ...})
            case "*parameters":
                parameters["*args"].update({arg_name: []})
                args_name = arg_name
            case "optional parameter":
                parameters["kwargs"].update({arg_name: ...})
            case "**parameters":
                parameters["**kwargs"].update({arg_name: {}})
                kwargs_name = arg_name
            case "scope":
                parameters["scope"].update({arg_name: ...})
                scope_name = arg_name
            case "tags":
                tags = func.script_flags.get("tags")
                parameters["tags"].update({
                    arg_name: {
                        "tag": tags["tag"],
                        tags["scope"]: []
                    }
                })

    state = "args"

    for name, value in params:
        if state == "args":
            if name:
                state = "kwargs"
                if name in parameters["args"]: parameters["args"][name] = value
                elif name in parameters["*args"]: raise Exception(f"Cannot assign to starred parameter by identifer")
                else:
                    if any(v is ... for v in parameters["args"].values()): raise Exception(f"not enough args passed to function '{func.id.full()}'")
                    else:
                        if name in parameters["kwargs"]: parameters["kwargs"][name] = value
                        else:
                            state = "**kwargs"
                            if kwargs_name: parameters["**kwargs"][kwargs_name].update({name: value})
                            else: raise Exception(f"function '{func.id.full()}' does not accept **kwargs")
            else:
                found = False
                for n, v in parameters["args"].items():
                    if v == ...:
                        parameters["args"][n] = value
                        found = True
                        break

                if not found:
                    state = "*args"
                    if args_name: parameters["*args"][args_name].append(value)
                    else:
                        state = "kwargs"
                        for n, v in parameters["kwargs"].items():
                            if v is ...:
                                parameters["kwargs"][n] = value
                                found = True
                                break
                            
                if not found: raise Exception(f"too many args passed to function '{func.id.full()}'")
                # if name in parameters["args"]: parameters["args"][name] = value
                # else:
                #     state = "*args"
                #     if args_name: parameters["*args"][args_name].append(value)
                #     else:
                #         state = "kwargs"
                #         for n, v in parameters["kwargs"].items():
                #             if v is ...:
                #                 parameters["kwargs"][n] = value
                #                 break
                #         else: raise Exception(f"too many args passed to function '{func.id.full()}'")
        elif state == "*args":
            if name:
                state = "kwargs"
                if name in parameters["args"]: parameters["args"][name] = value
                elif name in parameters["*args"]: raise Exception(f"Cannot assign to starred parameter by identifer")
                else:
                    if any(v is ... for v in parameters["args"].values()): raise Exception(f"not enough args passed to function '{func.id.full()}'")
                    else:
                        if name in parameters["kwargs"]: parameters["kwargs"][name] = value
                        else:
                            state = "**kwargs"
                            if kwargs_name: parameters["**kwargs"][kwargs_name].update({name: value})
                            else: raise Exception(f"function '{func.id.full()}' does not accept **kwargs")
            else:
                if args_name: parameters["*args"][args_name].append(value)
                else:
                    state = "kwargs"
                    for n, v in parameters["kwargs"].items():
                        if v is ...:
                            parameters["kwargs"][n] = value
                            break
                    else: raise Exception(f"too many args passed to function '{func.id.full()}'")
        elif state == "kwargs":
            if name:
                state = "kwargs"
                if name in parameters["args"]: parameters["args"][name] = value
                elif name in parameters["*args"]: raise Exception(f"Cannot assign to starred parameter by identifer")
                else:
                    if any(v is ... for v in parameters["args"].values()): raise Exception(f"not enough args passed to function '{func.id.full()}'")
                    else:
                        if name in parameters["kwargs"]: parameters["kwargs"][name] = value
                        else:
                            state = "**kwargs"
                            if kwargs_name: parameters["**kwargs"][kwargs_name].update({name: value})
                            else: raise Exception(f"function '{func.id.full()}' does not accept **kwargs")
            else: raise Exception(f"cannot put positional arg after key word arg")
        else: # if state == "**kwargs":
            if name:
                if kwargs_name: parameters["**kwargs"][kwargs_name].update({name: value})
                else: raise Exception(f"function '{func.id.full()}' does not accept **kwargs")
            else: raise Exception(f"cannot put positional arg after key word arg")
    

    data = {
        "function": func.id.full()
    }
    if len(p) == 4:
        d = p[3]
        if isinstance(d, dict): # scope
            parameters["scope"] = d["scope"]
        else: # tags
            tag_list = d
            #parameters["tags"] = tag_list
            tags = parameters.get("tags")
            for v, d in tags.items():
                data_ = {v: []}

                for tag in tag_list:
                    keys = list(tag.keys())
                    if keys[0] == d["tag"]:
                        data_[v].append({
                            d["tag"]: tag[d["tag"]],
                            list(d.keys())[1]: tag["scope"]["functions"]
                        })
    
                data.update(data_)

    for n, v in parameters["args"].items():
        data.update({n: v})
    for n, vs in parameters["*args"].items():
        data.update({n: vs})
    for n, v in parameters["kwargs"].items():
        if v is not ...:
            data.update({n: v})
    for n, vs in parameters["**kwargs"].items():
        data.update({n: vs})
    for n, s in parameters["scope"].items():
        data.update({scope_name: {n: s}})

    p[0] = data

def p_tag(p):
    '''tag : TAG expression'''
    d = p[2]
    p[0] = {
        p[1][1:-1]: p[2]
    }

def p_tag_list(p):
    '''tag_list : tag '#' scope tag_list
                | tag '#' scope'''
    if len(p) == 5:
        d = p[1]
        d.update(p[3])
        p[0] = flatten_list([
            d,
            p[4]
        ])
    else:
        d = p[1]
        d.update(p[3])
        p[0] = [d]

def p_scope(p):
    "scope : '{' expressions '}'"
    p[0] = {"scope": p[2]}

def p_statements(p):
    """expressions : statement expressions
                   | statement"""
    if len(p) == 3:
        p[0] = {
            "functions": [p[1]] + p[2]["functions"]
        }
    else:
        p[0] = {
            "functions": [p[1]]
        }

def p_parameters(p):
    """parameters : '(' param_element ')'
                  | '(' ')'"""
    if len(p) == 4:
        p[0] = {"parameters": p[2]}
    else:
        p[0] = {"parameters": []}

def p_param_element2(p):
    """param_element_pos : WORD ':' expression ',' param_element_pos
                         | WORD ':' expression ','
                         | WORD ':' expression"""
    if len(p) == 6:
        p[0] = flatten_list([
            (p[1], p[3]), p[5]
        ])
    else:
        p[0] = [
            (p[1], p[3])
        ]

def p_param_element(p):
    """param_element : expression ',' param_element
                     | expression ',' param_element_pos
                     | expression ','
                     | expression"""
    if len(p) == 4:
        p[0] = flatten_list([
            (None, p[1]), p[3]
        ])
    else:
        p[0] = [
            (None, p[1])
        ]

def p_statement_break(p):
    "statement : BREAK"
    p[0] = {"function": "engine:control/break"}

def p_statement_expr(p):
    '''statement : expression'''
    p[0] = p[1]

def p_expression_function_call(p):
    '''expression : function_call'''
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''

    if isinstance(p[1], str):
        p[1] = {"#ref": p[1][1:-1]}
    if isinstance(p[3], str):
        p[3] = {"#ref": p[3][1:-1]}

    if isinstance(p[1], dict):
        if p[1].get("function", None) == "engine:math/solve":
            p[1].pop("function")
    if isinstance(p[3], dict):
        if p[3].get("function", None) == "engine:math/solve":
            p[3].pop("function")
    
    if p[2] == '+':
        p[0] = {"add": [p[1], p[3]]}
    elif p[2] == '-':
        p[0] = {"subtract": [p[1], p[3]]}
    elif p[2] == '*':
        p[0] = {"multiply": [p[1], p[3]]}
    elif p[2] == '/':
        p[0] = {"divide": [p[1], p[3]]}

    p[0].update({"function": "engine:math/solve"})

def p_expression_uminus(p):
    "expression : '-' expression"
    if isinstance(p[2], str):
        p[2] = {"#ref": p[2][1:-1]}

    if isinstance(p[2], dict):
        if p[2].get("function", None) == "engine:math/solve":
            p[2].pop("function")
    
    p[0] = {"function": "engine:math/solve", "multiply": [-1, p[2]]}

def p_comma_sep_expressions(p):
    """comma_expressions : expression ',' comma_expressions
                         | expression ','
                         | expression"""
    if len(p) == 4:
        p[0] = flatten_list([p[1], p[3]])
    else:
        p[0] = flatten_list([p[1]])

def p_expression_min(p):
    """expression : MIN '(' comma_expressions ')'
                  | MAX '(' comma_expressions ')'"""
    ls = p[3]
    for l in ls:
        if isinstance(l, dict):
            if l.get("function", None) == "engine:math/solve":
                l.pop("function")
    p[0] = {
        "function": "engine:math/solve",
        p[1].value: l
    }

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_return(p):
    """statement : RETURN expression
                 | RETURN"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_list(p):
    "list : '[' comma_expressions ']'"
    p[0] = p[2]

def p_table_contents(p):
    """table_contents : STRING ':' expression ',' table_contents
                      | NUMBER ':' expression ',' table_contents
                      | STRING ':' expression ','
                      | NUMBER ':' expression ','
                      | STRING ':' expression
                      | NUMBER ':' expression"""
    if len(p) == 6:
        p[0] = flatten_list([
            (p[1], p[3]),
            p[5]
        ])
    else:
        p[0] = [(p[1], p[3])]

def p_table(p):
    "table : '%' '{' table_contents '}'"
    d = {}
    for k, v in p[3]:
        d.update({k: v})
    p[0] = d

def p_expression_other(p):
    """expression : NUMBER
                  | BOOLEAN
                  | STRING
                  | WORD
                  | scope
                  | list
                  | table"""
    #print(p.slice)
    p[0] = p[1]

def p_expression_variable(p):
    "expression : VARIABLE"
    p[0] = {"#ref": p[1][1:-1]}

# def p_expression_name(p):
#     "expression : NAME"
#     try:
#         p[0] = names[p[1]]
#     except LookupError:
#         print("Undefined name '%s'" % p[1])
#         p[0] = 0

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' ({p.lineno}, {p.lexpos})")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()


# Parse an expression
# ast = parser.parse(example_script)#'2 * 3 + 4 * (5 - -<x>)') # 
# print("ast:", ast)

script_files = glob.glob("**/*.dungeon_script", recursive=True)


class EngineScript:

    def __init__(self, script_file):
        self.script_file = script_file

        for f in script_files:
            if f.endswith(f"{script_file.replace('.dungeon_script', '')}.dungeon_script"):
                self.script_file = f
                break

        self.script = ""
        self.compiled_script = {}

    def compile(self):
        with open(self.script_file, "r+", encoding="utf-8") as f:
            self.script = f.read()
        self.compiled_script = parser.parse(self.script)
    
    def getScript(self):
        #if not self.compiled_script:
        self.compile()
        return self.compiled_script


if __name__ == "__main__":
    engine_script = EngineScript(example_script)

    engine_script.compile()

    print(json.dumps(engine_script.getScript(), indent=4))

