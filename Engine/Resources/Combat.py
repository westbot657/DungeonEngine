# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractEnemy import AbstractEnemy, Enemy
except ImportError:
    from AbstractEnemy import AbstractEnemy, Enemy



from enum import Enum, auto


class Combat:

    class Style(Enum):
        SEQUENCED = auto()
        BASIC = auto()

    def __init__(self, abstract, enemies:list[Enemy], sequence:dict, data:dict):
        self.abstract = abstract
        self.enemies = enemies
        self.sequence = sequence
        self.data = data

