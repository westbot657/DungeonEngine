# pylint: disable=W,R,C,import-error,assignment-from-no-return,undefined-variable

try:
    from .EngineErrors import ScriptError, FinalScriptError, EOF
    from .Serializer import Serializer
    from .YieldTools import YieldTools
    # from .LoaderFunction import LoaderFunction
    from .ESFunctions import ESFunction, ESClass
    from .ESNodes import *
except ImportError:
    from EngineErrors import ScriptError, FinalScriptError, EOF
    from Serializer import Serializer
    from YieldTools import YieldTools
    from ESFunctions import ESFunction, ESClass
    # from LoaderFunction import LoaderFunction
    from ESNodes import *

from typing import Any

import re
import json

test_script = """
#!emberhollow/rooms/boats/spawn_boat
#!enter-script

num_players = length(#dungeon.player_ids)

#dungeon.player_ids.append(#player.uid)

#player.tag$[listening = true]

$listening = #player.tag$[listening]

output("say `skip` to skip dialog")

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
            format($message, captain: captain)
        )
        wait($wait_time)
    }
}

$outm($message, $wait_time) {
    if ($listening) {
        output(
            format($message, captain: captain, money: starting_money.total)
        )
        wait($wait_time)
    }
}

// ...

match random.choice([1, 2, 3, 4]) {
    case 1 {
        // ...
        $outm("{captain} hands you a bag of coins.\n(+{money})", 2)
    }
}

#player.give_money(starting_money)


move: #player -> <emberhollow:rooms/docks/roads/road_4>


"""

class Type:
    def __init__(self, tp:str, type_set:list|None=None):
        self.tp = tp
        self.type_set = type_set
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        if self.type_set:
            return f"{self.tp}[{"|".join(str(t) for t in self.type_set)}]"
        return self.tp

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
        r"\b(new|move)\b": "COMMAND",
        r"\b(if|elif|else|while|for|in|and|not|or|none|match|case|class|def|break|continue)\b": "KEYWORD",
        r"[a-zA-Z_][a-zA-Z0-9_]*": "WORD",
        r"(\d+(\.\d+)?|\.\d+)": "NUMBER",
        # r"\*\*": "POW",
        r"[=\-+*/()&\[\]{},#%:|^\.\$;~`]": "LITERAL",
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
        
        def remove(self, name:str):
            if name in self.vars:
                return self.vars.pop(name)
        
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
            self.in_macro = False
            
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
            elif self.type == "OBJECT":
                self.value = self.value[1:-1]
            elif self.type == "BOOLEAN":
                self.value = self.value == "true"
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
                return f"'{self.raw}' (Line {self.line_start+1}, Column {self.col_start+1} to {self.col_end+1})"
            else:
                return f"'{self.raw}' (Line {self.line_start+1}, Column {self.col_start+1} to Line {self.line_end+1}, Column {self.col_end+1})"

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
        self.parsing_macro = False
        self.curr_macro_args = []
        self.commands = {
            "new": self.parse_cmd_new,
            "move": self.parse_cmd_move
        }
        
    def get_type_ref_tree(self, value):
        print(f"ES3: get value of {value}")
        
        return self.get_context(value)

    def get_type_from_obj(self, obj):
        print(f"ES3: get type of {obj}")
        
        
    def snapshot(self, tokens):
        return len(tokens)

    def load_snapshot(self, snapshot) -> list[Token]:
        return self._tokens[len(self._tokens)-snapshot:]

    class ExecReturn:
        def __init__(self, type:str, value:Any):
            self.type = type
            self.value = value

    def execute(self):
        yt = YieldTools("ES3:execute")
        yield from yt.call(self._execute, self.compiled_script)
        r = yt.result()
        print(r)
        

    def parse_cmd_new(self, tokens:list[Token]):
        tokens.pop(0)
        if tokens and tokens[0] == ("LITERAL", ":"):
            tokens.pop(0)
            
            if tokens and tokens[0].type == "OBJECT":
                obj = tokens.pop(0)
                
                if tokens and tokens[0] == ("LITERAL", "{"):
                    args = self.call_args(tokens)
                    
                    return NewNode(obj, args)
                
                elif tokens:
                    raise tokens[0].expected("{")
                else:
                    raise FinalScriptError("Unexpected EOF while parsing 'new' command")
                
            elif tokens:
                raise tokens[0].expected("object", False)
            else:
                raise FinalScriptError("Unexpected EOF while parsing 'new' command")
            
        elif tokens:
            raise tokens[0].expected(":")
        else:
            raise FinalScriptError("Unexpected EOF after 'new' command")
    
    def parse_cmd_move(self, tokens:list[Token]):
        tokens.pop(0)
        
        if tokens and tokens[0] == ("LITERAL", ":"):
            tokens.pop(0)
            
            obj = self.atom(tokens)
            
            if len(tokens) >= 2 and tokens[0] == ("LITERAL", "-") and tokens[1] == ("COMP", ">"):
                tokens.pop(0)
                tokens.pop(0)
                
                if tokens and tokens[0].type == "OBJECT":
                    dest = tokens.pop(0)
                    
                    return MoveNode(obj, dest)
                elif tokens:
                    raise tokens[0].expected("object", False)
                else:
                    raise FinalScriptError("Unexpected EOF while parsing 'move' command")
            elif tokens:
                raise tokens[0].expected("->")
            else:
                raise FinalScriptError("Unexpected EOF while parsing 'move' command")
        elif tokens:
            raise tokens[0].expected(":")
        else:
            raise FinalScriptError("Unexpected EOF after 'move' command")
        

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
        
        tokens = [t for t in tokens if t.type not in ["ignore", "context_hint", "NEWLINE"]]
        # print(tokens)
        
        self._tokens = tokens.copy()

        self.build(tokens)
    
    def tokenize(self) -> list[Token]:
        """
        Returns a list of tokens from the script
        """
        return [EngineScript.Token(self, t.group()) for t in re.finditer("(?:"+"|".join(self._patterns.keys())+")", self.script)]
    
    def cleanup(self, ast):
        # print(f"CLEANUP: {ast}")
        if isinstance(ast, dict):
            if "#functions" in ast and ast["#functions"] == []:
                ast.pop("#functions")
            if "true" in ast and ast["true"] in [{"#functions": []}, None]:
                ast.update({"true": {}})
            if "false" in ast and ast["false"] in [{"#functions": []}, None]:
                ast.update({"false": {}})
            # if "#check" in ast and ast["#check"] in [{"#functions": []}, None]:
            #     ast.pop("false")
            #     t = ast.pop("true")
            #     ast.pop("#check")
            #     if t != {}:
            #         ast.update(t)
            out = {}
            for k, v in ast.items():
                x = self.cleanup(v)
                out.update({k: x})
            return out
        elif isinstance(ast, list):
            lst = []
            for l in ast:
                x = self.cleanup(l)
                if not x in [None, {}]:
                    lst.append(x)
            return lst
        return ast
    
    def build(self, tokens:list[Token]):
        t = bool(tokens)
        if tokens:
            try:
                ast: Node = self.statements(tokens)
                print(ast.display())
                
                ast.get_ret_type()
                # for macro, val in self.macros.items():
                #     print(f"\nmacro: {macro} :\n{val.display()}")
                # for macro, val in self.macro_functions.items():
                #     print(f"\nmacro: {macro} :\n{val.display()}")
                self.compiled_script = self.cleanup(ast.compile())
            except EOF:
                self.compiled_script = {}
        if t and self.compiled_script == {}:
            print(f"Warning:\n    File '{self.script_file}' contained code that compiled to nothing.")

    def statements(self, tokens:list[Token]):
        stmts = []
        while tokens and tokens[0] != ("LITERAL", ("}", ")", "]")):
            try:
                stmt = self.statement(tokens)
                if stmt:
                    stmts.append(stmt)
            except EOF as e:
                break
            except ScriptError as e:
                if tokens and tokens[0] == ("LITERAL", "}"):
                    break
        return Statements(stmts)

    def get_context(self, ctx_type:str):
        match ctx_type:
            case "str":
                return {
                    "split": {
                        "type": "function",
                        "function": ESClass.classes["ESString"],
                        "returns": "list[str]"
                    }
                }
            case "boolean":
                return {}
            case "number":
                return {}
            case "Inventory":
                return {}
            case "Location":
                return {}
            case "Currency":
                return {}
            case "StatusEffects":
                return {}
            case "StatusEffect":
                return {}
            case "Position":
                return {}
            case "dungeon":
                return {}
            case _:
                raise Exception(f"forgot to implement context type '{ctx_type}'")

    def add_base_context(self):
        self.variable_table.vars = {
            "#player": {
                "type": "Player",
                "attrs": {
                    "inventory": {
                        "type": "Inventory",
                        "attrs": self.get_context("Inventory")
                    },
                    "name": {
                        "type": "str",
                        "attrs": self.get_context("str")
                    },
                    "health": {
                        "type": "number",
                        "attrs": self.get_context("number")
                    },
                    "max_health": {
                        "type": "number",
                        "attrs": self.get_context("number")
                    },
                    "location": {
                        "type": "Location",
                        "attrs": self.get_context("Location")
                    },
                    "money": {
                        "type": "Currency",
                        "attrs": self.get_context("Currency")
                    },
                    "status_effects": {
                        "type": "StatusEffects",
                        "attrs": self.get_context("StatusEffects")
                    },
                    "in_combat": {
                        "type": "boolean",
                        "attrs": self.get_context("boolean")
                    },
                    "position": {
                        "type": "Position",
                        "attrs": self.get_context("Position")
                    }
                }
            }
        }

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
        
        elif tokens[0].type == "CONTEXT":
            ctx_tok = tokens.pop(0)
            ctx = ctx_tok.value
            # TODO: do stuff with this context object (primarily just populate variable tables)
            # print(f"CONTEXT: {ctx}")
            
            self.add_base_context()
            
            if ctx == "#!enter-script":
                print("ENTER SCRIPT")
            elif ctx == "#!exit-script":
                print("EXIT SCRIPT")
            elif ctx == "#input-script":
                print("INPUT SCRIPT")
            elif (m := re.match(r"(?P<obj>[a-zA-Z_]+)-(?P<act>[a-zA-Z_]+)-script", ctx)):
                m: re.Match
                d = m.groupdict()
                obj = d["obj"]
                act = d["act"]
                
                
                
                match obj:
                    case "weapon":
                        match act:
                            case "use":
                                ...
                            case "damaged":
                                ...
                            case "broken":
                                ...
                            case "equip":
                                ...
                            case "unequip":
                                ...
                            case "repair":
                                ...
                            case "player_hit":
                                ...
                            case _: pass
                    case "armor":
                        match act:
                            case "equip":
                                ...
                            case "unequip":
                                ...
                            case "player_hit":
                                ...
                            case "damaged":
                                ...
                            case "broken":
                                ...
                            case _: pass
                    case "tool":
                        ...
                    case "item":
                        ...
                    case "ammo":
                        ...
                    case "interactable":
                        ...
                    case "enemy":
                        ...
                    case "attack":
                        ...
                    case "combat":
                        ...
                    case "status_effect":
                        ...
                    case "dungeon":
                        ...
                    case "room":
                        ...
                    case _:
                        pass
                
            elif "/" in ctx:
                data_dir = ctx.replace("#!", "", 1)
                print(f"get data from dir: {data_dir}")
            
            return None
        
        elif tokens[0].type == "MACRO":
            snap = self.snapshot(tokens)
            macro = tokens.pop(0)
            if tokens:
                if tokens[0] == ("LITERAL", "("):
                    try:
                        args = self.macro_args(tokens)
                    
                        if tokens[0] == ("LITERAL", "{"):
                            if self.parsing_macro:
                                raise FinalScriptError(f"Cannot define nested macro definitions. @ {macro.get_location()}")
                            
                            self.parsing_macro = True
                            self.curr_macro_args = args
                            body = self.scope(tokens)
                            self.parsing_macro = False
                            self.curr_macro_args = []
                        else:
                            raise ScriptError()
                        
                        md = MacroDef(macro, args, body)
                        self.macro_functions.update({macro.value: md})
                        self.variable_table.set(macro.value, md)
                        return None #md
                    
                    except ScriptError as e:
                        tokens.clear()
                        tokens.extend(self.load_snapshot(snap))
                        return self.expression(tokens)
                
                elif tokens[0] == ("LITERAL", "="):
                    tokens.pop(0)
                    expr = self.expression(tokens)
                    ma = MacroAssign(macro, expr)
                    self.macros.update({macro.value: ma})
                    self.variable_table.set(macro.value, ma)
                    return None #ma
                
                else:
                    tokens.insert(0, macro)
                    return self.expression(tokens)
            else:
                return MacroRef(macro, self)
        
        elif tokens[0].type == "WORD":
            if len(tokens) >= 2 and tokens[1] == ("LITERAL", ":"):
                var_token = tokens.pop(0)
                tokens.pop(0)
                type_annotation = self.type_annotation(tokens)
                
            else:
                return self.expression(tokens)
        else:
            return self.expression(tokens)
    
    def type_annotation(self, tokens:list[Token]):
        
        if tokens:
            if tokens[0].type == "WORD":
                tp = tokens.pop(0)
                
                if tokens:
                    if tokens[0] == ("LITERAL", "["):
                        tokens.pop(0)
                        tps = []
                        while tokens and tokens[0] != ("LITERAL", "]"):
                            tps.append(self.type_annotation(tokens))
                            
                            if tokens[0] == ("LITERAL", ","):
                                tokens.pop(0)
                            else:
                                break
                        
                        if not tokens:
                            raise FinalScriptError(f"Unexpected EOF while parsing type annotation")
                        
                        if tokens[0] == ("LITERAL", "]"):
                            tokens.pop(0)
                            return Type(tp, tps)
                        else:
                            raise tokens[0].expected("']'")
                        
                    else:
                        return Type(tp)
                else:
                    raise FinalScriptError(f"Unexpected EOF while parsing type annotation")
                
            else:
                raise tokens[0].expected("type name")
        else:
            raise FinalScriptError(f"Unexpected EOF while parsing type annotation")
        
    
    def macro_args(self, tokens:list[Token]):
        lp = tokens.pop(0)
        
        args = []
        while tokens and not (tokens[0] == ("LITERAL", ")")):
            if tokens[0].type == "MACRO":
                args.append(tokens.pop(0))
            else:
                raise ScriptError(f"Expected macro name @ {tokens[0].get_location()}")
            
            if tokens:
                if tokens[0] == ("LITERAL", ","):
                    tokens.pop(0)
                elif tokens[0] == ("LITERAL", ")"):
                    break
                else:
                    raise ScriptError(f"Expected ',' or ')' @ {tokens[0].get_location()}")
            else:
                raise FinalScriptError(f"Unexpected EOF while parsing macro def/call")
        
        if not tokens:
            raise FinalScriptError(f"Unexpected EOF while parsing macro def/call")
        
        tokens.pop(0)
        return args
    
    def expression(self, tokens:list[Token]):
        return self.comp(tokens)

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
        tokens.pop(0)
        if tokens and tokens[0] == ("LITERAL", "("):
            tokens.pop(0)
            condition = self.expression(tokens)
            
            if tokens and tokens[0] == ("LITERAL", ")"):
                tokens.pop(0)
                
                if tokens and tokens[0] == ("LITERAL", "{"):
                    body = self.scope(tokens)
                elif tokens:
                    raise tokens[0].expected("{")
                else:
                    raise FinalScriptError("Unexpected EOF while parsing if-statement")
                
                stmt = IfStatement(condition, body)
                
                while tokens and tokens[0] == ("KEYWORD", "elif"):
                    tokens.pop(0)
                    
                    if tokens and tokens[0] == ("LITERAL", "("):
                        tokens.pop(0)
                        condition = self.expression(tokens)
                        if tokens and tokens[0] == ("LITERAL", ")"):
                            tokens.pop(0)
                            if tokens and tokens[0] == ("LITERAL", "{"):
                                body = self.scope(tokens)
                            elif tokens:
                                raise tokens[0].expected("{")
                            else:
                                raise FinalScriptError("Unexpected EOF while parsing elif-statement")
                            st = IfStatement(condition, body)
                            stmt.else_node = st
                            stmt = st
                        elif tokens:
                            raise tokens[0].expected(")")
                        else:
                            raise FinalScriptError("Unexpected EOF while parsing elif-statement")
                    elif tokens:
                        raise tokens[0].expected("(")
                    else:
                        raise FinalScriptError("Unexpected EOF while parsing elif-statement")
                
                if tokens and tokens[0] == ("KEYWORD", "else"):
                    tokens.pop(0)
                    if tokens and tokens[0] == ("LITERAL", "{"):
                        body = self.scope(tokens)
                    elif tokens:
                        raise tokens[0].expected("{")
                    else:
                        raise FinalScriptError(f"Unexpected EOF while parsing else-statement")
                    
                    stmt.else_node = body
                
                return stmt

                
            elif tokens:
                raise tokens[0].expected(")")
            else:
                raise FinalScriptError("Unexpected EOF while parsing if-statement")
            
        elif tokens:
            raise tokens[0].expected("(")
        else:
            raise FinalScriptError("Unexpected EOF while parsing if-statement")

    def match_case(self, tokens:list[Token]):
        tokens.pop(0)
        
        matching = self.expression(tokens)
        
        if tokens and tokens[0] == ("LITERAL", "{"):
            tokens.pop(0)
            cases = []
            bodies = []
            while tokens and not (tokens[0] == ("LITERAL", "}")):
                if tokens[0] == ("KEYWORD", "case"):
                    tokens.pop(0)
                    case = self.expression(tokens)
                    if tokens and tokens[0] == ("LITERAL", "{"):
                        body = self.scope(tokens)
                        
                        cases.append(case)
                        bodies.append(body)
                        
                    elif tokens:
                        raise tokens[0].expected("{")
                    else:
                        raise FinalScriptError("Unexpected EOF while parsing match-case-statement")
                
                else:
                    raise tokens[0].expected("case")
            
            if not tokens:
                raise FinalScriptError("Unexpected EOF while parsing match-case-statement")
            
            tokens.pop(0)
            
            return MatchCase(matching, cases, bodies)
            
        elif tokens:
            raise tokens[0].expected("{")
        else:
            raise FinalScriptError("Unexpected EOF while parsing match-case-statement")
            

    def while_loop(self, tokens:list[Token]):
        tokens.pop(0)
        condition = self.expression(tokens)
        
        if tokens and tokens[0] == ("LITERAL", "{"):
            body = self.scope(tokens)
        else:
            body = None
        
        return WhileLoop(condition, body)

    def for_loop(self, tokens:list[Token]): # I kinda want support for python-style and C-style for loops...
        tokens.pop(0)
        
        if tokens and tokens[0] == ("LITERAL", "["):
            tokens.pop(0)
            init = self.expression(tokens)
            
            if tokens and tokens[0] == ("LITERAL", ";"):
                tokens.pop(0)
                
                step = self.expression(tokens)
                
                if tokens and tokens[0] == ("LITERAL", ";"):
                    tokens.pop(0)
                    
                    end = self.expression(tokens)
                    
                    if tokens and tokens[0] == ("LITERAL", "]"):
                        tokens.pop(0)
                        
                        if tokens and tokens[0] == ("LITERAL", "{"):
                            body = self.scope(tokens)
                            
                            return ForLoopC(init, step, end, body)
                        elif tokens:
                            raise tokens[0].expected("{")
                    elif tokens:
                        raise tokens[0].expected("]")
                elif tokens:
                    raise tokens[0].expected(";")
            elif tokens:
                raise tokens[0].expected(";")
            
            raise FinalScriptError("Unexpected EOF while parsing for-loop")
            
        else:
            unpack = self.unpacker(tokens)
            
            if tokens and tokens[0] == ("KEYWORD", "in"):
                tokens.pop(0)
                
                expr = self.expression(tokens)
                
                if tokens and tokens[0] == ("LITERAL", "{"):
                    body = self.scope(tokens)
                
                    return ForLoopPy(unpack, expr, body)
                
                elif tokens:
                    raise tokens[0].expected("{")
                else:
                    raise FinalScriptError("Unexpected EOF while parsing for-loop")
            elif tokens:
                raise tokens[0].expected("in")
            else:
                raise FinalScriptError("Unexpected EOF while parsing for-loop")
            
    def unpacker(self, tokens:list[Token]):
        unpacks = []
        while tokens and not (tokens[0] == ("LITERAL", ("{", ")"))):
            if tokens[0].type == "WORD":
                unpacks.append(ReferenceNode(tokens.pop(0), es3=self))
            elif tokens[0] == ("LITERAL", "("):
                tokens.pop(0)
                
                unpacks.append(self.unpacker(tokens))
                
                if tokens and tokens[0] == ("LITERAL", ")"):
                    tokens.pop(0)
                elif tokens:
                    raise tokens[0].expected(")")
                else:
                    raise FinalScriptError("Unexpected EOF while parsing unpack-expression")
            
            if tokens and tokens[0] == ("LITERAL", ","):
                tokens.pop(0)
            else:
                break
        
        return UnpackNode(unpacks)

    def comp(self, tokens:list[Token]):
        if tokens:
            if tokens[0] == ("KEYWORD", "NOT"):
                tokens.pop(0)
                c = self.comp(tokens)
                return NotNode(c)
            else:
                a = self.arith(tokens)

                if tokens:
                    if tokens[0] == ("LITERAL", ("<=", "<", ">=", ">", "!=", "==")):
                        op = tokens.pop(0)
                        
                        a2 = self.arith(tokens)
                        
                        return Comp(a, op, a2)
                        
                    elif tokens[0] == ("KEYWORD", ("and", "or")):
                        op = tokens.pop(0)
                        
                        c2 = self.comp(tokens)
                        
                        return Comp(c, op, c2)
                    else:
                        return a
                return a
                
        else:
            raise EOF("<TODO: EOF in comp method>")

    def arith(self, tokens:list[Token]):
        left = self.mul(tokens)
        while tokens and tokens[0] == ("LITERAL", ("+", "-")):
            op = tokens.pop(0)
            right = self.mul(tokens)
            
            left = BinaryOp(left, op, right)
        
        return left
    
    def mul(self, tokens:list[Token]):
        left = self.pow(tokens)
        while tokens and tokens[0] == ("LITERAL", ("*", "/", "%")):
            op = tokens.pop(0)
            right = self.pow(tokens)
            
            left = BinaryOp(left, op, right)
            
        return left
    
    def pow(self, tokens:list[Token]):
        left = self.concat(tokens)
        while tokens and tokens[0] == ("LITERAL", "^"):
            op = tokens.pop(0)
            right = self.concat(tokens)
            
            left = BinaryOp(left, op, right)
        return left

    def concat(self, tokens:list[Token]):
        args = [self.atom(tokens)]
        do_concat = False
        while tokens and tokens[0] == ("LITERAL", ".."):
            do_concat = True
            tokens.pop(0)
            a = self.atom(tokens)
            args.append(a)
        
        if tokens and tokens[0] == ("LITERAL", "::"):
            do_concat = True
            tokens.pop(0)
            sep = self.atom(tokens)
        else:
            sep = None
        
        if do_concat:
            return Concat(args, sep)
        else:
            return args[0]
            
    def atom(self, tokens:list[Token]):
        snap = self.snapshot(tokens)
        if tokens:
            if tokens[0].type == "WORD" or tokens[0] == ("LITERAL", "#"):
                return self.var(tokens)
            elif tokens[0] == ("LITERAL", "-"):
                op = tokens.pop(0)
                
                right = self.atom(tokens)
                
                return UnaryOp(op, right)
            elif tokens[0] == ("LITERAL", "("):
                lp = tokens.pop(0)

                expr = self.expression(tokens)
                
                if tokens:
                    if tokens[0] == ("LITERAL", ")"):
                        return expr
                    else:
                        raise tokens[0].expected(")")
                else:
                    raise FinalScriptError(f"No valid closing parenthesis found for open parenthesis @ {lp.get_location()}")
            elif tokens[0] == ("LITERAL", ("{", "[")):
                return self.table(tokens)

            elif tokens[0].type in ["STRING", "BOOLEAN", "NUMBER"]:
                return ValueNode(tokens.pop(0))
            elif tokens[0] == ("KEYWORD", "none"):
                return NoneNode(tokens.pop(0))
            elif tokens[0].type == "MACRO":
                macro = tokens.pop(0)
                
                if tokens and tokens[0] == ("LITERAL", "("):
                    if self.variable_table.exists(macro.value):
                        node = self.variable_table.get(macro.value, None)
                        
                        if isinstance(node, MacroDef):
                            args = self.macro_params(tokens)
                            
                            if len(node.args) != len(args):
                                raise FinalScriptError(f"Invalid number of arguments passed to function-macro @ {macro.get_location()}")
                            
                            return MacroCall(macro, args, self)
                        
                        else:
                            raise FinalScriptError(f"Macro '{macro.value}' is a value-macro and cannot be called as a function")
                    
                    elif self.parsing_macro and macro.value in [m.value for m in self.curr_macro_args]:
                        args = self.macro_params(tokens)
                        return MacroCall(macro, args, self)
                    
                    else:
                        raise FinalScriptError(f"Macro '{macro.value}' @ {macro.get_location()} is undefined.")
                
                else:
                    if self.variable_table.exists(macro.value):
                        node = self.variable_table.get(macro.value, None)
                        
                        if isinstance(node, MacroAssign):
                            return MacroRef(macro, self)
                        else:
                            raise FinalScriptError(f"Macro '{macro.value}' is a function-macro and connot be referenced plainly.")
                        
                        
                    elif self.parsing_macro and macro.value in [m.value for m in self.curr_macro_args]:
                        return MacroRef(macro, self)
                    else:
                        raise FinalScriptError(f"Macro '{macro.value}' @ {macro.get_location()} is undefined.")

            elif tokens[0].type == "COMMAND":
                return self.commands[tokens[0].value](tokens)


    def macro_params(self, tokens:list[Token]):
        tokens.pop(0)
        args = []
        while tokens and not (tokens[0] == ("LITERAL", ")")):
            expr = self.expression(tokens)
            args.append(expr)
            if tokens:
                if tokens[0] == ("LITERAL", ","):
                    tokens.pop(0)
                elif tokens[0] == ("LITERAL", ")"):
                    break
                else:
                    raise tokens[0].expected("',' or ')'", False)
            else:
                raise FinalScriptError("unexpected EOF while parsing macro paramaters")
        
        tokens.pop(0)
        return args
    
    def var(self, tokens:list[Token]):
        if tokens:
            if tokens[0] == ("LITERAL", "#"):
                if len(tokens) >= 2:
                    if tokens[1].type == "WORD":
                        tokens.pop(0)
                        obj = ReferenceNode(tokens.pop(0), global_=True, es3=self)
                    else:
                        raise tokens[1].expected("variable name", False)
                else:
                    raise FinalScriptError(f"Unexpected EOF while parsing variable name")
            
            elif tokens[0].type == "WORD":
                obj = ReferenceNode(tokens.pop(0), es3=self)
            else:
                raise tokens[0].expected("variable name", False)
            
            while tokens and tokens[0] == ("LITERAL", (".", "[", "(", "$")):
                if tokens[0] == ("LITERAL", "."):
                    dot = tokens.pop(0)
                    if tokens:
                        if tokens[0].type == "WORD":
                            attr = tokens.pop(0)
                        else:
                            raise tokens[0].expected("attribute", False)
                    else:
                        raise dot.unexpected()
                    
                    obj = AccessNode(obj, attr)
                
                elif tokens[0] == ("LITERAL", "["):
                    lb = tokens.pop(0)
                    key = self.expression(tokens)
                    
                    if tokens:
                        if tokens[0] == ("LITERAL", "]"):
                            rb = tokens.pop(0)
                        
                        else:
                            raise tokens[0].expected("]")
                    else:
                        raise FinalScriptError(f"No valid closing brace found for open brace @ {lb.get_location()}")
                    
                    obj = GetItemNode(obj, key)
                elif tokens[0] == ("LITERAL", "("):
                    args = self.call_args(tokens)
                    obj = CallNode(obj, args, self)
                
                elif tokens[0] == ("LITERAL", "$"):
                    tokens.pop(0)
                    if tokens:
                        if tokens[0] == ("LITERAL", "["):
                            tokens.pop(0)
                            toks = []
                            while tokens and not (tokens[0] == ("LITERAL", "]")):
                                t = tokens.pop(0)
                                t.in_macro = True # this will help with syntax highlighting
                                toks.append(t)
                            if not tokens:
                                raise FinalScriptError(f"Unexpected EOF while parsing macro function")
                            if tokens[0] == ("LITERAL", "]"):
                                last = tokens.pop(0)
                                obj = MacroStack(obj, toks, last, self)
                            else:
                                raise FinalScriptError(f"you have reached an impossible state! congrats!")
                        else:
                            if tokens:
                                raise tokens[0].expected("macro stack ('$[...]')", False)
                            else:
                                raise FinalScriptError("Unexpected EOF while parsing macro stack")
            
            if tokens and tokens[0] == ("LITERAL", "="):
                tokens.pop(0)
                expr = self.expression(tokens)
                
                obj = AssignNode(obj, expr)
            
            return obj
        else:
            raise FinalScriptError("Expected variable name")

    def table(self, tokens:list[Token]):
        if tokens:
            if tokens[0] == ("LITERAL", "["):
                tokens.pop(0)
                ls = []
                while tokens and not (tokens[0] == ("LITERAL", "]")):
                    expr = self.expression(tokens)
                    ls.append(expr)
                    if tokens:
                        if tokens[0] == ("LITERAL", ","):
                            tokens.pop(0)
                        elif tokens[0] == ("LITERAL", "]"):
                            break
                        else:
                            raise tokens[0].expected("',' or ']'", False)
                    else:
                        raise FinalScriptError("Unexpected EOF while parsing list")
                tokens.pop(0)
                return ListNode(ls)
                            
            elif tokens[0] == ("LITERAL", "{"):
                tokens.pop(0)
                keys = []
                vals = []
                while tokens and not (tokens[0] == ("LITERAL", "}")):
                    key = self.expression(tokens)
                    if tokens:
                        if tokens[0] == ("LITERAL", ":"):
                            tokens.pop(0)
                        else:
                            raise tokens[0].expected(":")
                    else:
                        raise FinalScriptError(f"Unexpected EOF while parsing dictionary")
                    val = self.expression(tokens)
                    
                    keys.append(key)
                    vals.append(val)
                    if tokens:
                        if tokens[0] == ("LITERAL", ","):
                            tokens.pop(0)
                        elif tokens[0] == ("LITERAL", "}"):
                            break
                        else:
                            raise tokens[0].expected("',' or '}'", False)
                    else:
                        raise FinalScriptError("Unexpected EOF while parsing dictionary")
                tokens.pop(0)
                return DictNode(keys, vals)
    
    def call_args(self, tokens:list[Token]) -> ArgsCallNode:
        if tokens:
            if tokens[0] == ("LITERAL", ("(", "{")):
                lp = tokens.pop(0)
                p = lp.value == "("
                args = []
                kwargs = {}
                in_args = True
                while tokens and not ((p and tokens[0] == ("LITERAL", ")")) or ((not p) and tokens[0] == ("LITERAL", "}"))):
                    if tokens[0].type == "WORD":
                        if len(tokens) >= 2:
                            if tokens[1] == ("LITERAL", ":"):
                                in_args = False
                                keyword = tokens.pop(0)
                                c = tokens.pop(0)
                                value = self.expression(tokens)
                                
                                if keyword.value in kwargs.keys():
                                    raise FinalScriptError(f"repeated keyword argument '{keyword.value}' @ {keyword.get_location()}")
                                
                                kwargs.update({keyword.value: value})
                                
                            elif (p and tokens[1] == ("LITERAL", ")")) or ((not p) and tokens[1] == ("LITERAL", "}")):
                                if in_args:
                                    args.append(ReferenceNode(tokens.pop(0), es3=self))
                                    tokens.pop(0)
                                    return ArgsCallNode(args, {})
                                else:
                                    raise FinalScriptError(f"all positional arguments must be before any keyword arguments. @ {tokens[0].get_location()}")
                            else:
                                expr = self.expression(tokens)
                                
                        else:
                            raise EOF(f"unexpected EOF @ {tokens[1].get_location()}")
                    elif tokens[0] == ("LITERAL", ":"):
                        in_args = False
                        if len(tokens) >= 2:
                            if tokens[1].type == "WORD":
                                tokens.pop(0)
                                valword = tokens.pop(0)
                                if valword.value in kwargs.keys():
                                    raise FinalScriptError(f"repeated keyword argument '{valword.value}' @ {valword.get_location()}")
                                kwargs.update({valword.value: ReferenceNode(valword, es3=self)})
                            else:
                                raise FinalScriptError(f"Invalid syntax for implied keyword argument. @ {tokens[1].get_location()}")
                        else:
                            raise FinalScriptError("Unexpected EOF while trying to parse arguments.")
                    
                    else:
                        expr = self.expression(tokens)
                        args.append(expr)
                    
                    if tokens:
                        if tokens[0] == ("LITERAL", ","):
                            tokens.pop(0)
                            if (p and tokens[0] == ("LITERAL", ")")) or ((not p) and tokens[0] == ("LITERAL", "}")):
                                tokens.pop(0)
                                return ArgsCallNode(args, kwargs)
                        elif (p and tokens[0] == ("LITERAL", ")")) or ((not p) and tokens[0] == ("LITERAL", "}")):
                            tokens.pop(0)
                            return ArgsCallNode(args, kwargs)
                        else:
                            raise FinalScriptError(f"Expected comma or closing {"parenthesis" if p else "bracket"} @ {tokens[0].get_location()}")
                    else:
                        raise FinalScriptError("Unexpected EOF while trying to parse arguments.")

            else:
                raise tokens[0].expected("'(' or '{'", False)

        else:
            raise EOF("Unexpected EOF while trying to parse arguments.")

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
          | assign
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

concat : atom (CONCAT atom)? (CONCATSEP atom)?

assign : var '=' expression

atom : '-' atom
     | '(' expression ')'
     | (NUMBER|BOOL|STRING|OBJECT|table|scope|macro|function_call)

var : WORD (('.' WORD)* ('[' expression ']')*)

table : '[' comma_expressions ']'
      | '{' table_contents '}'

function_call : var (parameters scope?)?
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
    
    print(json.dumps(es.compiled_script, indent=4))
