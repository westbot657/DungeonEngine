# pylint: disable=[W,R,C,import-error, assignment-from-no-return, assignment-from-none]

try:
    from .LoaderFunction import LoaderFunction
    from .Functions import *
    from .ply.ply import lex
    from .ply.ply import yacc
    from .Identifier import Identifier
    from .Logger import Log
except ImportError:
    from LoaderFunction import LoaderFunction
    from Functions import *
    from ply.ply import lex
    from ply.ply import yacc
    from Identifier import Identifier
    from Logger import Log
import re, json, glob


macros = {}

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
    "TAG", "WORD", "RETURN", "BREAK", "CONTINUE", "MIN", "MAX",
    "IF", "ELSEIF", "ELSE", "AND", "OR", "EE", "NE", "GT", "GE",
    "LT", "LE", "NOT", "MACRO", "PASS", "POW"
)

literals = [
    "=", "-", "+", "*", "/", "(", ")", "&",
    "[", "]", "{", "}", ",", "#", "%", ":",
    "|", "^"
]

t_POW = r"\*\*"
t_ignore = " \t;~`"

t_ignore_comment = r"\/\/.*"
t_ignore_comment2 = r"(?<!\/)\/\*(\*[^/]|[^*])+\*\/"

t_FUNCTION = r"\[([^:\[]+:)(([^\/\]\[]+\/)*)([^\[\]]+)\]"

t_TAG = r"@[^\:]+\:"
t_MACRO = r"\$[a-zA-Z_][a-zA-Z0-9_]*"

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_BOOLEAN(t):
    r"(true|false)"
    t.value = t.value == "true"
    return t

def t_STRING(t):
    r"(\"(\\.|[^\"\\])*\"|\'(\\.|[^\'\\])*\')"
    
    if not t.value.startswith(("\"", "'")):
        t.value = t.value[2:-1]
    else:
        t.value = t.value[1:-1]

    matches = list(re.finditer(r"\\.", t.value))
    matches.reverse()

    replacements = {
        "\\n": "\n",
        "\\\"": "\"",
        "\\\'": "\'",
        "\\\\": "\\"
    }
    for match in matches:
        match:re.Match
        t.value = t.value[0:match.start()] + replacements.get(match.group(), match.group()) + t.value[match.end():]
    
    return t

def t_VARIABLE(t):
    r"\<[^<> ]+\>"
    return t

def t_COMP(t):
    r"(<=|>=|<<|>>|==|!=)"
    match t.value:
        case "<=":
            t.type = "LE"
        case ">=":
            t.type = "GE"
        case "<<":
            t.type = "LT"
            t.value = "<"
        case ">>":
            t.type = "GT"
            t.value = ">"
        case "==":
            t.type = "EE"
        case "!=":
            t.type = "NE"
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
    elif t.value == "if":
        t.type = "IF"
    elif t.value == "elif":
        t.type = "ELSEIF"
    elif t.value == "else":
        t.type = "ELSE"
    elif t.value == "and":
        t.type = "AND"
    elif t.value == "or":
        t.type = "OR"
    elif t.value == "not":
        t.type = "NOT"
    elif t.value == "pass":
        t.type = "PASS"
    return t

def t_NUMBER(t):
    r"(\d+(\.\d+)?|\.\d+)"
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_error(t):
    
    Log["ERROR"]["engine script"]("Illegal character '%s'" % t.value[0])
    # print(t)
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'EE', 'NE'),
    ('left', 'AND', 'OR')
)

start="expressions"

def p_pass(p):
    '''expression : PASS'''
    p[0] = None

def p_macro_statement(p):
    '''expression : MACRO '=' expression
                  | MACRO'''
    if len(p) == 4:
        macros.update({p[1]: p[3]})
        p[0] = None
    else:
        if p[1] in macros:
            p[0] = macros[p[1]]
        else:
            raise Exception(f"Macro not defined: '{p[1]}'")

def p_statement_assign(p):
    '''atom : VARIABLE '=' expression
            | VARIABLE'''
    if len(p) == 4:
        if isinstance(p[3], dict) and "scope" in p[3] and len(p[3]) == 1:
            p[3] = p[3]["scope"]["functions"]
        p[0] = {"#store": {p[1][1:-1]: p[3]}}
    else:
        if p[1].startswith("<$"):
            p[0] = {"#call": p[1][1:-1]}
        elif p[1].startswith("</$"):
            p[0] = {"#ref": p[1][2:-1]}
        else:
            p[0] = {"#ref": p[1][1:-1]}

def p_else_branch(p):
    """else_branch : ELSE scope"""
    p[0] = {
        "false": p[2]["scope"]
    }

def p_elif_branch(p):
    """elif_branch : ELSEIF '(' expression ')' scope elif_branch
                   | ELSEIF '(' expression ')' scope else_branch
                   | ELSEIF '(' expression ')' scope"""
    d = {
        "false": {
            "@check": p[3],
            "true": p[5]["scope"]
        }
    }
    if len(p) == 7:
        d["false"].update(p[6])
    p[0] = d

def p_if_statement(p):
    '''if_condition : IF '(' expression ')' scope elif_branch
                    | IF '(' expression ')' scope else_branch
                    | IF '(' expression ')' scope'''
    d = {
        "@check": p[3],
        "true": p[5]["scope"]
    }
    if len(p) == 7:
        d.update(p[6])
    p[0] = d

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
                    if args_name:
                        found = True
                        parameters["*args"][args_name].append(value)
                    else:
                        state = "args"
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
    
    if func.id.full() != "engine:control/check_predicate":
        data = {
            "function": func.id.full()
        }
    else:
        data = {}
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
        data.update({scope_name: s})

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
    """scope : '{' expressions '}'
             | '{' '}'"""
    if len(p) == 3:
        p[0] = {"scope": {"functions": []}}
    else:
        p[0] = {"scope": p[2]}

def p_statements(p):
    """expressions : statement expressions
                   | statement
                   | """
    if len(p) == 3:
        if p[1] and p[2]["functions"]:
            p[0] = {
                "functions": [p[1]] + p[2]["functions"]
            }
        elif p[1] and (not p[2]["functions"]):
            p[0] = {
                "functions": [p[1]]
            }
        elif (not p[1]) and p[2]["functions"]:
            p[0] = {
                "functions": p[2]["functions"]
            }
        elif (not p[1]) and (not p[2]["functions"]):
            raise Exception("uhhhh...")
            # this shouldn't be possible...
    elif len(p) == 2:
        p[0] = {
            "functions": [p[1]]
        }
    else:
        p[0] = {}

def p_parameters(p):
    """parameters : '(' param_element ')'
                  | '(' ')'"""
    if len(p) == 4:
        p[0] = {"parameters": p[2]}
    else:
        p[0] = {"parameters": []}

def p_param_element2(p):
    """param_element_pos : WORD '=' expression ',' param_element_pos
                         | WORD '=' expression ','
                         | WORD '=' expression"""
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
    '''statement : expression
                 | if_condition'''
    p[0] = p[1]

def p_expression_function_call(p):
    '''atom : function_call'''
    p[0] = p[1]

def p_comp_expression(p):
    """comp : NOT comp
            | arith LT arith
            | arith LE arith
            | arith GT arith
            | arith GE arith
            | arith EE arith
            | arith NE arith
            | comp AND comp
            | comp OR comp
            | arith"""
    if len(p) == 2:
        p[0] = p[1]
        return
    

    if len(p) == 3:
        if isinstance(p[2], dict):
            if p[2].get("function", None) == "engine:logic/compare":
                p[2].pop("function")
        p[0] = {
            "function": "engine:logic/compare",
            "not": p[2]
        }
        return

    # if isinstance(p[1], str) and p[1].startswith("<"):
    #     p[1] = {"#ref": p[1][1:-1]}
    # if isinstance(p[3], str) and p[3].startswith("<"):
    #     p[3] = {"#ref": p[3][1:-1]}

    if isinstance(p[1], dict):
        if p[1].get("function", None) == "engine:logic/compare":
            p[1].pop("function")
    if isinstance(p[3], dict):
        if p[3].get("function", None) == "engine:logic/compare":
            p[3].pop("function")
    
    match p[2]:
        case "<":
            p[0] = {"<": [p[1], p[3]]}
        case ">":
            p[0] = {">": [p[1], p[3]]}
        case "<=":
            p[0] = {"<=": [p[1], p[3]]}
        case ">=":
            p[0] = {">=": [p[1], p[3]]}
        case "==":
            p[0] = {"==": [p[1], p[3]]}
        case "!=":
            p[0] = {"!=": [p[1], p[3]]}
        case "and":
            p[0] = {"and": [p[1], p[3]]}
        case "or":
            p[0] = {"or": [p[1], p[3]]}
        
    p[0].update({"function": "engine:logic/compare"})

def p_expression_binop(p):
    '''arith : atom '+' atom
             | atom '-' atom
             | atom '*' atom
             | atom '/' atom
             | atom '%' atom
             | atom '&' atom
             | atom '|' atom
             | atom '^' atom
             | atom POW atom
             | atom'''

    if len(p) == 2:
        p[0] = p[1]
        return

    # if isinstance(p[1], str) and p[1].startswith("<"):
    #     p[1] = {"#ref": p[1][1:-1]}
    # if isinstance(p[3], str) and p[3].startswith("<"):
    #     p[3] = {"#ref": p[3][1:-1]}

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
    elif p[2] == "%":
        p[0] = {"mod": [p[1], p[3]]}
    elif p[2] == "&":
        p[0] = {"binand": [p[1], p[3]]}
    elif p[2] == "|":
        p[0] = {"binor": [p[1], p[3]]}
    elif p[2] == "^":
        p[0] = {"binxor": [p[1], p[3]]}
    elif p[2] == "**":
        p[0] = {"pow": [p[1], p[3]]}
    

    p[0].update({"function": "engine:math/solve"})

def p_expression_uminus(p):
    "atom : '-' atom"
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
    """arith : MIN '(' comma_expressions ')'
             | MAX '(' comma_expressions ')'"""
    ls = p[3]
    for l in ls:
        if isinstance(l, dict):
            if l.get("function", None) == "engine:math/solve":
                l.pop("function")
    p[0] = {
        "function": "engine:math/solve",
        p[1]: l
    }

def p_expression_group(p):
    "atom : '(' expression ')'"
    p[0] = p[2]

def p_expression_return(p):
    """statement : RETURN expression
                 | RETURN"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

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
        if isinstance(p[3], dict) and "scope" in p[3]:
            p[3] = p[3]["scope"]
        p[0] = [(p[1], p[3])]

def p_table(p):
    """table : '%' '[' comma_expressions ']'
             | '%' '{' table_contents '}'"""
    #print(f"\n\ntable: {p.slice}\n\n")
    if len(p[3]) > 0 and isinstance(p[3][0], tuple):
        d = {}
        for k, v in p[3]:
            if isinstance(v, dict) and "scope" in v:
                v = v["scope"]["functions"]
            d.update({k: v})
        p[0] = d
    else:
        if isinstance(p[3], dict) and "scope" in p[3]:
            p[3] = p[3]["scope"]["functions"]
        p[0] = p[3]

def p_expression_other(p):
    """atom : NUMBER
            | BOOLEAN
            | STRING
            | table
            | WORD
            | scope"""
    #print(p.slice)
    if isinstance(p[1], dict) and "scope" in p[1] and len(p[1]) == 1:
        p[1] = p[1]["scope"]["functions"]
    p[0] = p[1]

def p_expression_comp(p):
    "expression : comp"
    p[0] = p[1]

def p_error(p):
    if p:
        Log["ERROR"]["engine script"](f"Syntax error at '{p.value}' ({p.lineno}, {p.lexpos})")
    else:
        return {}
        # Log["ERROR"]["engine script"]("Syntax error at EOF")
    # print(p)

# Build the parser
parser = yacc.yacc()


script_files = glob.glob("**/*.dungeon_script", recursive=True) + glob.glob("**/*.ds", recursive=True)


class EngineScript:

    _scripts = {}

    def __new__(cls, script_file):

        for f in script_files:
            if f.replace("\\", "/").endswith(f"{script_file.replace('.dungeon_script', '').replace('.ds', '')}.dungeon_script".replace("\\", "/")):
                script_file = f
                break
            elif f.replace("\\", "/").endswith(f"{script_file.replace('.dungeon_script', '').replace('.ds', '')}.ds".replace("\\", "/")):
                script_file = f
                break

        if script_file in EngineScript._scripts:
            return EngineScript._scripts[script_file]
        else:
            self = super().__new__(cls)
            self._init_(script_file)
            EngineScript._scripts.update({script_file: self})
            return self

    def _init_(self, script_file):
        self.script_file = script_file

        for f in script_files:
            if f.replace("\\", "/").endswith(f"{script_file.replace('.dungeon_script', '').replace('.ds', '')}.dungeon_script".replace("\\", "/")):
                self.script_file = f
                break
            elif f.replace("\\", "/").endswith(f"{script_file.replace('.dungeon_script', '').replace('.ds', '')}.ds".replace("\\", "/")):
                self.script_file = f
                break

        self.script = ""
        self.compiled_script = {}

    @classmethod
    def preCompileAll(cls):
        Log["loadup"]["engine script"]("loading and compiling scripts")
        for script_file in script_files:
            Log["loadup"]["engine script"](f"compiling script '{script_file}'")
            es = EngineScript(script_file)
            es.compile()
        Log["loadup"]["engine script"]("all scripts compiled")

    def setRawScript(self, script):
        self.script = script
        self.compile(ignore_file=True)

    def compile(self, ignore_file=False):
        if not ignore_file:
            with open(self.script_file, "r+", encoding="utf-8") as f:
                self.script = f.read()

        macros.clear()

        self.compiled_script = parser.parse(self.script)
    
    def getScript(self):
        if not self.compiled_script:
            self.compile()
        return self.compiled_script



if __name__ == "__main__":

    import os, sys

    if len(sys.argv) > 1:
        f = sys.argv.pop(1)
    else:
        f = None

    if f:
        os.chdir("C:\\Users\\Westb\\Desktop\\Python-Projects\\DungeonEngine\\DungeonEngine")
        try:
            engine_script = EngineScript(f)
            engine_script.compile()
            print(json.dumps(engine_script.getScript(), indent=4))
        except Exception as e:
            print(e)
    else:

        while True:

            try:
                engine_script = EngineScript(input("file > "))
                engine_script.compile()

                print(json.dumps(engine_script.getScript(), indent=4))
            except Exception as e:
                print(e)
