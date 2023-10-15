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
    def __init__(self, abstract, name:str, description:str, damage_reduction:DynamicValue, max_durability:int, durability:int, events:dict):
        self.abstract = abstract
        self.name = name
        self.description = description
        self.damage_reduction = damage_reduction
        self.max_durability = max_durability
        self.durability = durability
        self.events = events

        self.owner = None

    def bonuses(self, engine):
        return f"+{self.damage_reduction.quickDisplay(engine)}def"

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name} +{self.damage_reduction.quickDisplay(function_memory)}def {Util.getDurabilityBar(self.durability, self.max_durability)}"

    def fullStats(self, function_memory:FunctionMemory, is_equipped=False):
        return f"{self.name} +{self.damage_reduction.fullDisplay(function_memory)}def" + (f" \"{self.description}\"" if self.description else "") + f" {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [WEARING]" if is_equipped else "")

    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".description": self.description,
            ".damage_reduction": self.damage_reduction,
            ".max_durability": self.max_durability,
            ".durability": self.durability
        }

        return d

    def updateLocalVariables(self, locals: dict):
        ...
        if n := locals.get(".name", None):
            if isinstance(n, str) and n.strip() != self.name:
                self.name = n.strip()
        
        if n := locals.get(".description", None):
            if isinstance(n, str) and n.strip() != self.description:
                self.description = n.strip()
        
        if n := locals.get(".durability", None):
            if isinstance(n, int) and n != self.durability:
                self.durability = n
    
    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#armor": self
        })
        function_memory.update(self.getLocalVariables())

    def postEvaluate(self, function_memory:FunctionMemory):
        ... # self.updateLocalVariables(function_memory.symbol_table)

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

    def onPlayerHit(self, function_memory:FunctionMemory, damage:int):

        self.prepFunctionMemory(function_memory)
        # function_memory.update({
        #     "damage": damage
        # })
        reduced_damage = self.damage_reduction.getNew(function_memory)
        # print(f"Armor.onPlayerHit(): damage: {damage} | damage reducer: {reduced_damage}")
        function_memory.update({
            "damage": max(0, damage - reduced_damage)
        })
        function_memory.addContextData({
            "#damage_reduction": reduced_damage
        })

        combat = function_memory.ref("#combat")

        combat.turn_summary.update({
            "blocking_armor": self if reduced_damage else None,
            "damage_blocked": reduced_damage
        })
        
        if reduced_damage > 0:
            if reduced_damage < damage:
                combat.addTask(combat.Operation.Message(f"`{self.name}` ─ Blocked *{reduced_damage}* damage!", function_memory.ref("#player")))
                # function_memory.engine.sendOutput(function_memory.ref("#player"), f"`{self.name}` ─ Blocked *{reduced_damage}* damage!")
            elif reduced_damage >= damage:
                combat.addTask(combat.Operation.Message(f"`{self.name}` ─ Attack blocked!", function_memory.ref("#player")))
                
                # function_memory.engine.sendOutput(function_memory.ref("#player"), f"`{self.name}` ─ Attack blocked!")

        if on_player_hit := self.events.get("on_player_hit", None):
            #self.prepFunctionMemory(function_memory)
            
            
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

        if self.durability <= 0:
            function_memory.ref("#player").inventory.removeObject(self)

    def _get_save(self, function_memory:FunctionMemory):
        d = {
            "type": "engine:armor",
            "parent": self.abstract.identifier.full()
        }

        if self.name != self.abstract.getName():
            d.update({"name": self.name})
        if self.description != self.abstract.getDescription():
            d.update({"description": self.description})
        if self.damage_reduction != self.abstract.getDamageReduction():
            d.update({"damage_reduction": self.damage_reduction})
        if self.max_durability != self.abstract.getMaxDurability():
            d.update({"max_durability": self.max_durability})
        if self.durability != self.abstract.getDurability():
            d.update({"durability": self.durability})

        return d