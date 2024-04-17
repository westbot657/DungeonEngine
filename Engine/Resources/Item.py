# pylint: disable=[W,R,C,import-error]

from GameObject import GameObject
from Identifier import Identifier
from Util import Util
from EngineDummy import Engine
from EngineOperation import EngineOperation, _EngineOperation
from FunctionMemory import FunctionMemory
from Serializer import Serializer, Serializable

from enum import Enum, auto

@Serializable("Item")
class Item(GameObject):

    identifier = Identifier("engine", "object/", "item")
    def __init__(self, abstract, name:str, description:str, max_count:int, count:int, data:dict|None, events:dict):
        self.abstract = abstract
        self.name = name
        self.description = description
        self.max_count = max_count
        self.count = count
        self.data = data
        self.events = events

        self.owner = None

    def serialize(self):
        return {
            "abstract": Serializer.serialize(self.abstract),
            "name": Serializer.serialize(self.name),
            "description": Serializer.serialize(self.description),
            "max_count": Serializer.serialize(self.max_count),
            "count": Serializer.serialize(self.count),
            "data": Serializer.serialize(self.data),
            "events": Serializer.serialize(self.events),
            "owner": Serializer.serialize(self.owner)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    def can_stack(self, other):
        other: Item
        return self.abstract is other.abstract and self.name == other.name and self.description == other.description and self.max_count == other.max_count and self.data == other.data

    def stack(self, other) -> bool:
        other: Item
        """returns whether `other` should be deleted after trying to stack"""
        if self.can_stack(other):
            if self.max_count <= 0:
                self.count += other.count
                return True
            
            diff = self.max_count - self.count
            
            c = other.count
            other.count = max(0, other.count - diff)
            d = c - other.count
            
            self.count += d
            
            return other.count <= 0
        return False

    def checkKeyword(self, keyword):
        return keyword.lower() in self.abstract.getKeywords()

    def __repr__(self):
        return f"Item {self.name}: max_count:{self.max_count} count:{self.count} data:{self.data}"

    def fullStats(self, function_memory:FunctionMemory, _):
        return f"{self.name}  {self.count}/{self.max_count}" + (f" \"{self.description}\"" if self.description else "")

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name}  {self.count}/{self.max_count}"
    
    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".description": self.description,
            ".max_count": self.max_count,
            ".count": self.count
        }

        for key, val in self.data.items():
            d.update({f".{key}": val})

        return d

    def updateLocalVariables(self, locals: dict):
        ...
        if n := locals.get(".name", None):
            if isinstance(n, str) and n.strip() != self.name:
                self.name = n.strip()
        
        if n := locals.get(".description", None):
            if isinstance(n, str) and n.strip() != self.description:
                self.description = n.strip()

        if n := locals.get(".count", None):
            if isinstance(n, int) and n != self.count:
                self.count = n

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#item": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        ... # self.updateLocalVariables(function_memory.symbol_table)

    def onUse(self, function_memory:FunctionMemory, inventory):

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
            if self.count <= 0:
                inventory.removeObject(self)
                inventory.consolidate()
        

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

    def _get_save(self, function_memory:FunctionMemory):
        d = {
            "type": "engine:item",
            "parent": self.abstract.identifier.full(),
            "data": self.data
        }

        if self.name != self.abstract.getName():
            d.update({"name": self.name})
        if self.description != self.abstract.getDescription():
            d.update({"description": self.description})
        if self.max_count != self.abstract.getMaxCount():
            d.update({"max_count": self.max_count})
        if self.count != self.abstract.getCount():
            d.update({"count": self.count})
        return d
