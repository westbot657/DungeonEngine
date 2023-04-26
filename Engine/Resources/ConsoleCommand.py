# pylint: disable=[W,R,C,import-error]

try:
    from .EngineErrors import FunctionCallError, ParseError, IdentifierError
    from .Identifier import Identifier
except ImportError:
    from EngineErrors import FunctionCallError, ParseError, IdentifierError
    from Identifier import Identifier

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
        raise FunctionCallError(f"Command: '{self.identity.full()}' is not properly defined")

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
                    string += quote
                    text = text[1:]
                    return string, text.strip()
                else:
                    string += text[0]
                    text = text[1:]
        else:
            s = text.split(" ", 1)
            if len(s) == 1: return s + [""]
            return s

    # @classmethod
    # def _parse_number(cls, text) -> tuple[int|float, str]:
    #     num = ""
    #     while True:
    #         if len(text) == 0:
    #             break
    #         if text[0] in "0123456789":
    #             num += text[0]
    #             text = text[1:]
    #         elif text[0] == ".":
    #             if "." not in num:
    #                 num += "."
    #                 text = text[1:]
    #             else:
    #                 raise ParseError("number cannot contain '.' twice")
    #         elif text[0] == " ":
    #             break
    #         else:
    #             raise ParseError("numbers cannot contain letters")

    #     if "." in num:
    #         return float(num), text
    #     return int(num), text

    # @classmethod
    # def _parse_word(cls, engine, text):
    #     word, text = text.split(" ", 1)
    #     if word == "true":
    #         return True, text
    #     if word == "false":
    #         return False, text
    #     try:
    #         i = Identifier.fromString(word)
    #         if s := engine.loader.searchFor(i):
    #             return s
    #     except IdentifierError:
    #         pass


    @classmethod
    def _parse_args(cls, function_memory, arg_tree:dict|None, text:str) -> list|None:
        engine = function_memory.engine
        args = []
        for arg, con in arg_tree.items():
            arg: str
            con: dict|None
            arg_name, arg_types = arg.split(":")
            arg_types = arg_types.split("|")
            for tp in arg_types:
                try:
                    match tp:
                        case "str":
                            string, other = cls._parse_string(text)
                            text = other
                            args.append(string)
                        case "int":
                            n, other = text.split(" ", 1)
                            if re.match(r"(\d+|0[Bb][01_]+|0[Oo][0-7_]+|0[Xx][a-fA-F0-9_]+)", n):
                                if "__" in n: raise ParseError("numbers can only have up to 1 '_' between numeric characters")
                                args.append(int(n))
                                text = other
                            else:
                                raise ParseError("expected 'int'")
                        case "float":
                            n, other = text.split(" ", 1)
                            if re.match(r"[0-9_]+\.[0-9_]+", n):
                                if "__" in n: raise ParseError("numbers can only have up to 1 '_' between numeric characters")
                                args.append(float(n))
                                text = other
                            else:
                                raise ParseError("expected 'float'")
                        case "bool":
                            n, other = text.split(" ", 1)
                            if n == "true":
                                args.append(True)
                            elif n == "false":
                                args.append(False)
                            else:
                                raise ParseError("expected 'true' or 'false'")
                        case "dict" | "list":
                            s = text
                            out = None
                            while out is None:
                                try:
                                    out = json.loads(s)
                                except json.decoder.JSONDecodeError as e:
                                    if e.args:
                                        if m := re.match(r"Extra data: line \d+ column \d+ \(char (?P<col>\d+)\)", e.args[0]):
                                            col = m.groupdict()["col"]
                                            s = s[0:col].strip()
                                        else:
                                            raise e
                        case "engine:ammo":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_ammo.get(n, None):
                                return a
                        case "engine:armor":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_armor.get(n, None):
                                return a
                        case "engine:attack":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_attacks.get(n, None):
                                return a
                        case "engine:item":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_items.get(n, None):
                                return a
                        case "engine:tool":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_tools.get(n, None):
                                return a
                        case "engine:weapon":
                            n, other = text.split(" ", 1)
                            if a := engine.loader.abstract_weapons.get(n, None):
                                return a
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


    def _run(self, function_memory, text:str):
        args = ConsoleCommand._parse_args(function_memory, self.args, text)


    @classmethod
    def handle_input(cls, function_memory, text:str):
        values = []
        if " " not in text:
            cmd, text = text, ""
        else:
            cmd, text = text.split(" ", 1)

        if command := cls._commands.get(cmd, None):
            #try:
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

