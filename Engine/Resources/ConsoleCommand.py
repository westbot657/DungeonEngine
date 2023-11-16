# pylint: disable=[W,R,C,import-error]

try:
    from .EngineErrors import FunctionCallError, ParseError, IdentifierError, UnknownPlayerError
    from .Identifier import Identifier
    from .GameObject import GameObject
    from .Logger import Log
    from .Player import Player
except ImportError:
    from EngineErrors import FunctionCallError, ParseError, IdentifierError, UnknownPlayerError
    from Identifier import Identifier
    from GameObject import GameObject
    from Logger import Log
    from Player import Player

import json, re

class ConsoleCommand:
    _commands = {}

    def __init__(self, identity:Identifier, args:dict): # TODO: finish this...
        self.identity = identity
        self.command_exec = None
        self.args = args

    def __call__(self, command_exec):
        self.command_exec = command_exec
        ConsoleCommand._commands.update({self.identity.full(): self})

    def call(self, function_memory, *args):
        if not self.command_exec:
            raise FunctionCallError(f"Command: '{self.identity.full()}' is not properly defined")
        return self.command_exec(function_memory, *args)
    @classmethod
    def _parse_string(cls, text:str) -> tuple[str, str]:
        string = ""
        if text.startswith(("'", "\"")):
            quote = text[0]
            text = text[1:]
            while True:
                if len(text) == 0:
                    raise ParseError(f"string does not terminate")
                if m := re.match(r"\\.", text[0:2]):
                    string += m.group()
                    text = text[2:]
                elif text[0] == quote:
                    # string += quote
                    text = text[1:]
                    return string, text.strip()
                else:
                    string += text[0]
                    text = text[1:]
        else:
            s = text.split(" ", 1)
            if len(s) == 1: return s + [""]
            return s

    @classmethod
    def _parse_args(cls, function_memory, arg_tree:dict|None, text:str) -> list|None:
        engine = function_memory.engine
        args = []
        text = text + " END"
        for arg, con in arg_tree.items():
            arg: str
            con: dict|None
            arg_name, arg_types = arg.split(":", 1)
            arg_types = arg_types.strip().split("|")
            for tp in arg_types:
                tp = tp.strip()

                if text.strip() == "END":
                    raise FunctionCallError(f"Not enough args passed to function")

                try:
                    match tp:
                        case "engine:str":
                            string, other = cls._parse_string(text)
                            text = other
                            args.append(string)
                        case "engine:int":
                            n, other = text.split(" ", 1)
                            if re.match(r"(\d+|0[Bb][01_]+|0[Oo][0-7_]+|0[Xx][a-fA-F0-9_]+)", n):
                                if "__" in n: raise ParseError("numbers can only have up to 1 '_' between numeric characters")
                                args.append(int(n))
                                text = other
                            else:
                                raise ParseError("expected 'int'")
                        case "engine:float":
                            n, other = text.split(" ", 1)
                            if re.match(r"[0-9_]+\.[0-9_]+", n):
                                if "__" in n: raise ParseError("numbers can only have up to 1 '_' between numeric characters")
                                args.append(float(n))
                                text = other
                            else:
                                raise ParseError("expected 'float'")
                        case "engine:bool":
                            n, other = text.split(" ", 1)
                            if n == "true":
                                args.append(True)
                            elif n == "false":
                                args.append(False)
                            else:
                                raise ParseError("expected 'true' or 'false'")
                        case "engine:dict" | "engine:list":
                            s = text
                            out = None
                            while out is None:
                                try:
                                    out = json.loads(s)
                                    args.append(out)
                                except json.decoder.JSONDecodeError as e:
                                    if e.args:
                                        if m := re.match(r"Extra data: line \d+ column \d+ \(char (?P<col>\d+)\)", e.args[0]):
                                            col = m.groupdict()["col"]
                                            s = s[0:col].strip()
                                            args.append(json.loads(s))
                                        else:
                                            raise e
                        case "engine:Player":
                            n, other = text.split(" ", 1)
                            try:
                                args.append(Player.getPlayer(n))
                            except UnknownPlayerError as e:
                                f = "\n".join(e.args)
                                print(f"Failed to get player.\n{f}")
                        case "engine:Ammo":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_ammo.get(n, None):
                                args.append(a)
                        case "engine:Armor":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_armor.get(n, None):
                                args.append(a)
                        case "engine:Attack":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_attacks.get(n, None):
                                args.append(a)
                        case "engine:Item":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_items.get(n, None):
                                args.append(a)
                        case "engine:Tool":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_tools.get(n, None):
                                args.append(a)
                        case "engine:Weapon":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_weapons.get(n, None):
                                args.append(a)
                        case "engine:GameObjectType":
                            n, other = text.split(" ", 1)

                        case _:
                            raise FunctionCallError(f"unrecognized value type: '{tp}'")
                    if con is None:
                        return args
                    if isinstance(con, dict):
                        a = cls._parse_args(function_memory, con, text)
                        if a is None: continue
                        if isinstance(a, list):
                            return args + a
                except ParseError:
                    pass
        return []


    def _run(self, function_memory, text:str):
        args = ConsoleCommand._parse_args(function_memory, self.args, text)
        return self.call(function_memory, *args)


    @classmethod
    def handle_input(cls, function_memory, text:str):
        values = []
        if " " not in text:
            cmd, text = text, ""
        else:
            cmd, text = text.split(" ", 1)

        if command := cls._commands.get(cmd, None):
            #try:
            Log["console command"](f"Running command {command}")
            command._run(function_memory, text)
            #except Exception as e:
            #    print(e, e.args)
            #    return
        else:
            function_memory.engine.io_hook.sendOutput(0, f"There is no command by the name '{cmd}'")
            return


    @classmethod
    def call_command(cls, function_memory, command:str, args:list):
        if cmd := cls._commands.get(command, None):
            return cmd.call(function_memory, *args)
        raise FunctionCallError(f"No command exists by the name '{command}'")

