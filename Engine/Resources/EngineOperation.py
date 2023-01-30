

from enum import Enum, auto

class OpType(Enum):
    GET_INPUT = auto()


class _EngineOperation:
    def __init__(self, operation_type):
        self.operation_type = operation_type

class EngineOperation:

    class GetInput(_EngineOperation):
        def __init__(self, target, prompt):
            super().__init__(OpType.GET_INPUT)
            self.target = target
            self.prompt = prompt



