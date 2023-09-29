# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .EngineDummy import Engine
    from .EngineOperation import EngineOperation, _EngineOperation
    from .Util import Util
    from .FunctionMemory import FunctionMemory
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from EngineDummy import Engine
    from EngineOperation import EngineOperation, _EngineOperation
    from Util import Util
    from FunctionMemory import FunctionMemory

from enum import Enum, auto

class Tool(GameObject):

    class Action(Enum):
        CANCEL_USE = auto()

    identifier = Identifier("engine", "object/", "tool")
    def __init__(self, abstract, name:str, description:str, durability:int, max_durability:int, events:dict, data:dict):
        self.abstract = abstract
        self.name = name
        self.description = description
        self.durability = durability
        self.max_durability = max_durability
        self.events = events
        self.data = data

        self.owner = None

    def checkKeyword(self, keyword):
        return keyword in self.abstract.getKeywords()

    def getLocalVariables(self):
        d = {
            ".name": self.name,
            ".description": self.description,
            ".durability": self.durability,
            ".max_durability": self.max_durability,
        }

        for key, val in self.data.items():
            d.update({f".{key}": val})

        return d

    def updateLocalVariables(self, function_memory, locals:dict):
        if n := locals.get(".name", None):
            if isinstance(n, str) and n.strip() != self.name:
                self.name = n.strip()
        
        if (n := locals.get(".description", None)) is not None:
            if isinstance(n, str) and n.strip() != self.description:
                self.description = n.strip()
        
        if (m := locals.get(".max_durability", None)) is not None:
            if isinstance(m, int):
                if m <= 0:
                    self.durability = -1
                    self.max_durability = -1
                else:
                    self.max_durability = m
                    self.durability = min(self.durability, self.max_durability)

        if (d := locals.get(".durability", None)) is not None:
            if isinstance(d, int) and (0 < d <= self.max_durability):
                self.durability = d

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({ # context data is immutable
            "#tool": self
        })
        # local variables are mutable (as long as they remain valid)
        function_memory.update(self.getLocalVariables())

    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory, function_memory.symbol_table)

    def onUse(self, function_memory:FunctionMemory):
        if on_use := self.events.get("on_use", None):

            self.prepFunctionMemory(function_memory)
            #res = function_memory.evaluateFunction(on_use)

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
            
            # function_memory.clear()

            if res is Tool.Action.CANCEL_USE:
                return

            if self.max_durability > 0:
                self.durability -= 1

                if self.durability <= 0:
                    v = None
                    ev = self.onBreak(function_memory)
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield v
                            v = ev.send(res)
                    except StopIteration as e:
                        v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                    return v

                else:
                    v = None
                    ev = self.onDamaged(function_memory)
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield v
                            v = ev.send(res)
                    except StopIteration as e:
                        v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                    return v

    def onBreak(self, function_memory:FunctionMemory):
        if on_break := self.events.get("on_break", None):
            self.prepFunctionMemory(function_memory)
            #res = function_memory.evaluateFunction(on_break)
            ev = function_memory.generatorEvaluateFunction(on_break)
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


        if self.durability <= 0:
            function_memory.ref("#player").inventory.removeObject(self)

    def onDamaged(self, function_memory:FunctionMemory):
        if on_damaged := self.events.get("on_damaged", None):
            self.prepFunctionMemory(function_memory)
            #res = function_memory.evaluateFunction(on_damage)
            ev = function_memory.generatorEvaluateFunction(on_damaged)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                if isinstance(e.value, _EngineOperation): print("\n\n\nEngine Operation\n\n\n")
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            res = v
            self.postEvaluate(function_memory)

            # function_memory.clear()

    def onRepair(self, function_memory:FunctionMemory):
        if on_repair := self.events.get("on_repair", None):
            self.prepFunctionMemory(function_memory)
            #res = function_memory.evaluateFunction(on_repair)
            ev = function_memory.generatorEvaluateFunction(on_repair)
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

            # function_memory.clear()

    def onEquip(self, function_memory:FunctionMemory):
        if on_equip := self.events.get("on_equip", None):
            self.prepFunctionMemory(function_memory)
            #res = function_memory.evaluateFunction(on_equip)
            ev = function_memory.generatorEvaluateFunction(on_equip)
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

            # function_memory.clear()

    def onUnequip(self, function_memory:FunctionMemory):
        if on_unequip := self.events.get("on_unequip", None):
            self.prepFunctionMemory(function_memory)
            #res = function_memory.evaluateFunction(on_unequip)
            ev = function_memory.generatorEvaluateFunction(on_unequip)
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

            # function_memory.clear()

    def onPlayerHit(self, function_memory:FunctionMemory, damage:int):
        if on_player_hit := self.events.get("on_player_hit", None):
            self.prepFunctionMemory(function_memory)
            #res = function_memory.evaluateFunction(on_unequip)
            ev = function_memory.generatorEvaluateFunction(on_player_hit)
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

    def __repr__(self):
        return f"Tool: {self.name} {self.durability}/{self.max_durability}"

    def fullStats(self, function_memory:FunctionMemory, is_equipped=False):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}" + (f" \"{self.description}\"" if self.description else "") + (" [EQUIPPED]" if is_equipped else "")

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"

    def _get_save(self, function_memory:FunctionMemory):
        d = {
            "type": "engine:tool",
            "parent": self.abstract.identifier.full(),
            "data": self.data
        }

        if self.name != self.abstract.getName():
            d.update({"name": self.name})
        if self.description != self.abstract.getDescription():
            d.update({"description": self.description})
        if self.max_durability != self.abstract.getMaxDurability():
            d.update({"max_durability": self.max_durability})
        if self.durability != self.abstract.getDurability():
            d.update({"durability": self.durability})
        return d
