# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .FunctionMemory import FunctionMemory
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from FunctionMemory import FunctionMemory


class Ammo(GameObject):
    identifier = Identifier("engine", "object/", "ammo")
    def __init__(self, abstract, name:str, bonus_damage:DynamicValue, max_count:int, count:int=None):
        self.abstract = abstract
        self.name = name
        self.bonus_damage = bonus_damage
        self.max_count = max_count
        self.count = count or max_count # this will make None and 0 set the amount to max (0 is included so that you can't have a stack of no ammo)

        self.owner = None

    def __repr__(self):
        return f"Ammo {self.name}: bonus-damage:{self.bonus_damage} max-count:{self.max_count}"

    def fullStats(self, function_memory:FunctionMemory, is_equipped=False):
        return f"{self.name} +{self.bonus_damage.fullDisplay(function_memory)}dmg {self.count}/{self.max_count}"

    def quickStats(self, function_memory:FunctionMemory):
        return f"{self.name} {self.count}/{self.max_count}"

    def getLocalVariables(self) -> dict:
        return {}

    def updateLocalVariables(self, locals: dict):
        ...

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#ammo": self
        })
        function_memory.update(self.getLocalVariables())

    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    # on_load: when ammo is loaded into a weapon
    def onLoad(self, function_memory:FunctionMemory):
        ...

    # on_unload: when ammo is unloaded from a weapon
    def onUnload(self, function_memory:FunctionMemory):
        ...
    
    # when weapon is used to fire ammo
    def onFire(self, function_memory:FunctionMemory):
        ...

    def onHit(self, function_memory:FunctionMemory):
        ...
    
    def onMiss(self, function_memory:FunctionMemory):
        ...

    def _get_save(self, function_memory:FunctionMemory):
        d = {
            "type": "engine:ammo",
            "parent": self.abstract.identifier.full()
        }

        if self.name != self.abstract.getName():
            d.update({"name": self.name})
        if self.bonus_damage != self.abstract.getBonusDamage():
            d.update({"bonus_damage": self.bonus_damage})
        if self.max_count != self.abstract.getMaxCount():
            d.update({"max_count": self.max_count})
        if self.count != self.abstract.getCount():
            d.update({"count": self.count})
        return d

