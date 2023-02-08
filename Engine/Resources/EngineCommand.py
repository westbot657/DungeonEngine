# pylint: disable=[W,R,C,import-error]


class EngineCommand:
    _commands = {}

    def __init__(self, name, args): # TODO: finish this...
        self.name = name
        self.command_exec = None

    def __call__(self, command_exec):
        self.command_exec = command_exec

