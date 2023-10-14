# pylint: disable=[W,R,C,import-error]


try:
    from .Identifier import Identifier
    from .EngineDummy import Engine
    from .FunctionMemory import FunctionMemory
    from .Util import Util
    from .Logger import Log
    from .EngineOperation import _EngineOperation
except ImportError:
    from Identifier import Identifier
    from EngineDummy import Engine
    from FunctionMemory import FunctionMemory
    from Util import Util
    from Logger import Log
    from EngineOperation import _EngineOperation

import random

"""
LootTable Examples:


{
    "pools": [
        {
            "rolls": 3,
            "entries": [
                {
                    "item": {"type": "engine:weapon", "parent": "engine:weapons/sword"},
                    "count": "",
                    "cost": [1, 0, 0]
                }
            ]
        }
    ]
}


"""

class LootPool:
    def __init__(self, rolls:int, entries:list):
        self.rolls = rolls
        self.entries = entries
    
    @classmethod
    def fromList(cls, data:list):
        r = []
        for d in data:
            r.append(
                LootPool(
                    d.get("rolls", 1),
                    d.get("entries", [])
                )
            )
        return r

    def roll(self, function_memory:FunctionMemory) -> list:

        if isinstance(self.rolls, dict):
            r = random.randint(self.rolls["min"], self.rolls["max"])
        elif isinstance(self.rolls, int):
            r = self.rolls
        
        return [random.choice(self.entries) for _ in range(r)]

class LootTable:

    def __init__(self, pools:list[dict]):
        # self.rolls = rolls
        self.pools = pools

    @classmethod
    def fromDict(cls, data:dict):
        # rolls:int = data.get("rolls", 1)
        pools:list[LootPool] = LootPool.fromList(data.get("pools", []))
        return cls(pools)

    def roll(self, function_memory:FunctionMemory):
        result = []

        for pool in self.pools:
            pool: LootPool

            result += pool.roll(function_memory)

        return result


