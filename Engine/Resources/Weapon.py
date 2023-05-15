# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .Util import Util
    from .FunctionMemory import FunctionMemory
    from .EngineOperation import _EngineOperation
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from Util import Util
    from FunctionMemory import FunctionMemory
    from EngineOperation import _EngineOperation

class Weapon(GameObject):
    identifier = Identifier("engine", "object/", "weapon")
    def __init__(self, abstract, name:str, damage:DynamicValue, range:DynamicValue, max_durability:int, durability:int, ammo_type, events:dict):
        self.abstract = abstract
        self.name = name
        self.damage = damage
        self.range = range
        self.durability = durability
        self.max_durability = max_durability
        self.ammo_type = ammo_type
        self.events = events

        self.owner = None

    def __repr__(self):
        return f"Weapon {self.name}: damage:{self.damage} range:{self.range}  durability:{self.durability}"

    def bonuses(self, function_memory:FunctionMemory):
        return f"+{self.damage.quickDisplay(function_memory)}dmg {self.range.quickDisplay(function_memory)}ft"

    def fullStats(self, function_memory:FunctionMemory, is_equipped=False):
        return f"{self.name} +{self.damage.fullDisplay(function_memory)}dmg {self.range.fullDisplay(function_memory)}ft {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [EQUIPPED]" if is_equipped else "")

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"

    def getLocalVariables(self) -> dict:
        d = {}
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

    def onUse(self, function_memory:FunctionMemory):
        if on_use := self.events.geT("on_use", None):
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

            self.postEvaluate(function_memory)

    def onDamage(self, function_memory:FunctionMemory):
        if on_damage := self.events.geT("on_damage", None):
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
        if on_break := self.events.geT("on_break", None):
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

    def onAttack(self, function_memory:FunctionMemory):
        if on_attack := self.events.geT("on_attack", None):
            self.prepFunctionMemory(function_memory)

            ev = function_memory.generatorEvaluateFunction(on_attack)
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
        if on_equip := self.events.geT("on_equip", None):
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
        if on_unequip := self.events.geT("on_unequip", None):
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
        if on_repair := self.events.geT("on_repair", None):
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



