# pylint: disable=[W,R,C,import-error]


try:
    from .Identifier import Identifier
    from .EngineDummy import Engine
except ImportError:
    from Identifier import Identifier
    from EngineDummy import Engine


class LootEntry:
    def __init__(self, data):
        self.data = data

    def calcWeight(self, engine:Engine, curr_weight:float, num_entries:int) -> float:
        if weight := self.data.get("weight", None):
            if isinstance(weight, dict):
                weight = engine.evaluateFunction(engine, weight)


class LootPool:
    def __init__(self, bonus_rolls:int, entries:list[LootEntry]):
        self.bonus_rolls = bonus_rolls
        self.entries = entries
    
    def roll(self, engine:Engine) -> list:
        

class LootTable:

    def __init__(self, rolls:int, pools:list[dict]):
        self.rolls = rolls
        self.pools = pools
        

    @classmethod
    def loadTable(cls, data:dict):
        rolls:int = data.get("rolls", 1)
        pools:list[dict] = data.get("pools", [])
        return cls(rolls, pools)



