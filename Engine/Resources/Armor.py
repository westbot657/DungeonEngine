# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier

class Armor(GameObject):
    identifier = Identifier("engine", "object/", "armor")
    def __init__(self, abstract, name, damage_reduction, max_durability, durability):
        self.abstract = abstract
        ...

