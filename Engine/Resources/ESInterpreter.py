# pylint: disable=[W,R,C,import-error]

try:
    from .Logger import Log
    from .ESInstructions import *
except ImportError as e:
    from Logger import Log
    from ESInstructions import *


from mergedeep import merge
from typing import Any
from enum import Enum, auto

class DataStack:
    
    def __init__(self):
        self.stack: list[dict] = []
        self.index = -1
    
    def push(self):
        self.stack.append({})
        self.index += 1
        
    def pop(self):
        out = self.stack.pop(self.index)
        self.index -= 1
        return out
    
    def update(self, data:dict):
        self.stack[self.index].update(data)

class ESInterpreter:
    
    class ExecutionFlag(Enum):
        COMPLETE = auto(), "Executed Successfully"
        INCOMPLETE = auto(), "Execution paused, return when needed"
        ERROR = auto(), "Execution failed"

        def __new__(cls, value, description):
            obj = object.__new__(cls)
            obj._value_ = value
            obj.description = description
            obj.instance_parameter = None  # Placeholder for the instance parameter
            return obj

        def __call__(self, instance_parameter):
            obj = object.__new__(self.__class__)
            obj._value_ = self._value_
            obj.description = self.description
            obj.instance_parameter = instance_parameter
            return obj

        def __eq__(self, other):
            if isinstance(other, ESInterpreter.ExecutionFlag):
                return self._value_ == other._value_
            return False
    
    def __init__(self, script:dict=None):
        self.script = script
        self.memory = {
            "#vars": {},
            "#data": {}
        }
        self.pointer = 0
        self.instructions = []

    def assemble(self):
        self.instructions.clear()
        self._assemble(self.script)

    def _assemble(self, branch):
        if isinstance(branch, dict):
            if funcs := branch.get("#functions", None):
                self._assemble(funcs)
            elif br := branch.get("#access", None):
                ...
            elif br := branch.get("#call", None):
                ...
            elif br := branch.get("#check", None):
                ...
            elif br := branch.get("#for", None):
                ...
            elif br := branch.get("#while", None):
                ...
            elif br := branch.get("#match", None):
                ...
            elif br := branch.get("#function", None):
                ...
            elif br := branch.get("#break", None):
                ...
            elif br := branch.get("#return", None):
                ...
            elif br := branch.get("#ref", None):
                ...
            elif br := branch.get("#store", None):
                ...
            elif br := branch.get("#not", None):
                ...
            elif br := branch.get("#new", None):
                ...
            elif br := branch.get("#move", None):
                ...
        elif isinstance(branch, list):
            for item in branch:
                self._assemble(item)
        else:
            pass # ignore invalid data



if __name__ == "__main__":
    from ES3 import EngineScript, test_script
    
    es = EngineScript.inline_script(test_script)
    
    es.compile()
    
    breakpoint()

