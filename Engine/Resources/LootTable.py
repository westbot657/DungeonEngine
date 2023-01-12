# pylint: disable=[W,R,C,import-error]

try:
    from .LootPool import LootPool
    from .Identifier import Identifier
except ImportError:
    from LootPool import LootPool
    from Identifier import Identifier


class LootTable:

    def __init__(self, rolls:int, pools:list[LootPool]):
        self.rolls = rolls
        self.pools = pools



