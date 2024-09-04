# pylint: disable=[W,R,C,import-error]

try:
    from .Logger import Log
except ImportError as e:
    from Logger import Log


from mergedeep import merge
from typing import Any
from enum import Enum, auto

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




if __name__ == "__main__":
    from ES3 import EngineScript, test_script
    
    es = EngineScript.inline_script(test_script)
    
    es.compile()
    
    breakpoint()

