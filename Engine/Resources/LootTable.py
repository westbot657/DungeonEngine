# pylint: disable=[W,R,C,import-error]

try:
    from .LootPool import LootPool
    from .Identifier import Identifier
except ImportError:
    from LootPool import LootPool
    from Identifier import Identifier


class LootTable:

    def __init__(self, abstract, rolls:int, pools:list[LootPool]):
        self.abstract = abstract
        self.rolls = rolls
        self.pools = pools



