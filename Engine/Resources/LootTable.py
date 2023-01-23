# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
except ImportError:
    from Identifier import Identifier


class LootTable:

    def __init__(self, rolls:int, pools:list[dict], weighted:bool=False):
        self.rolls = rolls
        self.pools = pools
        self.weighted = weighted

    @classmethod
    def loadTable(cls, data:dict, weighted:bool=False):
        rolls:int = data.get("rolls", 1)
        pools:list[dict] = data.get("pools", [])
        return cls(rolls, pools, weighted)



