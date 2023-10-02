# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .EngineErrors import MemoryError
    from .Logger import Log
    from .FunctionalElement import FunctionalElement
    from .Environment import Environment
    from .EngineOperation import _EngineOperation
except ImportError:
    from EngineDummy import Engine
    from EngineErrors import MemoryError
    from Logger import Log
    from FunctionalElement import FunctionalElement
    from Environment import Environment
    from EngineOperation import _EngineOperation

from typing import Any

import glob, json, sys, os



class FunctionMemory:
    #_instance = None
    

    with open(f"./resources/engine.json", "r+", encoding="utf-8") as f:
        _config: dict = json.load(f)
        global_environment_variables: dict = _config.get("environment_variables")
        data_types: dict = _config.get("data_types")

        stored_functions: dict = _config.get("functions", {})

    function_files = glob.glob("**/ec_functions.json", recursive=True)
    for file in function_files:
        with open(file, "r+", encoding="utf-8") as f:
            stored_functions.update(json.load(f))

    # def __new__(cls):
    #     if not cls._instance:
    #         cls._instance = super().__new__(cls)
    #         cls._instance.init()
    #     return cls._instance

    def saveGame(self):
        self.engine.saveGame()

    def unloadGame(self):
        self.engine.unloadGame()

    def __init__(self, engine:Engine):
        self.symbol_table = {}
        self.context_data = {}
        self.engine = engine
    
    # def prepFunction(self):
    #     self.symbol_table.clear()
    #     self.context_data.clear()

    def evaluateFunction(self, data:dict):
        return self.engine.evaluateFunction(data, self)

    def generatorEvaluateFunction(self, data:dict):
        return self.engine.generatorEvaluateFunction(data, self)

    def addContextData(self, data:dict):
        #print(f"#store: {data}")
        self.context_data.update(data)

    def getMemory(self):
        return {
            "local variables": self.symbol_table,
            "context variables": self.context_data,
            "global constants": self.global_environment_variables,
            # "functions": self.stored_functions
        }

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
        if name.startswith("$"):
            FunctionMemory.stored_functions.update({name: value})
        else:
            if "." in name:
                props = [(f".{prop}" if not prop.startswith("#") else prop) for prop in name.split(".")]
                # print(f"PROPS: {props}")
                prop = props.pop(0)
                if prop in self.context_data:
                    return self._setProperty(self.context_data[prop], props, value)

                elif prop.replace(".", "") in self.symbol_table:
                    return self._setProperty(self.symbol_table[prop.replace(".", "")], props, value)
                
            self.symbol_table.update({name: value})
    
    def _setProperty(self, obj, propertyTree:list, value):
        # print(f"setProperty: {obj} {propertyTree} {value}")
        while propertyTree:
            if isinstance(obj, FunctionalElement):
                obj_props = obj.getLocalVariables()
                curr = propertyTree.pop(0)
                # print(f"{obj_props} {curr}")
                if curr in obj_props:
                    if len(propertyTree) == 0:
                        # print(obj_props, curr, value)
                        obj_props.update({
                            curr: value
                        })
                        obj.updateLocalVariables(obj_props)
                    
                    obj = obj_props[curr]
                else:
                    raise MemoryError(f"Variable '{obj}' has no property '{curr}'")
            else:
                break
        return obj

    def call(self, name:str):
        if name.startswith("$"):
            func = FunctionMemory.stored_functions.get(name, None)
        else:
            func = self.symbol_table.get(name, None)
        
        if func is None:
            raise MemoryError(f"Function is not defined: '{name}'")
    
        if not isinstance(func, dict):
            raise MemoryError(f"Cannot call non-function variable: '{name}' ({func})")
        
        ev = self.generatorEvaluateFunction(func)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield v
                v = ev.send(res)
        except StopIteration as e:
            v = self.engine.loader.stopIterationEval(e.value, v)
        return v

    def call2(self, name:str):
        if name.startswith("$"):
            func = FunctionMemory.stored_functions.get(name, None)
        else:
            func = self.symbol_table.get(name, None)
        
        if func is None:
            raise MemoryError(f"Function is not defined: '{name}'")
    
        if not isinstance(func, dict):
            raise MemoryError(f"Cannot call non-function variable: '{name}' ({func})")
        
        v = self.evaluateFunction(func)
        return v

    def ref(self, name:str):
        #print(f"#ref: {self.context_data}")
        optional = False
        if name.startswith("%"):
            if name in self.global_environment_variables:
                return self.global_environment_variables[name]
            raise MemoryError(f"Global environment variable not defined: '{name}'")

        elif name.startswith("#"):
            if "?" in name:
                name = name.replace("?", "")
                optional = True
            if "." in name:
                props = [(f".{prop}" if not prop.startswith("#") else prop) for prop in name.split(".")]
                prop = props.pop(0)
                if prop in self.context_data:
                    return self._getProperty(self.context_data[prop], props)

            if name in self.context_data:
                return self.context_data[name]
            
            if optional:
                return None
            raise MemoryError(f"Local context variable not defined: '{name}'")

        else:
            props = [f".{prop}" if prop else "." for prop in name.split(".")]
            prop = props.pop(0)[1:]
            if prop == "": prop = props.pop(0)
            
            if "?" in prop:
                prop = prop.replace("?", "")
                optional = True
            
            if prop in self.symbol_table:
                return self._getProperty(self.symbol_table[prop], props)

            if optional:
                return None

            raise MemoryError(f"Variable referenced before assignment: '{name}'")

        # else:
        #     if name in self.symbol_table:
        #         return self.symbol_table[name]
            
        #     raise MemoryError(f"Variable referenced before assignment: '{name}'")

    def _getProperty(self, obj, propertyTree:list):
        optional = False
        while propertyTree:
            if isinstance(obj, FunctionalElement):
                obj_props = obj.getLocalVariables()
                curr = propertyTree.pop(0)
                
                if "?" in curr:
                    curr = curr.replace("?", "")
                    optional = True
                
                if curr in obj_props:
                    obj = obj_props[curr]
                else:
                    if optional:
                        return None
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


