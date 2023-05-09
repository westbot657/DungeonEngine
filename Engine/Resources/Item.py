# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .Util import Util
    from .EngineDummy import Engine
    from .EngineOperation import EngineOperation, _EngineOperation
    from .FunctionMemory import FunctionMemory
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from Util import Util
    from EngineDummy import Engine
    from EngineOperation import EngineOperation, _EngineOperation
    from FunctionMemory import FunctionMemory

from enum import Enum, auto

class Item(GameObject):

    identifier = Identifier("engine", "object/", "item")
    def __init__(self, abstract, name:str, max_count:int, count:int, data:dict|None, events:dict):
        self.abstract = abstract
        self.name = name
        self.max_count = max_count
        self.count = count
        self.data = data
        self.events = events

        self.owner = None

    def checkKeyword(self, keyword):
        return keyword in self.abstract.getKeywords()

    def __repr__(self):
        return f"Item {self.name}: max_count:{self.max_count} count:{self.count} data:{self.data}"

    def fullStats(self, engine, _):
        return f"{self.name}  {self.count}/{self.max_count}"

    def quickStats(self, engine):
        return f"{self.name}  {self.count}/{self.max_count}"
    
    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".max_count": self.max_count,
            ".count": self.count
        }

        for key, val in self.data.items():
            d.update({f".{key}": val})

        return d

    def updateLocalVariables(self, locals: dict):
        ...

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#item": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def onUse(self, function_memory:FunctionMemory):

        if on_use := self.events.get("on_use", None):
            self.prepFunctionMemory(function_memory)
            
            ev = function_memory.generatorEvaluateFunction(on_use)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            res = v
            self.postEvaluate(function_memory)

        if self.max_count > 0:

            self.count -= 1

            if self.count <= 0:
                ev = self.onExpended(function_memory)
                v = None
                try:
                    v = ev.send(None)
                    while isinstance(v, _EngineOperation):
                        res = yield v
                        v = ev.send(res)
                except StopIteration as e:
                    v = e.value or (v if not isinstance(v, _EngineOperation) else None)


    def onExpended(self, function_memory:FunctionMemory):
        if on_expended := self.events.get("on_expended", None):
            self.prepFunctionMemory(function_memory)
            ev = function_memory.generatorEvaluateFunction(on_expended)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            res = v
            self.postEvaluate(function_memory)
