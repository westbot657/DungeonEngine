# pylint: disable=[W,R,C,import-error]

try:
    from .EngineErrors import FunctionCallError
    from .Identifier import Identifier
except ImportError:
    from EngineErrors import FunctionCallError
    from Identifier import Identifier



class ConsoleCommand:
    _commands = {}

    def __init__(self, identity:Identifier, args:dict): # TODO: finish this...
        self.identity = identity
        self.command_exec = None
        self.args = args

    def __call__(self, command_exec):
        self.command_exec = command_exec
        ConsoleCommand._commands.update({self.identity.full(): self})

    def call(self, engine, *args):
        raise FunctionCallError(f"Command: '{self.identity.full()}' is not properly defined")

    @classmethod
    def call_command(cls, engine, command:str, args:list):
        if cmd := cls._commands.get(command, None):
            return cmd.call(engine, *args)
        raise FunctionCallError(f"No command exists by the name '{command}'")

