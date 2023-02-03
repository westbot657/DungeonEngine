# pylint: disable=[W,R,C,import-error]


from enum import Enum, auto

class OpType(Enum):
    GET_INPUT = auto()
    RESTART = auto()
    SUCCESS = auto()
    CONTINUE = auto()
    ERROR = auto()
    FAILURE = auto()
    CANCEL = auto()

class _EngineOperation:
    def __init__(self, operation_type):
        self.operation_type = operation_type

class EngineOperation:
    
    class GetInput(_EngineOperation):
        """
        yield this to request input from a player
        leave target as None to accept input from any player (for internal engine use only)
        leave prompt as None to wait for target to give any input
        """
        def __init__(self, target:int=None, prompt:str=None):
            super().__init__(OpType.GET_INPUT)
            self.target = target
            self.prompt = prompt

    class Restart(_EngineOperation):
        """
        yield/return this to restart the entire interaction
        """
        def __init__(self):
            super().__init__(OpType.RESTART)

    class Cancel(_EngineOperation):
        """
        yield/return to end the interaction early
        """
        def __init__(self):
            super().__init__(OpType.CANCEL)
    
    class Success(_EngineOperation):
        """
        yield/return if interaction passes and stuff happens
        """
        def __init__(self):
            super().__init__(OpType.SUCCESS)
    
    class Continue(_EngineOperation):
        """
        yield this to tell engine to continue with the interaction (this actually sounds pointless now, but whatever)
        """
        def __init__(self):
            super().__init__(OpType.CONTINUE)
    
    class Failure(_EngineOperation):
        """
        yield/return if interaction fails and nothing happens
        """
        def __init__(self):
            super().__init__(OpType.FAILURE)
            
    class Error(_EngineOperation):
        """
        """
        def __init__(self, details):
            super().__init__(OpType.ERROR)
            self.details = details

