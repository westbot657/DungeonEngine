# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .EngineDummy import Engine
    from .Util import Util
    from .FunctionMemory import FunctionMemory
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from EngineDummy import Engine
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

    def onUse(self, function_memory:FunctionMemory, amount_used):
        if on_use := self.events.get("on_use", None):

            function_memory.addContextData({
                "#tool": self
            })
            function_memory.update({
                ".name": self.name,
                ".durability": self.durability,
                ".max_durability": self.max_durability,
            })
            res = function_memory.engine.evaluateFunction(on_use)
            function_memory.clear()

            if res is Tool.Action.CANCEL_USE:
                return

            if self.max_durability > 0:
                self.durability -= 1

                if self.durability <= 0:
                    self.onBreak(function_memory)

                else:
                    self.onDamage(function_memory)

    def onBreak(self, function_memory:FunctionMemory):
        if on_break := self.events.get("on_break", None):
            function_memory.addContextData({
                "#tool": self
            })
            res = function_memory.engine.evaluateFunction(on_break)
            function_memory.clear()

    def onDamage(self, function_memory:FunctionMemory):
        if on_damage := self.events.get("on_damage", None):
            function_memory.addContextData({
                "#tool": self
            })
            res = function_memory.engine.evaluateFunction(on_damage)
            function_memory.clear()

    def onRepair(self, function_memory:FunctionMemory):
        if on_repair := self.events.get("on_repair", None):
            function_memory.addContextData({
                "#tool": self
            })
            res = function_memory.engine.evaluateFunction(on_repair)
            function_memory.clear()

    def onEquip(self, function_memory:FunctionMemory):
        if on_equip := self.events.get("on_equip", None):
            function_memory.addContextData({
                "#tool": self
            })
            res = function_memory.engine.evaluateFunction(on_equip)
            function_memory.clear()

    def onUnequip(self, function_memory:FunctionMemory):
        if on_unequip := self.events.get("on_unequip", None):
            function_memory.addContextData({
                "#tool": self
            })
            res = function_memory.engine.evaluateFunction(on_unequip)
            function_memory.clear()

    def __repr__(self):
        return f"Tool: {self.name} {self.durability}/{self.max_durability}"

    def fullStats(self, engine, is_equipped=False):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [EQUIPPED]" if is_equipped else "")

    def quickStats(self, engine):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"



