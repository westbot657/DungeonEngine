# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .Util import Util
    from .FunctionMemory import FunctionMemory
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from Util import Util
    from FunctionMemory import FunctionMemory

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
        d = {}

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
        ...
    def onUnequip(self, function_memory:FunctionMemory):
        ...
    def onDamaged(self, function_memory:FunctionMemory):
        ...
    def onBroken(self, function_memory:FunctionMemory):
        ...

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
