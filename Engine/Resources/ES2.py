# pylint: disable=[W,R,C]

# This is attampt 2 at a Engine Script parser but with syntax error position finding

try:
    from .LoaderFunction import LoaderFunction
    from .Functions import *
    from .Identifier import Identifier
    from .Logger import Log
    from .EngineErrors import ScriptError, EOF
except ImportError:
    from LoaderFunction import LoaderFunction
    from Functions import *
    from Identifier import Identifier
    from Logger import Log
    from EngineErrors import ScriptError, EOF

import re, glob, json




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
        self.macros = {}
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

        self.macros.clear()


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
            r"[a-zA-Z_][a-zA-Z0-9_]*": "WORD",
            r"(\d+(\.\d+)?|\.\d+)": "NUMBER",
            r"[=\-+*/()&\[\]{},#%:|^]": "LITERAL",
            r"[\n~`\t; ]+": "ignore"
        }

    class Token:
        def __init__(self, es, value:str):
            es: EngineScript
            self.value = value

            for pattern, token_type in EngineScript._patterns:
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
                return self.type == other[0] and self.value == other[1]

        def __str__(self):
            if self.line_start == self.line_end:
                return f"'{self.value}' (Line {self.line_start}, Column {self.col_start} to {self.col_end})"
            else:
                return f"'{self.value}' (Line {self.line_start}, Column {self.col_start} to Line {self.line_end}, Column {self.col_end})"

        def __repr__(self):
            return f"{self.type}: {self!s}"

    def parse(self):

        tokens = [EngineScript.Token(self, t) for t in re.finditer("(?:"+"|".join(self._patterns.keys())+")", self.script)]

        tokens = [t for t in tokens if t.type not in ["ignore"]]

        self.build(tokens)

    def build(self, tokens:list):
        if tokens:
            try:
                self.compiled_script = self.expressions(tokens)
            except EOF:
                self.compiled_script = {}

    def expressions(self, tokens:list):

        a = {
            "functions": self.statement(tokens)["functions"]
        }

        try:
            b = self.expressions(tokens)
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
                except:
                    r = None
                
                return r

            else:
                try:
                    return self.expression(tokens)
                except:
                    try:
                        return self.if_condition(tokens)
                    except:
                        try:
                            return self.while_loop(tokens)
                        except: pass
        else:
            raise EOF()

    def expression(self, tokens:list):
        # comp, MACRO = expression, MACRO, PASS
        if tokens:
            if tokens[0] == ("WORD", "pass"):
                return None
            elif tokens[0].type == "MACRO":
                tok = tokens.pop(0)
                if tokens[0] == ("LITERAL", "="):
                    tokens.pop(0)
                    self.macros.update({tok.value: self.statement(tokens)})
                else:
                    if tok.value in self.macros:
                        return self.macros[tok.value]
                    raise ScriptError(f"Undefined macro: {tok!s}")
            else:
                tk = tokens.copy()
                try:
                    return self.comp(tokens)
                except ScriptError:
                    tokens.clear()
                    tokens += tk
                    raise

        else:
            raise EOF()

    def comp(self, tokens): pass
    def if_condition(self, tokens): pass
    def while_loop(self, tokens): pass


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

            try:
                engine_script = EngineScript(input("file > "))
                engine_script.compile()

                print(json.dumps(engine_script.getScript(), indent=4, default=str))
            except Exception as e:
                print(e)


