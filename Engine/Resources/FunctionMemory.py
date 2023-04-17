# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .EngineErrors import MemoryError
except ImportError:
    from EngineDummy import Engine
    from EngineErrors import MemoryError

import json

"""
Function Memory:

Variable Types:
'%' - constant, global utility variables
'.' - local environment variables
'#' - global environment variables
'' - local, temporary variables

"""

class FunctionMemory:
    _instance = None

    with open(f"./resources/environment_variables.json", "r+", encoding="utf-8") as f:
        global_environment_variables = json.load(f)

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.symbol_table = {}
        self.context_data = {}
    
    def prepFunction(self):
        self.symbol_table.clear()
        self.context_data.clear()

    def addContextData(self, data:dict):
        self.context_data.update(data)

    def checkPredicate(self, engine:Engine, predicate:dict):
        ...

    def store(self, name:str, value):
        self.symbol_table.update({name, value})
        
    def ref(self, name:str):

        if name.startswith("%"):
            if name in self.global_environment_variables:
                return self.global_environment_variables[name]
            raise MemoryError(f"Global environment variable not defined: '{name}'")

        elif name.startswith("."):
            if name in self.context_data:
                return self.context_data[name]
            raise MemoryError(f"Local context variable not defined: '{name}'")

        else:
            if name in self.symbol_table:
                return self.symbol_table[name]
            raise MemoryError(f"Variable referenced before assignment: '{name}'")

    def clear(self):
        self.symbol_table.clear()
        self.context_data.clear()

    def update(self, data:dict):
        self.symbol_table.update(data)
    


if __name__ == "__main__":
    pass


