# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .EngineErrors import MemoryError
    from .Logger import Log
    from .FunctionalElement import FunctionalElement
    from .Environment import Environment
except ImportError:
    from EngineDummy import Engine
    from EngineErrors import MemoryError
    from Logger import Log
    from FunctionalElement import FunctionalElement
    from Environment import Environment

from typing import Any

import json


class FunctionMemory:
    #_instance = None

    with open(f"./resources/engine.json", "r+", encoding="utf-8") as f:
        _config = json.load(f)
        global_environment_variables = _config.get("environment_variables")
        data_types = _config.get("data_types")

    # def __new__(cls):
    #     if not cls._instance:
    #         cls._instance = super().__new__(cls)
    #         cls._instance.init()
    #     return cls._instance

    def __init__(self, engine:Engine):
        self.symbol_table = {}
        self.context_data = {}
        self.engine = engine
    
    # def prepFunction(self):
    #     self.symbol_table.clear()
    #     self.context_data.clear()

    # def evaluateFunction(self, data:dict):
    #     return self.engine.evaluateFunction(data, self)

    def generatorEvaluateFunction(self, data:dict):
        return self.engine.generatorEvaluateFunction(data, self)

    def addContextData(self, data:dict):
        #print(f"#store: {data}")
        self.context_data.update(data)

    def checkPredicate(self, predicate:dict):
        #Log["debug"]["function memory"]["check predicate"](f"predicate: {predicate}")
        for key, value in predicate.items():
            key: str
            if key == "environment":
                e = Environment({})
                if (dungeon := self.context_data.get("#dungeon", None)) is not None:
                    e = e + dungeon.environment
                if (room := self.context_data.get("#room", None)) is not None:
                    e = e + room.environment
                v = e.check(value)
                #print(v)
                if v is False:
                    return False
                continue
            
            try:
                v = self.ref(key)
                if v != value:
                    return False
            except MemoryError:
                return False

        return True

    def getLocation(self, location):
        return self.engine.loader.getLocation(self, location)

    def getSaveData(self, obj:Any):
        return self.engine.loader.getSaveData(self, obj)

    def rebuildData(self, data:Any):
        return self.engine.loader.rebuildData(self, data)

    def store(self, name:str, value):
        self.symbol_table.update({name: value})
        
    def ref(self, name:str):
        #print(f"#ref: {self.context_data}")

        if name.startswith("%"):
            if name in self.global_environment_variables:
                return self.global_environment_variables[name]
            raise MemoryError(f"Global environment variable not defined: '{name}'")

        elif name.startswith("#"):
            if name in self.context_data:
                return self.context_data[name]
            raise MemoryError(f"Local context variable not defined: '{name}'")

        elif name.startswith("."):
            props = [f".{prop}" for prop in name.split(".") if prop]
            prop = props.pop(0)
            if prop in self.symbol_table:
                return self._getProperty(self.symbol_table[prop], props)

            raise MemoryError(f"Variable referenced before assignment: '{name}'")

        else:
            if name in self.symbol_table:
                return self.symbol_table[name]
            
            raise MemoryError(f"Variable referenced before assignment: '{name}'")

    def _getProperty(self, obj, propertyTree:list):
        while propertyTree:
            if isinstance(obj, FunctionalElement):
                obj_props = obj.getLocalVariables()
                curr = propertyTree.pop(0)
                if curr in obj_props:
                    obj = obj_props[curr]
                else:
                    raise MemoryError(f"Variable '{obj}' has no property '{curr}'")
            else:
                break
        return obj


    def clear(self):
        #self.symbol_table.clear()
        #self.context_data.clear()
        pass

    def update(self, data:dict):
        self.symbol_table.update(data)
    


if __name__ == "__main__":
    pass


