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
    def __init__(self, abstract, name:str, durability:int, max_durability:int, events:dict):
        self.abstract = abstract
        self.name = name
        self.durability = durability
        self.max_durability = max_durability
        self.events = events

    def checkKeyword(self, keyword):
        return keyword in self.abstract.getKeywords()

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({ # context data is immutable
            "#tool": self
        })
        function_memory.update({ # local variables are mutable (as long as they remain valid)
            ".name": self.name,
            ".durability": self.durability,
            ".max_durability": self.max_durability,
        })

    def postEvaluate(self, function_memory:FunctionMemory):
        x = function_memory.symbol_table

        if n := x.get(".name", None):
            if isinstance(n, str) and n.strip() != self.name:
                self.name = n.strip()
        
        if m := x.get(".max_durability", None) is not None:
            if isinstance(m, int):
                if m <= 0:
                    self.durability = self.max_durability = -1
                else:
                    self.max_durability = m
                    self.durability = min(self.durability, self.max_durability)

        if d := x.get(".durability", None) is not None:
            if isinstance(d, int) and (0 < d <= self.max_durability):
                self.durability = d

    def onUse(self, function_memory:FunctionMemory, amount_used):
        if on_use := self.events.get("on_use", None):

            self.prepFunctionMemory(function_memory)
            res = function_memory.evaluateFunction(on_use)
            self.postEvaluate(function_memory)
            # function_memory.clear()

            if res is Tool.Action.CANCEL_USE:
                return
            
            elif isinstance(res, (EngineOperation, _EngineOperation)):
                return res

            if self.max_durability > 0:
                self.durability -= 1

                if self.durability <= 0:
                    self.onBreak(function_memory)

                else:
                    self.onDamage(function_memory)

    def onBreak(self, function_memory:FunctionMemory):
        if on_break := self.events.get("on_break", None):
            self.prepFunctionMemory(function_memory)
            res = function_memory.evaluateFunction(on_break)
            self.postEvaluate(function_memory)


        if self.durability <= 0:
            function_memory.ref("#player").inventory.removeObject(self)

    def onDamage(self, function_memory:FunctionMemory):
        if on_damage := self.events.get("on_damage", None):
            self.prepFunctionMemory(function_memory)
            res = function_memory.evaluateFunction(on_damage)
            self.postEvaluate(function_memory)

            # function_memory.clear()

    def onRepair(self, function_memory:FunctionMemory):
        if on_repair := self.events.get("on_repair", None):
            self.prepFunctionMemory(function_memory)
            res = function_memory.evaluateFunction(on_repair)
            self.postEvaluate(function_memory)

            # function_memory.clear()

    def onEquip(self, function_memory:FunctionMemory):
        if on_equip := self.events.get("on_equip", None):
            self.prepFunctionMemory(function_memory)
            res = function_memory.evaluateFunction(on_equip)
            self.postEvaluate(function_memory)

            # function_memory.clear()

    def onUnequip(self, function_memory:FunctionMemory):
        if on_unequip := self.events.get("on_unequip", None):
            self.prepFunctionMemory(function_memory)
            res = function_memory.evaluateFunction(on_unequip)
            self.postEvaluate(function_memory)

            # function_memory.clear()

    def __repr__(self):
        return f"Tool: {self.name} {self.durability}/{self.max_durability}"

    def fullStats(self, engine, is_equipped=False):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [EQUIPPED]" if is_equipped else "")

    def quickStats(self, engine):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"



