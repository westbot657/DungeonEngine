# pylint: disable=[W,R,C,import-error]

try:
    from .EngineErrors import FunctionCallError
except ImportError:
    from EngineErrors import FunctionCallError



class ConsoleCommand:
    _commands = {}

    def __init__(self, name, args): # TODO: finish this...
        self.name = name
        self.command_exec = None

    def __call__(self, command_exec):
        self.command_exec = command_exec
        ConsoleCommand._commands.update({self.name: self})

    def call(self, *args):
        raise FunctionCallError(f"Command: '{self.name}' is not properly defined")

    @classmethod
    def call_command(cls, command:str, args:list):
        if cmd := cls._commands.get(command, None):
            return cmd.call(args)
        raise FunctionCallError(f"No command exists by the name '{command}'")
