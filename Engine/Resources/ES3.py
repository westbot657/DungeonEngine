# pylint: disable=W,R,C,import-error


from .EngineErrors import ScriptError, FinalScriptError, EOF
from .Serializer import Serializer

from typing import Any

import re

"""
#!enter-script // emberhollow/scripts/rooms/boats/spawn_boat

num_players = length(#dungeon.player_ids)

#dungeon.player_ids.append(#player.uid)

#player: @listening = true

$listening = #player: @listening

output("say `skip` to skeip dialog")

captain = random.choice([
    "...",
    "..."
])

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


#player.goto(<emberhollow:rooms/docks/roads/road_4>)


"""


class EngineScript:
    _scripts = {}
    
    _patterns = {
        r"\/\/.*": "ignore",
        r"(?<!\/)\/\*(\*[^/]|[^*])+\*\/": "ignore",
        "\\#\\![^\n;]*;?": "context_hint",
        r"(\"(\\.|[^\"\\])*\"|\'(\\.|[^\'\\])*\')": "STRING",
        r"@[^ ]*": "TAG",
        r"\$[a-zA-Z_][a-zA-Z0-9_]*": "MACRO",
        r"\b(true|false)\b": "BOOLEAN",
        r"\<[^<> ]+\>": "VARIABLE",
        r"(<=|>=|<|>|==|!=)": "COMP",
        r"(\.\.|::)": "CONCAT",
        r"\b(if|elif|else|while|for|in|and|not|or|true|false|none)\b": "KEYWORD",
        r"[a-zA-Z_][a-zA-Z0-9_]*": "WORD",
        r"(\d+(\.\d+)?|\.\d+)": "NUMBER",
        r"\*\*": "POW",
        r"[=\-+*/()&\[\]{},#%:|^\.]": "LITERAL",
        r"[\n~`\t; ]+": "ignore"
    }

    class Token:
        def __init__(self, es, value:str):
            self.es = es
            self.value = value
            
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
        __slots__ = ["name", "token"]
        def __init__(self, name, token=None):
            self.name = name
            self.token = token
    
    
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
        self.variable_table = {}
        
        
    def compile(self):
        self.macro_functions.clear()
        self.macros.clear()
        
        self.parse()
    
    def parse(self):
        
        self.line = 0
        self.col = 0
        
        tokens = [EngineScript.Token(self, t.group()) for t in re.finditer("(?:"+"|".join(self._patterns.keys())+")", self.script)]

        tokens = [t for t in tokens if t.type not in ["ignore", "context_hint"]]

        self.build(tokens)
    
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
    
    def build(self, tokens):
        t = bool(tokens)
        if tokens:
            try:
                self.compiled_script = self.cleanup(self.statements(tokens))
            except EOF:
                self.compiled_script = {}
        if t and self.compiled_script == {}:
            print(f"Warning:\n    File '{self.script_file}' contained code that compiled to nothing.")

    def statements(self, tokens:list[Token], ignore_macros:bool=False):
        ...
        
