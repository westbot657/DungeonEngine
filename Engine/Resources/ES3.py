# pylint: disable=W,R,C,import-error,assignment-from-no-return

try:
    from .EngineErrors import ScriptError, FinalScriptError, EOF
    from .Serializer import Serializer
    from .YieldTools import YieldTools
    from .LoaderFunction import LoaderFunction
except ImportError:
    from EngineErrors import ScriptError, FinalScriptError, EOF
    from Serializer import Serializer
    from YieldTools import YieldTools
    from LoaderFunction import LoaderFunction
    

from typing import Any

import re

test_script = """
#!emberhollow/rooms/boats/spawn_boat
#!enter-script

num_players = length(#dungeon.player_ids)

#dungeon.player_ids.append(#player.uid)

#player.tag: listening = true

$listening = #player.tag: listening

output("say `skip` to skeip dialog")

captain = random.choice(
    "...",
    "..."
)

starting_money = new: <engine:currency> {
    gold: random.range(9, 11),
    silver: random.range(5, 7),
    copper: random.range(2, 9)
}

if ($listening) {
    output("...")
    wait(2)
}

$out($message, $wait_time) {
    if ($listening) {
        output(
            format($message, captain=captain)
        )
        wait($wait_time)
    }
}

$outm($message, $wait_time) {
    if ($listening) {
        output(
            format($message, captain=captain, money=starting_money.total)
        )
        wait($wait_time)
    }
}

// ...

match random.choice([1, 2, 3, 4]) {
    case 1 {
        // ...
        $outm("{captain} hands you a bag of coins.\n(+{money})")
    }
}

#player.give_money(starting_money)


move: #player -> <emberhollow:rooms/docks/roads/road_4>


"""


class Node:
    def compile(self):
        return {}

class Statements(Node):
    def __init__(self, nodes:list[Node]):
        self.nodes = nodes
    
    def compile(self):
        return {
            "#functions": [node.compile() for node in self.nodes]
        }

class Comp(Node):
    def __init__(self, left:Node, op:str, right:Node):
        self.left = left
        self.op = op
        self.right = right
    
    def compile(self):
        return {
            "#function": "math.compare",
            self.op: [
                self.left.compile(),
                self.right.compile()
            ]
        }

class IfStatement(Node):
    def __init__(self, condition:Node, body:Node, else_node:Node=None):
        self.condition = condition
        self.body = body
        self.else_node = else_node
    
    def compile(self):
        return {
            "#check": self.condition.compile(),
            "true": self.body.compile(),
            "false": self.else_node.compile()
        }

class ForLoop(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class WhileLoop(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MatchCase(Node):
    def __init__(self, match_value:Node, cases:list[Node], bodies:list[Node]):
        self.match_value = match_value
        self.cases = cases
        self.bodies = bodies
    
    
    def compile(self):
        pass

class ClassDef(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class BinaryOp(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MacroDef(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MacroCall(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MacroAssign(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MacroRef(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class Table(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class Concat(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class BreakNode(Node):
    def __init__(self, token):
        self.token = token
    
    def compile(self):
        pass

class ReturnNode(Node):
    def __init__(self, token, expr:Node):
        self.token = token
        self.expr = expr
    
    def compile(self):
        pass

class PassNode(Node):
    def __init__(self, token):
        self.token = token
    
    def compile(self):
        pass

class ArgsDefNode(Node):
    def __init__(self, positional:list[Node], keyword:list[tuple[Node, Node]]):
        self.positional = positional
        self.keyword = keyword
    
    def compile(self):
        pass

class FunctionDefNode(Node):
    def __init__(self, name, args:ArgsDefNode, body:Node):
        self.name: EngineScript.Token = name
        self.args = args
        self.body = body
    
    def compile(self):
        pass

class EngineScript:
    _scripts = {}
    
    _patterns = {
        r"\/\/.*": "ignore",
        r"(?<!\/)\/\*(\*[^/]|[^*])+\*\/": "ignore",
        "\\#\\![^\n;]*;?": "CONTEXT",
        r"(\"(\\.|[^\"\\])*\"|\'(\\.|[^\'\\])*\')": "STRING",
        r"@[^ ]*": "TAG",
        r"\$[a-zA-Z_][a-zA-Z0-9_]*": "MACRO",
        r"\b(true|false)\b": "BOOLEAN",
        r"\<[^<> ]+\>": "OBJECT",
        r"(<=|>=|<|>|==|!=)": "COMP",
        r"(\.\.|::)": "CONCAT",
        r"\b(if|elif|else|while|for|in|and|not|or|true|false|none|match|case|class|def|break|continue)\b": "KEYWORD",
        r"[a-zA-Z_][a-zA-Z0-9_]*": "WORD",
        r"(\d+(\.\d+)?|\.\d+)": "NUMBER",
        r"\*\*": "POW",
        r"[=\-+*/()&\[\]{},#%:|^\.;~`]": "LITERAL",
        r"\n+": "NEWLINE",
        r"[\t ]+": "ignore"
    }

    class VarTable:
        def __init__(self):
            self.parent: EngineScript.VarTable = None
            self.vars = {}
        
        def exists(self, name:str):
            return name in self.vars or (self.parent and self.parent.exists(name))
    
        def get(self, name:str, default):
            if name in self.vars:
                return self.vars[name]
            if self.parent:
                return self.parent.get(name, default)
            else:
                return default
        
        def set(self, name:str, value:Any):
            self.vars.update({name: value})
        
        def scope_in(self):
            new = EngineScript.VarTable()
            new.parent = self
            return new

        def scope_out(self):
            return self.parent

        def clear(self):
            self.vars.clear()
            self.parent = None

    class Token:
        def __init__(self, es, value:str):
            self.es = es
            self.value = value
            self.raw = value
            
            for pattern, token_type in EngineScript._patterns.items():
                if re.fullmatch(pattern, self.value):
                    self.type = token_type

            self.line_start = es.line
            self.col_start = es.col

            es.lexpos += len(self.value)
            if x := self.value.count("\n"):
                es.line += x
                es.col = 0
            es.col += len(self.value.split("\n")[-1])
            
            self.line_end = es.line
            self.col_end = es.col

            if self.type == "NUMBER":
                self.value = float(self.value) if "." in self.value else int(self.value)
            elif self.type == "OBJECT":
                self.value = self.value[1:-1]
            elif self.type == "STRING":

                if not self.value.startswith(("\"", "'")):
                    self.value = self.value[2:-1]
                else:
                    self.value = self.value[1:-1]

                matches = list(re.finditer(r"\\.", self.value))
                matches.reverse()

                replacements = {
                    "\\n": "\n",
                    "\\\"": "\"",
                    "\\\'": "\'",
                    "\\\\": "\\"
                }
                for match in matches:
                    match:re.Match
                    self.value = self.value[0:match.start()] + replacements.get(match.group(), match.group()) + self.value[match.end():]

        def __eq__(self, other):
            if isinstance(other, EngineScript.Token):
                return self.type == other.type and self.value == other.value
            elif isinstance(other, tuple):
                return (self.type == other[0]) and ((self.value in other[1]) if isinstance(other[1], (tuple, list)) else (self.value == other[1]))

        def __str__(self):
            if self.line_start == self.line_end:
                return f"'{self.value}' (Line {self.line_start+1}, Column {self.col_start+1} to {self.col_end+1})"
            else:
                return f"'{self.value}' (Line {self.line_start+1}, Column {self.col_start+1} to Line {self.line_end+1}, Column {self.col_end+1})"

        def __repr__(self):
            return f"{self.type}: {self!s}"
    
        def unexpected(self, actual:str=""):

            if self.line_start == self.line_end:
                err_disp = self.es.script.split("\n")[self.line_start]
                err_disp += f"\n{' '*self.col_start}{'^'*(min(self.col_end-self.col_start, len(err_disp)-self.col_start))}"
            else:
                err_disp = ""

            return ScriptError(f"Unexpected token at Line {self.line_start+1}, Column {self.col_start+1}: {self.value!r}:\n\n{err_disp}" + (f"  Expected: {actual}" if actual else ""))

        def expected(self, actual, do_quotes=True):
            if self.line_start == self.line_end:
                err_disp = self.es.script.split("\n")[self.line_start]
                err_disp += f"\n{' '*self.col_start}{'^'*(min(self.col_end-self.col_start, len(err_disp)-self.col_start))}"
            else:
                err_disp = ""
            q = "'" if do_quotes else ""
            
            return FinalScriptError(f"Expected {q}{actual}{q} at Line {self.line_start+1}, Column {self.col_start+1}, got {self.value!r} instead.\n\n{err_disp}")

        def syntax(self, msg:str):
            # if self.col_start <= 4:
            out = f"Ln {self.line_start: <5} | {" "*self.col_start}{self.raw}"
            out2 = f"           {" "*self.col_start}{"~"*len(self.raw)}"
            return FinalScriptError(f"{msg}\nAt:\n{out}\n{out2}")
                

        def get_location(self):
            return f"Line {self.line_start+1}, Column {self.col_start+1}"

    class Macro:
        __slots__ = ["name", "token"]
        def __init__(self, name, token=None):
            self.name:str = name
            self.token:EngineScript.Token = token

    class MacroFunction:
        __slots__ = [
            "es", "name", "args", "code"
        ]
        def __init__(self, es, name, args, code):
            self.es: EngineScript = es
            self.name = name
            self.args = args
            self.code = code
        
        def compile(self, arg_values, macro_token):
            macro_token: EngineScript.Token
            if len(arg_values) > len(self.args):
                raise FinalScriptError(f"Too many args passed into macro at {macro_token.get_location()}")
            elif len(arg_values) < len(self.args):
                raise FinalScriptError(f"Too few args passed into macro at {macro_token.get_location()}")
            
            macros = {}
            
            for k, v in zip(self.args, arg_values):
                macros.update({k: v})
                
            return self.deep_replace(self.code, macros, macro_token)


        def deep_replace(self, obj:Any, repls:dict, macro_call_token):
            if isinstance(obj, EngineScript.Macro):
                if obj.name in repls:
                    return repls[obj.name]
                elif obj.name in self.es.macros:
                    return self.es.macros[obj.name]
                raise FinalScriptError(f"Undefined macro: '{obj.name}' in macro function")
            elif isinstance(obj, dict):
                out = {}
                for k, v in obj.items():
                    if isinstance(k, EngineScript.Macro):
                        if k.name in repls:
                            r = repls[k.name]
                            if isinstance(r, dict) and ((v2 := r.get("#ref", None)) is not None):
                                out.update({v2: self.deep_replace(v, repls, macro_call_token)})
                            else:
                                raise FinalScriptError(f"Macro at {k.token.get_location()} does not describe a variable, so cannot be assigned a value. Called at {macro_call_token.get_location()}")
                    else:
                        out.update({k: self.deep_replace(v, repls, macro_call_token)})
                return out
            elif isinstance(obj, list):
                return [self.deep_replace(v, repls, macro_call_token) for v in obj]
            else:
                return obj


    def serialize(self):
        return {
            "script_file": Serializer.serialize(""),
            "script_name": Serializer.serialize(""),
            "script": Serializer.serialize(self.script),
            "line": Serializer.serialize(self.line),
            "col": Serializer.serialize(self.col),
            "lexpos": Serializer.serialize(self.lexpos),
            "compiled_script": Serializer.serialize(self.compiled_script),
            "_tokens": Serializer.serialize([]),
            "do_analysis": Serializer.serialize(False),
            "macros": Serializer.serialize(self.macros),
            "macro_functions": Serializer.serialize(self.macro_functions),
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    @classmethod
    def inline_script(cls,
    script:str):
        s = super().__new__(cls)
        s.init("", "<inline>")
        s.script = script
        return s

    def __new__(cls, script_file, do_analysis=False):
        script_name = f"{script_file.replace("\\", "/").replace(".ds", "").replace(".dungeon_script", "")}.ds"
        
        if script_name in cls._scripts:
            return cls._scripts[script_name]

        else:
            script = super().__new__(cls)
            cls._scripts.update({script_name: script})
            script.init(script_file, script_name, do_analysis)
            return script
    
    def init(self, script_file:str, script_name:str, do_analysis:bool=False):
        self.script_file = script_file
        self.script_name = script_name
        self.macro_functions: dict[str, EngineScript.MacroFunction] = {}
        self.macros: dict[str, Any] = {}
        self.script = ""
        self.line = 0
        self.col = 0
        self.lexpos = 0
        self.compiled_script = {}
        self.do_analysis = do_analysis
        self._tokens = []
        self.variable_table = EngineScript.VarTable()
        self.exec_depth = 0

    class ExecReturn:
        def __init__(self, type:str, value:Any):
            self.type = type
            self.value = value

    def execute(self):
        yt = YieldTools("ES3:execute")
        yield from yt.call(self._execute, self.compiled_script)
        r = yt.result()
        print(r)
        


    def _execute(self, branch:Any, context_object:Any=None):
        self.exec_depth += 1
        yt = YieldTools(f"ES3:_execute:{self.exec_depth}")
        if isinstance(branch, dict):
            if (function := branch.get("#function", None)) is not None:
                ...
            elif (funcs := branch.get("#functions", None)):
                if isinstance(funcs, list):
                    ...
                elif isinstance(funcs, dict):
                    
                    yield from yt.call(self._execute, )
            elif (script := branch.get("#script", None)):
                ...
            elif (call := branch.get("#call", None)) is not None:
                ...
            elif (ref := branch.get("#ref", None)):
                ...
            elif (store := branch.get("#store", None)):
                ...
        elif isinstance(branch, list):
            ...
        else:
            self.exec_depth
            return EngineScript.ExecReturn("value", branch)

    def compile(self):
        self.macro_functions.clear()
        self.macros.clear()
        
        self.line = 0
        self.col = 0
        
        tokens = self.tokenize()
        
        tokens = [t for t in tokens if t.type not in ["ignore", "context_hint"]]
        # print(tokens)

        self.build(tokens)
    
    def tokenize(self) -> list[Token]:
        """
        Returns a list of tokens from the script
        """
        return [EngineScript.Token(self, t.group()) for t in re.finditer("(?:"+"|".join(self._patterns.keys())+")", self.script)]
    
    def cleanup(self, ast):
        # print(f"CLEANUP: {ast}")
        if isinstance(ast, dict):
            if "functions" in ast and ast["functions"] == []:
                ast.pop("functions")
            if "true" in ast and ast["true"] == {"functions": []}:
                ast.update({"true": {}})
            if "false" in ast and ast["false"] == {"functions": []}:
                ast.update({"false": {}})
            out = {}
            for k, v in ast.items():
                x = self.cleanup(v)
                out.update({k: x})
            return out
        elif isinstance(ast, list):
            lst = []
            for l in ast:
                x = self.cleanup(l)
                if not any(x == h for h in (None, {})):
                    lst.append(x)
            return lst
        return ast
    
    def build(self, tokens:list[Token]):
        t = bool(tokens)
        if tokens:
            try:
                ast = self.statements(tokens)
                self.compiled_script = self.cleanup(ast.compile())
            except EOF:
                self.compiled_script = {}
        if t and self.compiled_script == {}:
            print(f"Warning:\n    File '{self.script_file}' contained code that compiled to nothing.")

    def statements(self, tokens:list[Token]):
        stmts = []
        while tokens:
            try:
                stmt = self.statement(tokens)
                stmts.append(stmt)
            except EOF as e:
                break
            except ScriptError as e:
                if tokens and tokens[0] == ("LITERAL", "}"):
                    break
        return Statements(stmts)

    def statement(self, tokens:list[Token]) -> Node:
        if not tokens:
            raise EOF()
        
        if tokens[0] == ("KEYWORD", "break"):
            return BreakNode(tokens.pop(0))

        elif tokens[0] == ("KEYWORD", "return"):
            ret_token = tokens.pop(0)
            
            if tokens:
                if tokens[0].line_start == ret_token.line_start:
                    expr = self.expression(tokens)
                else:
                    expr = None
            else:
                expr = None

            return ReturnNode(ret_token, expr)
        
        elif tokens[0] == ("KEYWORD", "pass"):
            return PassNode(tokens.pop(0))
    
        elif tokens[0] == ("KEYWORD", "def"):
            return self.function_def(tokens)

        elif tokens[0] == ("KEYWORD", "class"):
            return self.class_def(tokens)
        
        elif tokens[0] == ("KEYWORD", "if"):
            return self.if_statement(tokens)
        
        elif tokens[0] == ("KEYWORD", "match"):
            return self.match_case(tokens)
        
        elif tokens[0] == ("KEYWORD", "while"):
            return self.while_loop(tokens)
        
        elif tokens[0] == ("KEYWORD", "for"):
            return self.for_loop(tokens)
        
        else:
            return self.expression(tokens)
    
    def expression(self, tokens:list[Token]):
        pass

    def function_def(self, tokens:list[Token]):
        d = tokens.pop(0) # pop the 'def' keyword
        
        if not tokens: # there is no situation in which 'def' shouldn't be immediately followed by a word
            raise FinalScriptError(f"Expected function name after def keyword @ {d.get_location()}")
        
        if tokens[0].type == "WORD":
            name = tokens.pop(0)
        else:
            raise tokens[0].expected("function name", False)
        
        if not tokens:
            raise EOF() # blank definition at EOF doesn't make much sense, but I guess it's fine. (might be good for dse files)
        
        if tokens[0] == ("LITERAL", "("):
            args = self.param_def_list(tokens)
        elif tokens[0] == ("LITERAL", ";"):
            args = ArgsDefNode([], [])
            body = Statements([])
            return FunctionDefNode(name, args, body)
        else:
            raise tokens[0].expected("(")
        
        if not tokens:
            raise EOF()
        
        if tokens[0] == ("LITERAL", "{"):
            body = self.scope(tokens)
        else:
            raise tokens[0].unexpected("'{' or newline")
        
        return FunctionDefNode(name, args, body)
    
    def scope(self, tokens:list[Token]):
        open = tokens.pop(0) # pop '{'
        body = self.statements(tokens)
        
        if tokens and tokens[0] == ("LITERAL", "}"):
            tokens.pop(0)
            return body
        elif tokens:
            return tokens[0].expected("}")
        else:
            raise FinalScriptError(f"no valid closing bracket found for open bracket @ {open.get_location()}")
    
    def param_def_list(self, tokens:list[Token]):
        pass

    def class_def(self, tokens:list[Token]):
        clss = tokens.pop(0)
        
        if tokens and tokens[0].type == "OBJECT":
            name = tokens.pop(0)
            
        

    def if_statement(self, tokens:list[Token]):
        pass

    def match_case(self, tokens:list[Token]):
        pass

    def while_loop(self, tokens:list[Token]):
        pass

    def for_loop(self, tokens:list[Token]): # I kinda want support for python-style and C-style for loops...
        pass

"""
statements : statement*

statement : BREAK
          | RETURN expression?
          | PASS
          | function_def
          | class_def
          | if_statement
          | match_case
          | while_loop
          | for_loop
          | expression

expression : comp

if_statement : IF '(' expression ')' scope (elif_branch|else_branch)?

while_loop : WHILE '(' expression ')' scope

for_loop : FOR '(' word_list IN expreesion ')' scope

scope : '{' statements '}'

elif_branch : ELSEIF '(' expression ')' scope (elif_branch|else_branch)?

else_branch : ELSE scope

comp : NOT comp
     | arith (LT|LE|GT|GE|EE|NE) arith
     | comp (AND|OR) comp
     | arith

macro : MACRO '(' macro_args ')' '=' macro_scope
      | MACRO '(' comma_expressions ')'
      | MACRO '=' expression
      | MACRO

macro_args : (MACRO ','?)+

macro_scope : '{' macro_statements '}'

arith : mul (('+'|'-') mul)*

mul : pow (('*'|'/'|'%') pow)*

pow : concat ('^' concat)*

concat : var (CONCAT var)? (CONCATSEP var)?

atom : var '=' expression
     | var
     | '-' atom
     | '(' expression ')'
     | (NUMBER|BOOL|STRING|OBJECT|table|WORD|scope|macro|function_call)

var : WORD (('.' WORD)* ('[' expression ']')*)

table : '[' comma_expressions ']'
      | '{' table_contents '}'

function_call : var parameters scope?
              | 'new' ':' OBJECT scope

table_contents : (expression ':' expression ','?)*

parameters : '(' param_elements* ')'

param_elements : (expression ',')* (WORD '=' expression ','?)*

function_def : 'def' WORD '(' ( (WORD ','?)* (WORD '=' expression ','?)* )? ')' scope

class_def : 'class' OBJECT scope

"""




if __name__ == "__main__":
    es = EngineScript.inline_script(test_script)
    
    es.compile()
