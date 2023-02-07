# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .Util import Util
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from Util import Util

class Armor(GameObject):
    identifier = Identifier("engine", "object/", "armor")
    def __init__(self, abstract, name, damage_reduction, max_durability, durability):
        self.abstract = abstract
        self.name = name
        self.damage_reduction = damage_reduction
        self.max_durability = max_durability
        self.durability = durability

    def fullStats(self, is_equipped=False):
        return f"{self.name} -{self.damage_reduction}dmg {Util.getDurabilityBar(self.durability, self.max_durability)}" + (" [WEARING]" if is_equipped else "")

