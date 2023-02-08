# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier


class Ammo(GameObject):
    identifier = Identifier("engine", "object/", "ammo")
    def __init__(self, abstract, name:str, bonus_damage:int, max_count:int, count:int=None):
        self.abstract = abstract
        self.name = name
        self.bonus_damage = bonus_damage
        self.max_count = max_count
        self.count = count or max_count

    def __repr__(self):
        return f"Ammo {self.name}: bonus-damage:{self.bonus_damage} max-count:{self.max_count}"

    def fullStats(self, is_equipped=False):
        return f"{self.name} +{self.bonus_damage}dmg {self.count}/{self.max_count}"

    def quickStats(self):
        return f"{self.name} {self.count}/{self.max_count}"
