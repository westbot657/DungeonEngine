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

        EngineScript.Macro.clear_macros()

        self.parse()

    _patterns = {
            r"\/\/.*": "ignore",
            r"(?<!\/)\/\*(\*[^/]|[^*])+\*\/": "ignore",
            r"\[([^:\[]+:)(([^\/\]\[]+\/)*)([^\[\]]+)\]": "FUNCTION",
            r"@[^\:]+\:": "TAG",
            r"\$[a-zA-Z_][a-zA-Z0-9_]*": "MACRO",
            r"(true|false)": "BOOLEAN",
            r"(\"(\\.|[^\"\\])*\"|\'(\\.|[^\'\\])*\')": "STRING",
            r"\<[^<> ]+\>": "VARIABLE",
            r"(<=|>=|<|>|==|!=)": "COMP",
            r"(if|elif|else|while|for|in|and|not|or|true|false|none)": "KEYWORD",
            r"[a-zA-Z_][a-zA-Z0-9_]*": "WORD",
            r"(\d+(\.\d+)?|\.\d+)": "NUMBER",
            r"[=\-+*/()&\[\]{},#%:|^]": "LITERAL",
            r"[\n~`\t; ]+": "ignore"
        }

    class Macro:
        _macro_mapping = {}
        _macros = []
        
        def __init__(self, name:str, tree_ref:dict):
            self.name = name
            self.tree_ref = tree_ref
            
            EngineScript.Macro._macros.append(self)
            
        def new_macro(self, name, value):
            self._macro_mapping.update({name: value})
            
        def evaluate(self, value):
            self.tree_ref.update({self.name: value})

        @classmethod
        def clear_macros(cls):
            cls._macros.clear()



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
                return self.type == other[0] and (self.value in other[1] if isinstance(other[1], (tuple, list)) else self.value == other[1])

        def __str__(self):
            if self.line_start == self.line_end:
                return f"'{self.value}' (Line {self.line_start}, Column {self.col_start} to {self.col_end})"
            else:
                return f"'{self.value}' (Line {self.line_start}, Column {self.col_start} to Line {self.line_end}, Column {self.col_end})"

        def __repr__(self):
            return f"{self.type}: {self!s}"
    
        def unexpected(self):

            if self.line_start == self.line_end:
                err_disp = self.es.script.split("\n")[self.line_start]
                err_disp += f"\n{' ':> {self.col_start}}{'^'*(min(self.col_end-self.col_start, len(err_disp)-self.col_start))}"
            else:
                err_disp = ""

            return ScriptError(f"Unexpected token at Line {self.line_start}, Column {self.col_start}: {self.value!r}:\n\n{err_disp}")

        def expected(self, actual):
            if self.line_start == self.line_end:
                err_disp = self.es.script.split("\n")[self.line_start]
                err_disp += f"\n{' ':> {self.col_start}}{'^'*(min(self.col_end-self.col_start, len(err_disp)-self.col_start))}"
            else:
                err_disp = ""
            
            return ScriptError(f"Expected '{actual}' at Line {self.line_start}, Column {self.col_start}, got {self.value!r} instead.\n\n{err_disp}")

    def parse(self):

        tokens = [EngineScript.Token(self, t.group()) for t in re.finditer("(?:"+"|".join(self._patterns.keys())+")", self.script)]

        tokens = [t for t in tokens if t.type not in ["ignore"]]

        print(tokens)

        self.build(tokens)

    def build(self, tokens:list):
        if tokens:
            try:
                self.compiled_script = self.statements(tokens)
            except EOF:
                self.compiled_script = {}

    def statements(self, tokens:list):

        a = {
            "functions": self.statement(tokens)["functions"]
        }

        try:
            b = self.statements(tokens)
        except EOF:
            b = None

        if b:
            a["functions"] += b["functions"]

        return a

    def statement(self, tokens:list):
        if tokens:
            if tokens[0] == ("WORD", "break"):
                tokens.pop(0)
                return {"function": "engine:control/break"}

            elif tokens[0] == ("WORD", "return"):
                tokens.pop(0)
                try:
                    r = self.expression(tokens)
                except ScriptError:
                    r = None
                
                return r

            elif tokens[0] == ("WORD", "pass"):
                tokens.pop(0)
                return None

            else:
                try:
                    return self.if_condition(tokens)
                except:
                    try:
                        return self.while_loop(tokens)
                    except:
                        try:
                            return self.for_loop(tokens)
                        except:
                            try:
                                return self.expression(tokens)
                            except: pass
        else:
            raise EOF()

    def expression(self, tokens:list[Token]) -> dict:
        # comp, MACRO = expression, MACRO, PASS
        if tokens:
            tk = tokens.copy()
            try:
                return self.andor(tokens)
            except ScriptError as e:
                tokens.clear()
                tokens += tk
                raise e

        else:
            raise EOF()

    def andor(self, tokens:list[Token]) -> dict:
        
        if tokens:
            a = self.comp(tokens)
            
            if tokens[0] == ("KEYWORD", ("and", "or")):
                t = tokens.pop(0)
                
                try:
                    a2 = self.andor(tokens)
                    
                    if a.get("function", None) == "engine:logic/compare":
                        a.pop("function")
                    if a2.get("function", None) == "engine:logic/compare":
                        a2.pop("function")
                        
                    return {t.value: [a, a2]}
                    
                except ScriptError as e:
                    raise FinalScriptError(*e.args)
            
        else:
            raise EOF()
        
        
    def comp(self, tokens:list[Token]) -> dict:
        if tokens:
            if tokens[0] == ("LITERAL", "not"):
                tokens.pop(0)

                # tk = tokens.copy()
                c = self.comp(tokens)

                if c.get("function", None) == "engine:logic/compare":
                    c.pop("function")
                return {
                    "function": "engine:logic/compare",
                    "not": c
                }

            else:
                tk = tokens.copy()
                try:
                    a = self.arith(tokens)

                    if tokens[0] == ("COMP", ("<=", "<", ">", ">=", "==", "!=")):
                        t = tokens.pop(0)

                        try:
                            a2 = self.arith(tokens)
                            
                            if a.get("function", None) == "engine:logic/compare":
                                a.pop("function")
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
    def if_condition(self, tokens) -> dict: pass
    def elif_branch(self, tokens) -> dict: pass
    def else_branch(self, tokens) -> dict: pass
    def while_loop(self, tokens) -> dict: pass
    def for_loop(self, tokens) -> dict: pass
    def arith(self, tokens) -> dict: pass
    def mult(self, tokens) -> dict: pass
    def pow(self, tokens) -> dict: pass
    def concat(self, tokens) -> dict: pass
    def access(self, tokens) -> dict: pass
    def atom(self, tokens:list[Token]) -> Any:
        if tokens:
            if tokens[0].type == "VARIABLE":
                var_name = tokens.pop(0).value[1:-1]
                if tokens:
                    if tokens[0] == ("LITERAL", "="):
                        tokens.pop(0)
                        
            elif tokens[0] == ("LITERAL", "-"):
                tokens.pop(0)
                a = self.atom(tokens)
                
                if isinstance(a, dict):
                    if a.get("function", None) == "engine:math/solve":
                        a.pop("function")
                return {
                    "function": "engine:math/solve",
                    "multiply": [-1, a]
                }
                
            elif tokens[0] == ("LITERAL", "("):
                tokens.pop(0)
                a = self.expression(tokens)
                if tokens:
                    if tokens[0] == ("LITERAL", ")"):
                        tokens.pop(0)
                    else:
                        raise tokens[0].expected(")")
                else:
                    raise EOF()
                    
            elif tokens[0].type == "NUMBER":
                ...
            elif tokens[0].type == "BOOLEAN":
                ...
            elif tokens[0].type == "STRING":
                ...
            elif tokens[0] == ("LITERAL", "%"):
                ... # table
            elif tokens[0] == ("LITERAL", "{"):
                ... # scope
            elif tokens[0].type == "MACRO":
                ... # macro
            elif tokens[0].type == "WORD":
                ... # short-hand function
            elif tokens[0].type == "FUNCTION":
                ... # function
            else:
                raise tokens[0].unexpected()
        else:
            raise EOF()
    def comma_expressions(self, tokens) -> dict: pass
    def table(self, tokens) -> dict: pass
    def scope(self, tokens) -> dict: pass
    def function_call(self, tokens) -> dict: pass
    def table_contents(self, tokens) -> dict: pass
    def parameters(self, tokens) -> dict: pass
    def param_element(self, tokens) -> dict: pass
    def tag(self, tokens) -> dict: pass
    def tag_list(self, tokens) -> dict: pass
    
    def macro(self, tokens) -> dict: pass
    def macro_args(self, tokens) -> dict: pass
    def macro_scope(self, tokens) -> dict: pass
    
    def table_accessor(self, tokens) -> dict:
        # accessor: <dict>[key1][key2]...
        pass




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


