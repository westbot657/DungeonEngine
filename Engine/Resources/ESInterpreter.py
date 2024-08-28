# pylint: disable=[W,R,C,import-error]

try:
    from .Logger import Log
except ImportError as e:
    from Logger import Log

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
    
    @classmethod
    def execute(cls, script, execution_point:list = None, execute_from:list|None=None, execute_data=None):
        if execution_point is None: execution_point = []
        
        if execute_from:
            return cls.execute(script[execute_from[0]], execution_point+[execute_from[0]], execute_from[1:], execute_data)
        else:
            if isinstance(script, dict):
                if funcs := script.get("#functions", None):
                    pass
                elif call := script.get("#call", None):
                    pass
            elif isinstance(script, list):
                pass
            else:
                return script
    
    
