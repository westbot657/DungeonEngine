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

import random

class Weapon(GameObject):
    identifier = Identifier("engine", "object/", "weapon")
    def __init__(self, abstract, name:str, description:str, damage:DynamicValue, range:int, max_durability:int, durability:int, ammo_type, events:dict):
        self.abstract = abstract
        self.name = name
        self.description = description
        self.damage = damage
        self.range = range
        self.durability = durability
        self.max_durability = max_durability
        self.ammo_type = ammo_type
        self.events = events

        self.owner = None

        self.loaded_ammo = None

    def __repr__(self):
        return f"Weapon {self.name}: damage:{self.damage} range:{self.range}  durability:{self.durability}"

    def bonuses(self, function_memory:FunctionMemory):
        return f"+{self.damage.quickDisplay(function_memory)}dmg {self.range}ft"

    def fullStats(self, function_memory:FunctionMemory, is_equipped=False):
        return f"{self.name} +{self.damage.fullDisplay(function_memory)}dmg {self.range}ft" + (f" \"{self.description}\"" if self.description else "") + " {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [EQUIPPED]" if is_equipped else "")

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"

    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".description": self.description,
            ".damage": self.damage,
            ".range": self.range,
            ".durability": self.durability,
            ".max_durability": self.max_durability
        }
        return d

    def updateLocalVariables(self, locals: dict):
        ...
    
    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#weapon": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)
        
    def onAttack(self, function_memory:FunctionMemory, target, acc:int=None):

        if acc is None: acc = random.randint(1, 100)

        damage = self.damage.getNew(function_memory)

        Log["debug"]["weapon"]("weapon.onAttack() called!")
        if on_attack := self.events.get("on_attack", None):
            self.prepFunctionMemory(function_memory)
            function_memory.update({
                "damage": damage,
                "accuracy": acc
            })
            ev = function_memory.generatorEvaluateFunction(on_attack)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = function_memory.engine.loader.stopIterationEval(e.value, v)

            damage = int(function_memory.ref("damage"))
            acc = int(function_memory.ref("accuracy"))
            self.postEvaluate(function_memory)
        Log["debug"]["weapon"](f"Weapon onAttack: damage:{damage}  accuracy:{acc}  target:{target}")

        function_memory.addContextData({"#damage": damage})
        ev = target.onEvent(function_memory, None, "on_attacked")
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield v
                v = ev.send(res)
        except StopIteration as e:
            v = function_memory.engine.loader.stopIterationEval(e.value, v)

    def onDamage(self, function_memory:FunctionMemory):
        if on_damage := self.events.get("on_damage", None):
            self.prepFunctionMemory(function_memory)

            ev = function_memory.generatorEvaluateFunction(on_damage)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)

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

            self.postEvaluate(function_memory)

    def onEquip(self, function_memory:FunctionMemory):
        if on_equip := self.events.get("on_equip", None):
            self.prepFunctionMemory(function_memory)

            ev = function_memory.generatorEvaluateFunction(on_equip)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)

            self.postEvaluate(function_memory)

    def onUnequip(self, function_memory:FunctionMemory):
        if on_unequip := self.events.get("on_unequip", None):
            self.prepFunctionMemory(function_memory)

            ev = function_memory.generatorEvaluateFunction(on_unequip)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)

            self.postEvaluate(function_memory)

    def onRepair(self, function_memory:FunctionMemory):
        if on_repair := self.events.get("on_repair", None):
            self.prepFunctionMemory(function_memory)

            ev = function_memory.generatorEvaluateFunction(on_repair)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)

            self.postEvaluate(function_memory)

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

    def _get_save(self, function_memory:FunctionMemory):
        d = {
            "type": "engine:weapon",
            "parent": self.abstract.identifier.full()
        }

        if self.name != self.abstract.getName():
            d.update({"name": self.name})
        if self.description != self.abstract.getDescription():
            d.update({"description": self.description})
        if self.damage != self.abstract.getDamage():
            d.update({"damage": self.damage.raw_data})
        if self.range != self.abstract.getRange():
            d.update({"range": self.range})
        if self.max_durability != self.abstract.getMaxDurability():
            d.update({"max_durability": self.max_durability})
        if self.durability != self.abstract.getDurability():
            d.update({"durability": self.durability})
        if self.ammo_type != self.abstract.getAmmoType():
            d.update({"ammo_type": self.ammo_type.identifier.full()})

        return d
