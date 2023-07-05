# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionMemory import FunctionMemory
    from .FunctionalElement import FunctionalElement
    from .DynamicValue import DynamicValue
    from .EngineOperation import _EngineOperation
except ImportError:
    from FunctionMemory import FunctionMemory
    from FunctionalElement import FunctionalElement
    from DynamicValue import DynamicValue
    from EngineOperation import _EngineOperation

import random

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
        print("\n\nAttack.onAttack() called!\n\n")
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
                v = e.value or v
        return v

    def onHit(self, function_memory:FunctionMemory, target):
        print("\n\nattack hit!\n\n")
        print(self.damage)
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
        
        return damage

    def onMiss(self, function_memory:FunctionMemory, target):
        print("\n\nattack missed!\n\n")

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



