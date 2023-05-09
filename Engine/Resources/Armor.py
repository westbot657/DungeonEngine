# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .Util import Util
    from .FunctionMemory import FunctionMemory
    from .EngineOperation import _EngineOperation
    from .Logger import Log
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from Util import Util
    from FunctionMemory import FunctionMemory
    from EngineOperation import _EngineOperation
    from Logger import Log

from typing import Generator

class Armor(GameObject):
    identifier = Identifier("engine", "object/", "armor")
    def __init__(self, abstract, name:str, damage_reduction:DynamicValue, max_durability:int, durability:int, events:dict):
        self.abstract = abstract
        self.name = name
        self.damage_reduction = damage_reduction
        self.max_durability = max_durability
        self.durability = durability
        self.events = events

        self.owner = None

    def bonuses(self, engine):
        return f"+{self.damage_reduction.quickDisplay(engine)}def"

    def quickStats(self, engine):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"

    def fullStats(self, engine, is_equipped=False):
        return f"{self.name} +{self.damage_reduction.fullDisplay(engine)}def {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [WEARING]" if is_equipped else "")

    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".damage_reduction": self.damage_reduction,
            ".max_durability": self.max_durability,
            ".durability": self.durability
        }

        return d

    def updateLocalVariables(self, locals: dict):
        ...
    
    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#armor": self
        })
        function_memory.update(self.getLocalVariables())

    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)


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

    def onDamageReduction(self, function_memory:FunctionMemory, damage:int):

        function_memory.update({
            "damage": damage
        })

        ev = self.damage_reduction.getNew(function_memory)
        v = None
        if isinstance(ev, Generator):
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
        
        elif isinstance(ev, (int, float)):
            v = ev
        else:
            Log["error"]["armor"]["event"]["on damage reduction"](f"invalid return from damage_reduction DynamicValue.getNew(): '{ev}'")
            

        if on_damage_reduction := self.events.get("on_damage_reduction", None):
            self.prepFunctionMemory(function_memory)
            ev = function_memory.generatorEvaluateFunction(on_damage_reduction)

            # function_memory.clear()
    def onDamaged(self, function_memory:FunctionMemory):
        if on_damaged := self.events.get("on_damaged", None):
            self.prepFunctionMemory(function_memory)
            ev = function_memory.generatorEvaluateFunction(on_damaged)
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

    def onBreak(self, function_memory:FunctionMemory):
        if on_break := self.events.get("on_break", None):
            self.prepFunctionMemory(function_memory)
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

    def _get_save(self, function_memory:FunctionMemory):
        d = {
            "type": "engine:armor",
            "parent": self.abstract.identifier.full()
        }

        if self.name != self.abstract.getName():
            d.update({"name": self.name})
        if self.damage_reduction != self.abstract.getDamageReduction():
            d.update({"damage_reduction": self.damage_reduction})
        if self.max_durability != self.abstract.getMaxDurability():
            d.update({"max_durability": self.max_durability})
        if self.durability != self.abstract.getDurability():
            d.update({"durability": self.durability})

        return d