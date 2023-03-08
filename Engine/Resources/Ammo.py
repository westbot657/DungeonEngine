# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .DynamicValue import DynamicValue
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from DynamicValue import DynamicValue


class Ammo(GameObject):
    identifier = Identifier("engine", "object/", "ammo")
    def __init__(self, abstract, name:str, bonus_damage:DynamicValue, max_count:int, count:int=None):
        self.abstract = abstract
        self.name = name
        self.bonus_damage = bonus_damage
        self.max_count = max_count
        self.count = count or max_count # this will make None and 0 set the amount to max (0 is included so that you can't have a stack of no ammo)

    def __repr__(self):
        return f"Ammo {self.name}: bonus-damage:{self.bonus_damage} max-count:{self.max_count}"

    def fullStats(self, engine, is_equipped=False):
        return f"{self.name} +{self.bonus_damage.fullDisplay(engine)}dmg {self.count}/{self.max_count}"

    def quickStats(self, engine):
        return f"{self.name} {self.count}/{self.max_count}"
