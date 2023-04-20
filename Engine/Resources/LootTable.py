# pylint: disable=[W,R,C,import-error]


try:
    from .Identifier import Identifier
    from .EngineDummy import Engine
    from .FunctionMemory import FunctionMemory
    from .Util import Util
    from .Logger import Log
except ImportError:
    from Identifier import Identifier
    from EngineDummy import Engine
    from FunctionMemory import FunctionMemory
    from Util import Util
    from Logger import Log

import random

class LootEntry:
    def __init__(self, data):
        self.data = data

    @classmethod
    def fromList(cls, data:list):
        r = []
        for d in data:
            r.append(cls(d))
        return r

    def calcWeight(self, function_memory:FunctionMemory, curr_weight:float, num_entries_calculated:int, num_entries_total:int) -> float:
        if weight := self.data.get("weight", None): # all entries with specified weight should be calculated before ones with unspecified
            Log["debug"]["fishing rod"](f"weight: {weight}")
            weight = function_memory.evaluateFunction(weight)
            if curr_weight + weight > 1.0:
                raise Exception(f"Weighted LootTable has too much weight! ({curr_weight} + {weight} = {curr_weight+weight})")
                
            return curr_weight + weight
        else:
            weight = (1 - curr_weight) / (num_entries_total - num_entries_calculated)
            return min(curr_weight + weight, 1.0) # min() just in case the last one decides that 0.9 + 0.1 => 1.000000000001 or something stupid


class LootPool:
    def __init__(self, bonus_rolls:int, entries:list[LootEntry]):
        self.bonus_rolls = bonus_rolls
        self.entries = entries
    
    @classmethod
    def fromList(cls, data:list):
        r = []
        for d in data:
            r.append(cls(d.get("bonus_rolls", 0), LootEntry.fromList(d.get("entries", []))))
        return r

    def roll(self, function_memory:FunctionMemory) -> list:
        weighted_entries = [entry for entry in self.entries if "weight" in entry.data]
        unspecified_entries = [entry for entry in self.entries if entry not in weighted_entries]

        weight = 0
        calculated = 0
        total_entries = len(self.entries)
        entries = weighted_entries + unspecified_entries

        weighted = {}

        for entry in entries:
            
            w = entry.calcWeight(function_memory, weight, calculated, total_entries)
            if w in weighted or w == 0:
                continue # entry weight is 0, so it can't be picked anyways
            weighted.update({w: entry})
            weight = w
            calculated += 1

        f = random.randint(0, 10000) / 10000
        choice = Util.getRoundedUpKey(f, weighted)

        entry:LootEntry = weighted.get(choice)
        return function_memory.evaluateFunction(entry.data), self.bonus_rolls

class LootTable:

    def __init__(self, rolls:int, pools:list[dict]):
        self.rolls = rolls
        self.pools = pools

    @classmethod
    def fromDict(cls, data:dict):
        rolls:int = data.get("rolls", 1)
        pools:list[LootPool] = LootPool.fromList(data.get("pools", []))
        return cls(rolls, pools)

    def roll(self, function_memory:FunctionMemory):
        result = []
        roll = 0
        while roll < self.rolls:
            for pool in self.pools:
                pool: LootPool
                r_b = pool.roll(function_memory)
                r, b = r_b
                if r:
                    result.append(r)
                    roll -= b
            roll += 1

        return result


