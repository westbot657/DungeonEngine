# pylint: disable=[W,R,C,assignment-from-no-return]

# This is attampt 2 at a Engine Script parser but with syntax error position finding

try:
    from .LoaderFunction import LoaderFunction
    from .Functions import *
    from .Identifier import Identifier
    from .Logger import Log
    from .EngineErrors import FinalScriptError, ScriptError, EOF
except ImportError:
    from LoaderFunction import LoaderFunction
    from Functions import *
    from Identifier import Identifier
    from Logger import Log
    from EngineErrors import FinalScriptError, ScriptError, EOF

import re, glob, json

from typing import Any


class EngineScript:

    _scripts = {}
    script_files: list = []

    @classmethod
    def load(cls):
        cls.script_files = glob.glob("**/*.dungeon_script", recursive=True) + glob.glob("**/*.ds", recursive=True)

    def __new__(cls, script_file):

        for f in cls.script_files:
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

        for f in self.script_files:
            if f.replace("\\", "/").endswith(f"{script_file.replace('.dungeon_script', '').replace('.ds', '')}.dungeon_script".replace("\\", "/")):
                self.script_file = f
                break
            elif f.replace("\\", "/").endswith(f"{script_file.replace('.dungeon_script', '').replace('.ds', '')}.ds".replace("\\", "/")):
                self.script_file = f
                break

        self.script = ""
        self.line = 0
        self.col = 0
        self.lexpos = 0
        self.compiled_script = {}
        self._tokens = []
        
        self.macros: dict[str, Any] = {}
        self.macro_functions: dict[str, EngineScript.MacroFunction] = {}

    @classmethod
    def preCompileAll(cls):
        Log["loadup"]["engine script"]("loading and compiling scripts")
        for script_file in cls.script_files:
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
                self.script = f.read()#self.remove_syntax_sugar(f.read())

        self.macros.clear()
        self.macro_functions.clear()

        self.parse()

    _patterns = {
            r"\/\/.*": "ignore",
            r"(?<!\/)\/\*(\*[^/]|[^*])+\*\/": "ignore",
            r"\[([^:\[]+:)(([^\/\]\[]+\/)*)([^\[\]]+)\]": "FUNCTION",
            r"@[^\:]+\:": "TAG",
            r"\$[a-zA-Z_][a-zA-Z0-9_]*": "MACRO",
            r"\b(true|false)\b": "BOOLEAN",
            r"(\"(\\.|[^\"\\])*\"|\'(\\.|[^\'\\])*\')": "STRING",
            r"\<[^<> ]+\>": "VARIABLE",
            r"(<=|>=|<|>|==|!=)": "COMP",
            r"(\.\.|::)": "CONCAT",
            r"\b(if|elif|else|while|for|in|and|not|or|true|false|none)\b": "KEYWORD",
            r"[a-zA-Z_][a-zA-Z0-9_]*": "WORD",
            r"(\d+(\.\d+)?|\.\d+)": "NUMBER",
            r"\*\*": "POW",
            r"[=\-+*/()&\[\]{},#%:|^]": "LITERAL",
            r"[\n~`\t; ]+": "ignore"
        }

    class Token:
        def __init__(self, es, value:str):
            es: EngineScript
            self.es: EngineScript = es
            self.value = value

            for pattern, token_type in EngineScript._patterns.items():
                if re.fullmatch(pattern, self.value):
                    self.type = token_type
                    break
            
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
    
        def unexpected(self):

            if self.line_start == self.line_end:
                err_disp = self.es.script.split("\n")[self.line_start]
                err_disp += f"\n{' '*self.col_start}{'^'*(min(self.col_end-self.col_start, len(err_disp)-self.col_start))}"
            else:
                err_disp = ""

            return ScriptError(f"Unexpected token at Line {self.line_start+1}, Column {self.col_start+1}: {self.value!r}:\n\n{err_disp}")

        def expected(self, actual, do_quotes=True):
            if self.line_start == self.line_end:
                err_disp = self.es.script.split("\n")[self.line_start]
                err_disp += f"\n{' '*self.col_start}{'^'*(min(self.col_end-self.col_start, len(err_disp)-self.col_start))}"
            else:
                err_disp = ""
            q = "'" if do_quotes else ""
            return FinalScriptError(f"Expected {q}{actual}{q} at Line {self.line_start+1}, Column {self.col_start+1}, got {self.value!r} instead.\n\n{err_disp}")

        def get_location(self):
            return f"Line {self.line_start+1}, Column {self.col_start+1}"
    
    class Macro:
        __slots__ = ["name"]
        def __init__(self, name):
            self.name = name
    
    class MacroFunction:
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
                
            return self.deep_replace(self.code, macros)


        def deep_replace(self, obj:Any, repls:dict):
            if isinstance(obj, EngineScript.Macro):
                if obj.name in repls:
                    return repls[obj.name]
                elif obj.name in self.es.macros:
                    return self.es.macros[obj.name]
                raise FinalScriptError(f"Undefined macro: '{obj.name}' in macro function")
            elif isinstance(obj, dict):
                out = {}
                for k, v in obj.items():
                    out.update({k: self.deep_replace(v, repls)})
                return out
            elif isinstance(obj, list):
                return [self.deep_replace(v, repls) for v in obj]
            else:
                return obj



    def parse(self):

        self.line = 0
        self.col = 0

        tokens = [EngineScript.Token(self, t.group()) for t in re.finditer("(?:"+"|".join(self._patterns.keys())+")", self.script)]

        tokens = [t for t in tokens if t.type not in ["ignore"]]

        # print(tokens)

        self.build(tokens)
        

    def build(self, tokens:list[Token]):
        if tokens:
            try:
                self.compiled_script = self.statements(tokens)
            except EOF:
                self.compiled_script = {}

    def statements(self, tokens:list[Token], ignore_macro:bool=False):
        # print("statements")
        a = []

        while tokens:
            try:
                s = self.statement(tokens, ignore_macro)
                if s is not None:
                    a.append(s)
            except ScriptError as e:
                print("\n".join(e.args))
                print(tokens[0:min(len(tokens), 5)])
                break

        print(f"STATEMENTS: {a}")
        return {
            "functions": a
        }

    def statement(self, tokens:list[Token], ignore_macro:bool=False):
        # print("statement")
        if tokens:
            if tokens[0] == ("WORD", "break"):
                tokens.pop(0)
                return {"function": "engine:control/break"}

            elif tokens[0] == ("WORD", "return"):
                tokens.pop(0)
                try:
                    r = self.expression(tokens, ignore_macro)
                except ScriptError:
                    r = None
                
                return r

            elif tokens[0] == ("WORD", "pass"):
                tokens.pop(0)
                return None

            else:
                tk = tokens.copy()
                try:
                    return self.if_condition(tokens, ignore_macro)
                except ScriptError as e:
                    # print(e)
                    tokens.clear()
                    tokens += tk
                    try:
                        return self.while_loop(tokens, ignore_macro)
                    except ScriptError as e:
                        # print(e)
                        tokens.clear()
                        tokens += tk
                        try:
                            return self.for_loop(tokens, ignore_macro)
                        except ScriptError as e:
                            # print(e)
                            tokens.clear()
                            tokens += tk
                            try:
                                return self.expression(tokens, ignore_macro)
                            except ScriptError as e:
                                # print(e)
                                raise tokens[0].unexpected()
        else:
            raise EOF()

    def expression(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("expression")
        if tokens:
            tk = tokens.copy()
            try:
                return self.andor(tokens, ignore_macro)
            except ScriptError as e:
                tokens.clear()
                tokens += tk
                raise e

        else:
            raise EOF()

    def andor(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("andor")
        
        if tokens:
            a = self.comp(tokens, ignore_macro)
            
            if tokens[0] == ("KEYWORD", ("and", "or")):
                t = tokens.pop(0)
                
                try:
                    a2 = self.andor(tokens, ignore_macro)
                    
                    if a.get("function", None) == "engine:logic/compare":
                        a.pop("function")
                    if a2.get("function", None) == "engine:logic/compare":
                        a2.pop("function")
                        
                    return {t.value: [a, a2]}
                    
                except ScriptError as e:
                    raise FinalScriptError(*e.args)
            return a
        else:
            raise EOF()
        
        
    def comp(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("comp")
        if tokens:
            if tokens[0] == ("LITERAL", "not"):
                tokens.pop(0)

                # tk = tokens.copy()
                c = self.comp(tokens, ignore_macro)

                if c.get("function", None) == "engine:logic/compare":
                    c.pop("function")
                return {
                    "function": "engine:logic/compare",
                    "not": c
                }

            else:
                tk = tokens.copy()
                try:
                    a = self.arith(tokens, ignore_macro)

                    if tokens[0] == ("COMP", ("<=", "<", ">", ">=", "==", "!=")):
                        t = tokens.pop(0)

                        try:
                            a2 = self.arith(tokens, ignore_macro)
                            
                            if isinstance(a, dict):
                                if a.get("function", None) == "engine:logic/compare":
                                    a.pop("function")
                            if isinstance(a2, dict):
                                if a2.get("function", None) == "engine:logic/compare":
                                    a2.pop("function")
                                
                            return {t.value: [a, a2]}
                            
                            
                        except ScriptError as e:
                            raise FinalScriptError(*e.args, *t.unexpected().args) # the comparison was present, which means there is a syntax error
                        
                    
                    else:
                        return a

                except ScriptError as e:
                    tokens.clear()
                    tokens += tk
                    raise e
                
        else:
            raise EOF()

    def if_condition(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("if condition")
        if tokens:
            if tokens[0] == ("KEYWORD", "if"):
                tokens.pop(0)

                if tokens:
                    if tokens[0] == ("LITERAL", "("):
                        tokens.pop(0)

                        e = self.expression(tokens, ignore_macro)

                        if tokens:
                            if tokens[0] == ("LITERAL", ")"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected(")")
                        else:
                            raise EOF()

                        if tokens:
                            if tokens[0] == ("LITERAL", "{"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected("{")
                        else:
                            raise EOF()
                        
                        s = self.statements(tokens, ignore_macro)
                        
                        if tokens:
                            if tokens[0] == ("LITERAL", "}"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected("}")
                        else:
                            raise EOF()
                        
                        func = {
                            "@check": e,
                            "true": s
                        }

                        try:
                            e2 = self.elif_branch(tokens, ignore_macro)

                            func.update({"false": e2})

                        except ScriptError as e:
                            pass
                        
                        return func

                    else:
                        raise tokens[0].expected("(")
                else:
                    raise EOF()
            else:
                raise ScriptError("not an if-statement")
        else:
            raise EOF()
    def elif_branch(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("elif")
        if tokens:
            if tokens[0] == ("KEYWORD", "elif"):
                tokens.pop(0)

                if tokens:
                    if tokens[0] == ("LITERAL", "("):
                        tokens.pop(0)

                        e = self.expression(tokens, ignore_macro)

                        if tokens:
                            if tokens[0] == ("LITERAL", ")"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected(")")
                        else:
                            raise EOF()

                        if tokens:
                            if tokens[0] == ("LITERAL", "{"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected("{")
                        else:
                            raise EOF()
                        
                        s = self.statements(tokens, ignore_macro)
                        
                        if tokens:
                            if tokens[0] == ("LITERAL", "}"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected("}")
                        else:
                            raise EOF()
                        
                        func = {
                            "@check": e,
                            "true": s
                        }

                        try:
                            e2 = self.elif_branch(tokens, ignore_macro)

                            func.update({"false": e2})

                        except ScriptError as e:
                            raise FinalScriptError(*e.args)
                        
                        return func

                    else:
                        raise tokens[0].expected("(")
                else:
                    raise EOF()
            else:
                return self.else_branch(tokens, ignore_macro)
        else:
            raise EOF()
    def else_branch(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("else")
        if tokens:
            if tokens[0] == ("KEYWORD", "else"):
                tokens.pop(0)

                if tokens:
                    if tokens[0] == ("LITERAL", "{"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("{")
                else:
                    raise EOF()
                
                s = self.statements(tokens, ignore_macro)
                
                if tokens:
                    print(f"ELSE TOKENS: {tokens}")
                    if tokens[0] == ("LITERAL", "}"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("}")
                else:
                    raise EOF()
                
                return s

                    
            else:
                raise tokens[0].unexpected()
        else:
            raise EOF()
    def while_loop(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            if tokens[0] == ("KEYWORD", "while"):
                tokens.pop(0)
                
                if tokens:
                    if tokens[0] == ("LITERAL", "("):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("(")
                else:
                    raise EOF()
                
                e = self.expression(tokens, ignore_macro)
                
                if tokens:
                    if tokens[0] == ("LITERAL", ")"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected(")")
                else:
                    raise EOF()

                if tokens:
                    if tokens[0] == ("LITERAL", "{"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("{")
                else:
                    raise EOF()
                
                r = self.statements(tokens, ignore_macro)
                
                if tokens:
                    if tokens[0] == ("LITERAL", "}"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("}")
                else:
                    raise EOF()
                
                return {
                    "function": "engine:control/while",
                    "condition": e,
                    "run": r
                }

            else:
                raise ScriptError()
                
        else:
            raise EOF()
    def for_loop(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            if tokens[0] == ("KEYWORD", "for"):
                tokens.pop(0)
                
                if tokens:
                    if tokens[0].type == "VARIABLE":
                        v = tokens.pop(0).value[1:-1]
                    else:
                        raise tokens[0].expected("variable", False)
                else:
                    raise EOF()
                
                if tokens:
                    if tokens[0] == ("LITERAL", ","): # dictionary for-loop?
                        tokens.pop(0)
                        
                        if tokens:
                            if tokens[0].type == "VARIABLE":
                                v2 = tokens.pop(0).value[1:-1]
                            else:
                                raise tokens[0].expected("variable", False)
                        else:
                            raise EOF()
                        
                        if tokens:
                            if tokens[0] == ("KEYWORD", "in"):
                                tokens.pop(0)
                                
                                d = self.expression(tokens, ignore_macro)
                                
                                if tokens:
                                    if tokens[0] == ("LITERAL", "{"):
                                        tokens.pop(0)
                                    else:
                                        raise tokens[0].expected("{")
                                else:
                                    raise EOF()
                                
                                r = self.statements(tokens, ignore_macro)
                                
                                if tokens:
                                    if tokens[0] == ("LITERAL", "}"):
                                        tokens.pop(0)
                                    else:
                                        raise tokens[0].expected("}")
                                else:
                                    raise EOF()
                                
                                return {
                                    "function": "engine:dict/for_each",
                                    "key_name": v,
                                    "value_name": v2,
                                    "dict": d,
                                    "run": r
                                }
                                
                                
                            else:
                                raise tokens[0].expected("in")
                        else:
                            raise EOF()
                        
                    elif tokens[0] == ("KEYWORD", "in"): # list for-loop
                        tokens.pop(0)
                        
                        l = self.expression(tokens, ignore_macro)
                        
                        if tokens:
                            if tokens[0] == ("LITERAL", "{"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected("{")
                        else:
                            raise EOF()
                        
                        r = self.statements(tokens, ignore_macro)
                        
                        if tokens:
                            if tokens[0] == ("LITERAL", "}"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected("}")
                        else:
                            raise EOF()
                        
                        return {
                            "function": "engine:list/for_each",
                            "list": l,
                            "element_name": v,
                            "run": r
                        }
                        
                    else:
                        raise tokens[0].expected("',' or 'in'", False)
                else:
                    raise EOF()
            else:
                raise ScriptError()
        else:
            raise EOF()
    def arith(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("arith")
        if tokens:
            c = self.mult(tokens, ignore_macro)

            if tokens:
                if tokens[0] == ("LITERAL", ("+", "-")):
                    t = tokens.pop(0)
                    try:
                        c2 = self.mult(tokens, ignore_macro)

                        if isinstance(c, dict):
                            if c.get("function", None) == "engine:math/solve":
                                c.pop("function")
                        if isinstance(c2, dict):
                            if c2.get("function", None) == "engine:math/solve":
                                c2.pop("function")
                            
                        return {
                            "function": "engine:math/solve",
                            {"+": "add", "-": "subtract"}[t.value]: [c, c2]
                        }

                    except ScriptError as e:
                        raise FinalScriptError(*e.args)
            return c
        else:
            raise EOF()
        
    def mult(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("mult")
        if tokens:
            c = self.pow(tokens, ignore_macro)

            if tokens:
                if tokens[0] == ("LITERAL", ("*", "/", "%")):
                    t = tokens.pop(0)
                    try:
                        c2 = self.pow(tokens, ignore_macro)

                        if isinstance(c, dict):
                            if c.get("function", None) == "engine:math/solve":
                                c.pop("function")
                        if isinstance(c2, dict):
                            if c2.get("function", None) == "engine:math/solve":
                                c2.pop("function")
                            
                        return {
                            "function": "engine:math/solve",
                            {"*": "multiply", "/": "divide", "%": "mod"}[t.value]: [c, c2]
                        }

                    except ScriptError as e:
                        raise FinalScriptError(*e.args)
            return c
        else:
            raise EOF()

    def pow(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("pow")
        if tokens:
            c = self.concat(tokens, ignore_macro)

            if tokens:
                if tokens[0].type == "POW":
                    tokens.pop(0)
                    try:
                        c2 = self.concat(tokens, ignore_macro)

                        if isinstance(c, dict):
                            if c.get("function", None) == "engine:math/solve":
                                c.pop("function")
                        if isinstance(c2, dict):
                            if c2.get("function", None) == "engine:math/solve":
                                c2.pop("function")
                            
                        return {
                            "function": "engine:math/solve",
                            "pow": [c, c2]
                        }

                    except ScriptError as e:
                        raise FinalScriptError(*e.args)
            return c
        else:
            raise EOF()
        
    def concat(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("concat")
        if tokens:
            a = self.access(tokens, ignore_macro)

            if tokens:
                if tokens[0] == ("CONCAT", ".."):

                    func = {
                        "function": "engine:text/join"
                    }
                    txt = [a]
                    while tokens:
                        if tokens[0] == ("CONCAT", ".."):
                            tokens.pop(0)
                            c = self.access(tokens, ignore_macro)
                            txt.append(c)
                        elif tokens[0] == ("CONCAT", "::"):
                            tokens.pop(0)
                            c = self.access(tokens, ignore_macro)
                            func.update({
                                "text": txt,
                                "seperator": c
                            })
                            return func
                        else:
                            break
                    func.update({"text": txt})
                    return func
            return a

        else:
            raise EOF()
    def access(self, tokens:list[Token], ignore_macro:bool=False) -> dict|int|float|bool|None:
        # print("access")
        if tokens:
            a = self.atom(tokens, ignore_macro)

            if isinstance(a, dict):

                tk = tokens.copy()
                try:
                    l = self.key_list(tokens, ignore_macro)

                    if l:
                        return {
                            "function": "engine:dict/access",
                            "dict": a,
                            "keys": l
                        }
                    # return a
                
                except ScriptError as e:
                    tokens.clear()
                    tokens += tk
                    raise e
            return a
        else:
            raise EOF()

    def key_list(self, tokens:list[Token], ignore_macro:bool=False) -> list:
        # print("key_list")
        if tokens:
            lst = []
            while tokens:
                if tokens[0] == ("LITERAL", "["):
                    tokens.pop(0)

                    e = self.expression(tokens, ignore_macro)

                    if tokens:
                        if tokens[0] == ("LITERAL", "]"):
                            tokens.pop(0)
                        else:
                            raise tokens[0].expected("]")
                    else:
                        raise EOF()

                    lst.append(e)
                else:
                    break
            return lst
        else:
            return []
    
    def atom(self, tokens:list[Token], ignore_macro:bool=False) -> Any:
        # print("atom")
        if tokens:
            if tokens[0].type == "VARIABLE":
                var_name = tokens.pop(0).value[1:-1]
                if tokens:
                    if tokens[0] == ("LITERAL", "="):
                        tokens.pop(0)

                        e = self.expression(tokens, ignore_macro)

                        return {"#store": {var_name: e}}

                    else:
                        return {"#ref": var_name}
                else:
                    raise EOF()
            elif tokens[0] == ("LITERAL", "-"):
                tokens.pop(0)
                a = self.atom(tokens, ignore_macro)
                
                if isinstance(a, dict):
                    if a.get("function", None) == "engine:math/solve":
                        a.pop("function")
                return {
                    "function": "engine:math/solve",
                    "multiply": [-1, a]
                }
                
            elif tokens[0] == ("LITERAL", "("):
                tokens.pop(0)
                a = self.expression(tokens, ignore_macro)
                if tokens:
                    if tokens[0] == ("LITERAL", ")"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected(")")
                else:
                    raise EOF()
                return a
                    
            elif tokens[0].type == "NUMBER":
                return tokens.pop(0).value
            elif tokens[0].type == "BOOLEAN":
                return True if tokens.pop(0).value == "true" else False
            elif tokens[0].type == "STRING":
                return tokens.pop(0).value
            elif tokens[0] == ("KEYWORD", "none"):
                return None
            elif tokens[0] == ("LITERAL", "%"):
                return self.table(tokens, ignore_macro)
            elif tokens[0] == ("LITERAL", "{"):
                tokens.pop(0)
                tk = tokens.copy()
                try:
                    a = self.statements(tokens, ignore_macro)

                except ScriptError as e:
                    tokens.clear()
                    tokens += tk
                    raise e
                
                if tokens:
                    if tokens[0] == ("LITERAL", "}"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("}")
                else:
                    raise EOF()

                return a
                
            elif tokens[0].type == "MACRO":
                return self.macro(tokens, ignore_macro)
            elif tokens[0].type == "WORD":
                return self.function_call(tokens, ignore_macro)
            elif tokens[0].type == "FUNCTION":
                return self.function_call(tokens, ignore_macro)
            else:
                raise tokens[0].unexpected()
        else:
            raise EOF()
    def comma_expressions(self, tokens:list[Token], ignore_macro:bool=False) -> list:

        if tokens:
            e = [self.expression(tokens, ignore_macro)]

            while tokens:
                if tokens[0] == ("LITERAL", ","):
                    tokens.pop(0)
                else:
                    return e
                
                e.append(self.expression(tokens, ignore_macro))
            

        else:
            raise EOF()

    def table(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            if tokens[0] == ("LITERAL", "%"):
                tokens.pop(0)
                print("\n\nmay be table\n\n")
                if tokens:
                    if tokens[0] == ("LITERAL", "["):
                        tokens.pop(0)
                        
                        l = self.comma_expressions(tokens, ignore_macro)
                        
                        if tokens:
                            if tokens[0] == ("LITERAL", "]"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected("]")
                        else:
                            raise EOF()
                        
                        return l
                        
                    elif tokens[0] == ("LITERAL", "{"):
                        tokens.pop(0)
                        
                        l = self.table_contents(tokens, ignore_macro)
                        
                        if tokens:
                            if tokens[0] == ("LITERAL", "}"):
                                tokens.pop(0)
                            else:
                                raise tokens[0].expected("}")
                        else:
                            raise EOF()

                        return l
                        
                    else:
                        raise tokens[0].expected("'{' or '['", False)
                else:
                    raise EOF()
                        
        else:
            raise EOF()

    shorthand = {
        "output": "[engine:player/message]",
        "combat_output": "[engine:combat/message]",
        "wait": "[engine:time/wait]",
        "format": "[engine:text/format]",
        "input": "[engine:player/get_input]",
        "length": "[engine:text/length]",
        "interact": "[engine:interaction/interact]",
        "match": "[engine:text/match]",
        "join": "[engine:text/join]"
    }

    def function_call(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        # print("function call")
        if tokens:
            if tokens[0].type == "WORD":
                func = self.shorthand.get(tokens[0].value, None)
                tokens.pop(0)
                if func is None:
                    raise FinalScriptError(f"No function short-hand for '{func}' defined")
            elif tokens[0].type == "FUNCTION":
                func = tokens[0].value
                tokens.pop(0)
            else:
                raise tokens[0].unexpected()
            
            p = [None, func]

            if tokens:
                if tokens[0] == ("LITERAL", "("):
                    p2 = self.parameters(tokens, ignore_macro)
                else:
                    return self.validate_function(p)
            else: raise EOF()

            p.append(p2)

            if tokens:
                if tokens[0] == ("LITERAL", "{"):
                    tokens.pop(0)
                    p3 = self.statements(tokens, ignore_macro)

                    if tokens:
                        if tokens[0] == ("LITERAL", "}"):
                            tokens.pop(0)
                        else:
                            raise tokens[0].expected("}")
                    else: raise EOF()
                
                elif tokens[0].type == "TAG":
                    p3 = self.tag_list(tokens)
                else:
                    return self.validate_function(p)
            else: raise EOF()

            p.append(p3)
            return self.validate_function(p)


        else:
            raise EOF()

    def validate_function(self, p:list):
        func: LoaderFunction = LoaderFunction.getFunction(Identifier.fromString(p[1][1:-1]))

        if func is None:
            raise FinalScriptError(f"function '{p[1][1:-1]}' is not defined")

        f_required = func.script_flags.get("required_args", 0)
        f_optional = func.script_flags.get("optional_args", 0)
        f_args = func.script_flags.get("args", {})
        if len(p) >= 3:
            params = p[2]
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
                case "required parameter"|"required_parameter"|"rp"|"required paramater"|"required_paramater":
                    parameters["args"].update({arg_name: ...})
                case "*parameters"|"*params"|"*paramaters"|"*":
                    parameters["*args"].update({arg_name: []})
                    args_name = arg_name
                case "optional parameter"|"optional parameter"|"op"|"optional_parameter"|"optional_paramater":
                    parameters["kwargs"].update({arg_name: ...})
                case "**parameters"|"**paramaters"|"**params"|"**":
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
                    elif name in parameters["*args"]: raise FinalScriptError(f"Cannot assign to starred parameter by identifer")
                    else:
                        if any(v is ... for v in parameters["args"].values()): raise FinalScriptError(f"not enough args passed to function '{func.id.full()}'")
                        else:
                            if name in parameters["kwargs"]: parameters["kwargs"][name] = value
                            else:
                                state = "**kwargs"
                                if kwargs_name: parameters["**kwargs"][kwargs_name].update({name: value})
                                else: raise FinalScriptError(f"function '{func.id.full()}' does not accept **kwargs")
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
                                
                    if not found: raise FinalScriptError(f"too many args passed to function '{func.id.full()}'")
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
                    elif name in parameters["*args"]: raise FinalScriptError(f"Cannot assign to starred parameter by identifer")
                    else:
                        if any(v is ... for v in parameters["args"].values()): raise FinalScriptError(f"not enough args passed to function '{func.id.full()}'")
                        else:
                            if name in parameters["kwargs"]: parameters["kwargs"][name] = value
                            else:
                                state = "**kwargs"
                                if kwargs_name: parameters["**kwargs"][kwargs_name].update({name: value})
                                else: raise FinalScriptError(f"function '{func.id.full()}' does not accept **kwargs")
                else:
                    if args_name: parameters["*args"][args_name].append(value)
                    else:
                        state = "kwargs"
                        for n, v in parameters["kwargs"].items():
                            if v is ...:
                                parameters["kwargs"][n] = value
                                break
                        else: raise FinalScriptError(f"too many args passed to function '{func.id.full()}'")
            elif state == "kwargs":
                if name:
                    state = "kwargs"
                    if name in parameters["args"]: parameters["args"][name] = value
                    elif name in parameters["*args"]: raise FinalScriptError(f"Cannot assign to starred parameter by identifer")
                    else:
                        if any(v is ... for v in parameters["args"].values()): raise FinalScriptError(f"not enough args passed to function '{func.id.full()}'")
                        else:
                            if name in parameters["kwargs"]: parameters["kwargs"][name] = value
                            else:
                                state = "**kwargs"
                                if kwargs_name: parameters["**kwargs"][kwargs_name].update({name: value})
                                else: raise FinalScriptError(f"function '{func.id.full()}' does not accept **kwargs")
                else: raise FinalScriptError(f"cannot put positional arg after key word arg")
            else: # if state == "**kwargs":
                if name:
                    if kwargs_name: parameters["**kwargs"][kwargs_name].update({name: value})
                    else: raise FinalScriptError(f"function '{func.id.full()}' does not accept **kwargs")
                else: raise FinalScriptError(f"cannot put positional arg after key word arg")
        
        if func.id.full() != "engine:control/check_predicate":
            data = {
                "function": func.id.full()
            }
        else:
            data = {}
        if len(p) == 4:
            d = p[3]
            if isinstance(d, dict): # scope
                print(parameters, d)
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

        return data

    def table_contents(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            table = {}
            
            while tokens:
                if tokens[0].type in ("STRING", "NUMBER", "BOOLEAN"):
                    key = tokens.pop(0).value
                else:
                    raise tokens[0].expected("string, number, or boolean", False)
                
                if tokens:
                    if tokens[0] == ("LITERAL", ":"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected(":")
                else:
                    raise EOF()
                
                val = self.expression(tokens, ignore_macro)
                
                table.update({key: val})
                
                if tokens:
                    if tokens[0] == ("LITERAL", ","):
                        tokens.pop(0)
                    elif tokens[0] == ("LITERAL", "}"):
                        return table
                    else:
                        raise tokens[0].expected("',' or '}'", False)
                else:
                    raise EOF()
                
        else:
            raise EOF()
        
    def parameters(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            if tokens[0] == ("LITERAL", "("):
                tokens.pop(0)
            else:
                raise tokens[0].expected("(")
            p = self.param_element(tokens, ignore_macro=ignore_macro)

            if tokens:
                if tokens[0] == ("LITERAL", ")"):
                    tokens.pop(0)
                    return p
                else:
                    raise tokens[0].expected(")")
            else:
                raise EOF()

        else:
            raise EOF()

    def param_element_2(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            if tokens[0].type == "WORD":
                w = tokens.pop(0)

                if tokens:
                    if tokens[0] == ("LITERAL", "="):
                        tokens.pop(0)
                    else:
                        tokens.insert(0, w)
                        return self.param_element(tokens, True, ignore_macro)
                        
            
                e = self.expression(tokens, ignore_macro)

                if tokens:
                    if tokens[0] == ("LITERAL", ","):
                        tokens.pop(0)

                        try:
                            x = self.param_element(tokens, ignore_macro=ignore_macro)
                        except ScriptError as e:
                            return [(w.value, e)]

                        return [(w.value, e)] + x
                    else:
                        return [(w.value, e)]
                else:
                    raise EOF()

        else:
            raise EOF()

    def param_element(self, tokens:list[Token], ignore_word=False, ignore_macro:bool=False) -> dict:

        if tokens:
            if tokens[0].type == "WORD" and not ignore_word:
                return self.param_element_2(tokens, ignore_macro)
            else:
                e = self.expression(tokens, ignore_macro)

                if tokens:
                    if tokens[0] == ("LITERAL", ","):
                        tokens.pop(0)

                        try:
                            x = self.param_element(tokens, ignore_macro=ignore_macro)
                        except ScriptError as e:
                            return [(None, e)]

                        return [(None, e)] + x
                    else:
                        return [(None, e)]
                else:
                    raise EOF()

        else:
            raise EOF()

    def tag(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            if tokens[0].type == "TAG":
                tag = tokens.pop(0).value

                e = self.expression(tokens, ignore_macro)

                if tokens:
                    if tokens[0] == ("LITERAL", "#"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("#")
                else:
                    raise EOF()
                
                if tokens:
                    if tokens[0] == ("LITERAL", "{"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("{")
                else:
                    raise EOF()

                s = self.statements(tokens, ignore_macro)

                if tokens:
                    print(tokens)
                    if tokens[0] == ("LITERAL", "}"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected("}")
                else:
                    raise EOF()

                return {tag: e, "scope": s}

            else:
                pass

        else:
            raise EOF()
    def tag_list(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            data = {}

            while tokens:
                if tokens[0].type == "TAG":
                    t = self.tag(tokens, ignore_macro)
                    data.update(t)
                else:
                    break
            return data

        else:
            raise EOF()
    
    def macro(self, tokens:list[Token], ignore_macro:bool=False) -> dict:
        if tokens:
            if tokens[0].type == "MACRO":
                macro = tokens.pop(0)
                macro_name = macro.value
                
                if tokens[0] == ("LITERAL", "("): # def/call
                    tokens.pop(0)
                    
                    # print(f"macro def? tokens: {tokens}")
                    if tokens:
                        if tokens[0] == ("LITERAL", ")"):
                            raise FinalScriptError(f"Macro functions must have at least one arg. Otherwise, use an expression macro instead of a function macro.\n'{macro_name}' at {macro.get_location()}")
                        elif tokens[0].type == "MACRO": # def
                            if macro_name in self.macro_functions:
                                raise FinalScriptError(f"Macro function '{macro_name}' at {macro.get_location()} is already defined")
                    
                            ms = []
                            
                            while tokens:
                                if tokens[0].type == "MACRO":
                                    ms.append(tokens.pop(0).value)
                                    if tokens:
                                        if tokens[0] == ("LITERAL", ")"):
                                            tokens.pop(0)
                                            break
                                        elif tokens[0] == ("LITERAL", ","):
                                            tokens.pop(0)
                                    else:
                                        raise EOF()
                                else:
                                    raise tokens[0].expected("macro argument", False)
                            


                            if tokens:
                                if tokens[0] == ("LITERAL", "{"):
                                    tokens.pop(0)
                                else:
                                    raise tokens[0].expected("{")
                            else:
                                raise EOF()
                            
                            s = self.statements(tokens, True)
                            
                            if tokens:
                                if tokens[0] == ("LITERAL", "}"):
                                    tokens.pop(0)
                                else:
                                    raise tokens[0].expected("}")
                            else:
                                raise EOF()
                            
                            self.macro_functions.update({macro_name: EngineScript.MacroFunction(self, macro_name, ms, s)})
                            return None
                            
                        else: # call
                            if macro_name not in self.macro_functions:
                                raise FinalScriptError(f"Macro function is not defined: '{macro_name}' at {macro.get_location()}")
                    
                            es = self.comma_expressions(tokens)

                            if tokens:
                                if tokens[0] == ("LITERAL", ")"):
                                    tokens.pop(0)
                                else:
                                    raise tokens[0].expected(")")
                            else:
                                raise EOF()
                            
                            return self.macro_functions[macro_name].compile(es, macro)
                            
                    else:
                        raise EOF()
                    
                elif tokens[0] == ("LITERAL", "="): # assign
                    if ignore_macro:
                        raise FinalScriptError(f"Cannot define a macro within a macro function! at {macro.get_location()}")
                    
                    tokens.pop(0)
                    
                    e = self.expression(tokens)
                    
                    self.macros.update({macro_name: e})
                    return None
                    
                else: # ref
                    if ignore_macro:
                        return EngineScript.Macro(macro_name)
                    if macro_name in self.macros:
                        return self.macros[macro_name]
                    raise FinalScriptError(f"Undefined macro '{macro_name}' at {macro.get_location()}")
                    
                
            else:
                raise tokens[0].unexpected()
        else:
            raise EOF()

    def getScript(self):
        if not self.compiled_script:
            self.compile()
        return self.compiled_script


    @classmethod
    def unload(cls):
        cls._scripts.clear()
        cls.script_files.clear()



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

            # try:
                engine_script = EngineScript(input("file > "))
                engine_script.compile()

                print(json.dumps(engine_script.getScript(), indent=4, default=str))
            # except Exception as e:
            #     print("\n".join(e.args))


