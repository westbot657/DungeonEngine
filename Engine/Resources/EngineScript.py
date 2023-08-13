# pylint: disable=[W,R,C,import-error, assignment-from-no-return, assignment-from-none]

try:
    from .LoaderFunction import LoaderFunction
    from .Functions import *
    from .ply.ply import lex
    from .ply.ply import yacc
except ImportError:
    from LoaderFunction import LoaderFunction
    from Functions import *
    from ply.ply import lex
    from ply.ply import yacc
import re, json

example_script = """
// example script: (based on combat.json)

// this is a comment

[engine:list/for_each] (<.enemies>)
{
    [engine:text/match] ([engine:text/replace_pattern] (" +", " ", [engine:text/set_case] (<#text>, "lower")))
    @pattern: [engine:text/set_case] (<element.name>, "lower"){
        return "idk"
    }
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

tokens = (
    "FUNCTION", "VARIABLE", "NUMBER", "STRING", "BOOLEAN",
    "TAG", "WORD", "RETURN", "BREAK", "CONTINUE", "MIN", "MAX"
)

literals = ["=", "-", "+", "*", "/", "(", ")", "[", "]", "{", "}", ",", "#"]

t_ignore = " \t;~`\n"

t_ignore_comment = r"\/\/.*"

t_FUNCTION = r"\[[^\]]+\]"
t_VARIABLE = r"\<[^>]+\>"
t_STRING = r"(\"[^\"]*\"|'[^']*')"
t_BOOLEAN = r"(true|false)"
t_TAG = r"@[^\:]+\:"


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
    r"\d+"
    t.value = int(t.value)
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
)

#names = {}

start="expressions"

tree = {}

def p_statement_assign(p):
    'statement : VARIABLE "=" expression'
    print(p.slice)
    p[0] = {"#store": {p[1][1:-1]: p[3]}}
    #names[p[1]] = p[3]

    tree.clear()
    tree.update(p[0])

def p_function_call(p):
    '''function_call : FUNCTION parameters scope
                     | FUNCTION parameters tag_list
                     | FUNCTION parameters
                     | FUNCTION'''
    if len(p) == 4:
        d = p[3]
        if d.get("scope", None) is not None:
            ...
        else:
            ...
    elif len(p) == 3:
        ...
    else:
        ...

def p_tag(p):
    '''tag : TAG expression'''
    p[0] = {
        p[1].value: p[2]
    }

def p_tag_list(p):
    '''tag_list : tag '#' scope tag_list
                | tag '#' scope'''
    print(p.slice)
    if len(p) == 5:
        d = p[1]
        d.update(p[3])
        p[0] = flatten_list([
            d,
            p[4]
        ])

def p_scope(p):
    "scope : '{' expressions '}'"
    p[0] = {"scope": p[2]}

def p_statements(p):
    """expressions : statement expressions
                   | statement"""
    print(p.slice)

def p_parameters(p):
    """parameters : '(' param_element ')'
                  | '(' ')'"""
    print(p.slice)

def p_param_element2(p):
    """param_element_pos : WORD ':' expression ',' param_element_pos
                         | WORD ':' expression ','
                         | WORD ':' expression"""
    print(p.slice)

def p_param_element(p):
    """param_element : expression ',' param_element
                     | expression ',' param_element_pos
                     | expression ','
                     | expression"""
    print(p.slice)

def p_statement_expr(p):
    '''statement : expression
                 | BREAK
                 | CONTINUE'''
    print(p.slice)

def p_expression_function_call(p):
    '''expression : function_call'''
    print(p.slice)

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    print(p.slice)

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
    print(p.slice)
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
    print(p.slice)
    p[0] = p[2]

def p_expression_return(p):
    """statement : RETURN expression
                 | RETURN"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_expression_other(p):
    """expression : NUMBER
                  | BOOLEAN
                  | STRING
                  | VARIABLE
                  | WORD
                  | scope"""
    #print(p.slice)
    p[0] = p[1]


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
ast = parser.parse(example_script)#'2 * 3 + 4 * (5 - -<x>)') # 
print("ast:", ast)


class Token:
    def __init__(self, token_type:str, content:str, start:int, end:int):
        self.token_type = token_type
        self.content = content
        self._start = start
        self._end = end

    def start(self):
        return self._start
    def span(self):
        return (self._start, self._end)
    def groupdict(self):
        return {self.token_type: self.content}

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.token_type == other.token_type and self.content == other.content
        elif isinstance(other, (str, int, bool)):
            return self.content == other
        elif isinstance(other, (list, tuple)):
            return (self.token_type == other[0] or other[0] is ...) and (self.content == other[1] or other[1] is ...)

    @classmethod
    def from_match(cls, match:re.Match):
        di = match.groupdict()
        key = list(di.keys())[0]
        val = di[key]
        return cls(key, val, match.start(), match.end())

class Scope:
    def __init__(self, statements:list):
        self.statements = statements

class Tag:
    def __init__(self, tag_value, scope:Scope):
        self.tag_value = tag_value
        self.scope = scope

class FunctionCall:
    def __init__(self, name:str, parameters:list|None=None, scope:Scope|None=None, tags:list[Tag]|None=None):
        self.name = name
        self.parameters = parameters
        self.scope = scope
        self.tags = tags

class Assignment:
    def __init__(self, name:str, value):
        self.name = name
        self.value = value

class Reference:
    def __init__(self, name:str):
        self.name = name

class Break:
    def __init__(self):
        pass

class Return:
    def __init__(self, ret_val=None):
        self.ret_val = ret_val

class String:
    def __init__(self, text):
        self.text = text

class Number:
    def __init__(self, num):
        self.num = num

class Boolean:
    def __init__(self, val):
        self.val = val


class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Subtract:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Divide:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Negative:
    def __init__(self, value):
        self.value = value

# () * / + -


class EngineScript:
    parse_pattern = r"((?P<comment>\/\/.*)|(?P<function>\[[^\]]*])|(?P<lparen>\()|(?P<rparen>\))|(?P<var><[^>]*>)|(?P<comma>,)|(?P<lbracket>{)|(?P<rbracket>})|(?P<lbrace>\[)|(?P<rbrace>\])|(?P<tag>\@[^\:]*\:)|(?P<quote>\")|(?P<single_quote>')|(?P<colon>\:)|(?P<other>[a-zA-Z0-9_+\-\*\/\=~\\\;\.]+)|(?P<spaces> +))"

    def __init__(self, script:str):
        self.script = script
        self.tokens = []

        self.components = []
        self.index = 0
        self.current = None

    def parse_function_call(self, return_node=False):
        func = self.tokens[self.index]

        func_node = FunctionCall(func.content)


        if return_node:
            return func_node

    def parse_parameters(self, return_node=False):
        ...

    def parse_list(self, return_node=False):
        ...

    def parse_assignment(self, return_node=False):
        ...

    def parse_math(self, return_node=False):
        ...

    def parse_word(self, return_node=False):
        c = self.current.content
        if c.isnumeric():
            return self.parse_math(return_node)
        else:
            if c == "return":
                r = Return()

                if t := self.getToken(self.index+1):
                    if t.token_type == "function": #in ["function", "lparen", "lbracket", "lbrace", "quote", "var"]:
                        r.ret_val = self.parse_function_call(True)
                    elif t.token_type == "lparen":
                        r.ret_val = self.parse_parameters(True)

                self.components.append()
                return
            elif c == "break":
                self.components.append()

    def parse_string(self, return_node=False):
        c = self.current
        self.index += 1
        string_components = []
        while self.index < len(self.tokens):
            self.current = curr = self.tokens[self.index]
            if curr.token_type == c.token_type:
                s = String("".join(_c.content) for _c in string_components)
                if return_node:
                    return s
                self.components.append(s)
                return
            string_components.append(curr)
        raise Exception("EOF while parsing string")

    def parse_scope(self, return_node=False):
        s = None
        while self.index < len(self.tokens):
            match: Token = self.tokens[self.index]

            self.current = match

            d = match.groupdict()

            if d.get("function", None) is not None:
                s = self.parse_function_call(return_node)
            elif d.get("lparen", None) is not None:
                s = self.parse_parameters(return_node)
            elif d.get("rparen", None) is not None:
                raise Exception(f"un-matched parenthesis at {match.span()}")
            elif d.get("lbracket", None) is not None:
                s = self.parse_scope(return_node)
            elif d.get("rbracket", None) is not None:
                self.index += 1
                return s
            elif d.get("lbrace", None) is not None:
                s = self.parse_list(return_node)
            elif d.get("rbrace", None) is not None:
                raise Exception(f"un-matched brace at {match.span()}")
            elif d.get("comma", None) is not None:
                raise Exception(f"unnecessary comma at {match.start()}")
            elif d.get("tag", None) is not None:
                raise Exception(f"unnecessary tag at {match.span()}")
            elif d.get("quote", None) is not None:
                s = self.parse_string(return_node)
            elif d.get("single_quote", None) is not None:
                s = self.parse_string(return_node)
            elif d.get("var", None) is not None:
                s = self.parse_assignment(return_node)
            elif d.get("colon", None) is not None:
                raise Exception(f"unnecessary colon at {match.start()}")
            elif d.get("other", None) is not None:
                s = self.parse_word(return_node)
            
            self.index += 1

        return s

    def getToken(self, index):
        if 0 <= index < len(self.tokens):
            return self.tokens[index]
        return None

    def compile(self):
        self.tokens = [Token.from_match(m) for m in re.finditer(self.parse_pattern, f"{{{self.script}}}")]

        self.parse_scope()








# if __name__ == "__main__":
#     engine_script = EngineScript(example_script)

#     engine_script.compile()
