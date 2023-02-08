# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .Util import Util
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from Util import Util

class Weapon(GameObject):
    identifier = Identifier("engine", "object/", "weapon")
    def __init__(self, abstract, name:str, damage:int, range:int, max_durability:int, durability:int, ammo_type):
        self.abstract = abstract
        self.name = name
        self.damage = damage
        self.range = range
        self.durability = durability
        self.max_durability = max_durability
        self.ammo_type = ammo_type

    def __repr__(self):
        return f"Weapon {self.name}: damage:{self.damage} range:{self.range}  durability:{self.durability}"

    def bonuses(self):
        return f"+{self.damage}dmg {self.range}ft"

    def fullStats(self, is_equipped=False):
        return f"{self.name} +{self.damage}dmg {self.range}ft {Util.getDurabilityBar(self.durability, self.max_durability)}"

    def quickStats(self):
        return f"{self.name} {Util.getDurabilityBar(self.durability, self.max_durability)}"
