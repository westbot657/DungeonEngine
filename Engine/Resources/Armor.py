# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
    from .Util import Util
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue
    from Util import Util

class Armor(GameObject):
    identifier = Identifier("engine", "object/", "armor")
    def __init__(self, abstract, name:str, damage_reduction:DynamicValue, max_durability:int, durability:int):
        self.abstract = abstract
        self.name = name
        self.damage_reduction = damage_reduction
        self.max_durability = max_durability
        self.durability = durability

    def bonuses(self, engine):
        return f"+{self.damage_reduction.quickDisplay(engine)}def"

    def quickStats(self, engine):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"

    def fullStats(self, engine, is_equipped=False):
        return f"{self.name} +{self.damage_reduction.fullDisplay(engine)}def {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [WEARING]" if is_equipped else "")

