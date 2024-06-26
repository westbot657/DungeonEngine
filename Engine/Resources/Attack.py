# pylint: disable=[W,R,C,import-error]

from .FunctionMemory import FunctionMemory
from .FunctionalElement import FunctionalElement
from .DynamicValue import DynamicValue
from .EngineOperation import _EngineOperation
from .Logger import Log
from .Serializer import Serializer, Serializable

import random

@Serializable("Attack")
class Attack(FunctionalElement):
    def __init__(self, abstract, name:str, damage:DynamicValue, range:int, accuracy:int, data:dict, events:dict):
        self.abstract = abstract

        self.name = name
        self.damage = damage
        self.range = range
        self.accuracy = accuracy
        self.data = data
        self.events = events
    
    def __repr__(self):
        return f"{self.name}"

    def getLocalVariables(self) -> dict:
        d = {
            ".name": self.name,
            ".damage": self.damage,
            ".range": self.range,
            ".accuracy": self.accuracy
        }

        for key, val in self.data.items():
            d.update({f".{key}": val})

        return d

    def __dict__(self):
        return {
            "%ENGINE:DATA-TYPE": "Attack",
            "name": self.name,
            "damage": self.damage,
            "range": self.range,
            "accuracy": self.accuracy,
            "events": self.events
        }

    def updateLocalVariables(self, locals: dict):
        ...

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#attack": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def fullStats(self, function_memory:FunctionMemory):
        return f"[TODO: Attack.fullStats()]"

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name}  {self.damage.quickDisplay(function_memory)}dmg {self.range}ft {self.accuracy}% accuracy"

    def onAttack(self, function_memory:FunctionMemory, target, acc=None):
        Log["debug"]["attack"]["on attack"]("Attack.onAttack() called!")
        if acc is None:
            acc = random.randint(1, 100)
        if (on_attack := self.events.get("on_attack", None)) is not None:
            self.prepFunctionMemory(function_memory)

            function_memory.update({
                "target": target,
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
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)

        if (ac := function_memory.symbol_table.get("accuracy", None)) is not None:
            if isinstance(ac, int) and 0 <= ac <= 100:
                acc = ac

        if acc >= self.accuracy:
            ev = self.onHit(function_memory, target)
        else:
            ev = self.onMiss(function_memory, target)

        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield v
                v = None
                v = ev.send(res)
        except StopIteration as e:
            if isinstance(e.value, _EngineOperation):
                yield e.value
            else:
                v = e.value if e.value is not None else v
        print(f"Attack.onAttack(): v: {v}")
        return v

    def onHit(self, function_memory:FunctionMemory, target):
        Log["debug"]["attack"]["on hit"]("attack hit!")
        Log["debug"]["attack"]["on hit"](self.damage)
        damage = self.damage.getNew(function_memory)

        function_memory.update({
            "damage": damage,
            "target": target
        })

        if (on_hit := self.events.get("on_hit", None)) is not None:
            self.prepFunctionMemory(function_memory)

            ev = function_memory.generatorEvaluateFunction(on_hit)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = None
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
        
        if (dmg := function_memory.symbol_table.get("damage", None)) is not None:
            if isinstance(dmg, int) and 0 <= dmg:
                damage = dmg
        
        combat = function_memory.ref("#combat")

        combat.turn_summary.update({
            "attack_hit": bool(damage > 0),
            "damage_dealt": damage
        })

        return damage

    def onMiss(self, function_memory:FunctionMemory, target):
        Log["debug"]["attack"]["on miss"]("\n\nattack missed!\n\n")

        if (on_miss := self.events.get("on_miss", None)) is not None:
            self.prepFunctionMemory(function_memory)

            function_memory.update({
                "target": target,
                "damage": 0
            })

            ev = function_memory.generatorEvaluateFunction(on_miss)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = None
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
        
        combat = function_memory.ref("#combat")
        
        combat.turn_summary.update({
            "attack_hit": False,
            "damage_dealt": 0
        })

        return 0

    def serialize(self):
        return {
            "abstract": Serializer.serialize(self.abstract),
            "name": Serializer.serialize(self.name),
            "damage": Serializer.serialize(self.damage),
            "range": Serializer.serialize(self.range),
            "accuracy": Serializer.serialize(self.accuracy),
            "data": Serializer.serialize(self.data),
            "events": Serializer.serialize(self.events)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

