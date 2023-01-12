# pylint: disable=[W,R,C,import-error]

try:
    from .LootTable import LootTable
    from .LootPool import LootPool
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
except ImportError:
    from LootTable import LootTable
    from LootPool import LootPool
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError

import glob, json, re

"""
<id>.json
{
    "entries": [
        {
            "item": "<namespace>:<category>/<item>",
            "<item attribute>": <override value>,
            "<item attribute>": {
                "function": "random",
                "type": "uniform",
                "min": <int>,
                "max": <int>
            },
            "<item attribute>": {
                "function": "random",
                "type": "uniform",
                "choices": [
                    ...
                ]
            }
        }
    ],
    "rolls": {
        "type": "uniform",
        "min": <int>,
        "max": <int>
    }
}
"""

class AbstractLootTable:
    _loaded = {}
    _link_parents = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.parent: AbstractLootTable|None = None
        self.children: list[AbstractLootTable] = []

        if "parent" in data:
            AbstractLootTable._link_parents.append((self, data["parent"]))

        self.rolls: int|None = data.get("rolls", None)
        self.pools: list[dict]|None = data.get("pools", None)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def getRolls(self) -> int:
        if self.rolls is None:
            if self.parent: return self.parent.getRolls()
            raise InvalidObjectError(f"LootTable has no rolls!  ({self.identifier})")
        if self.rolls < 0: raise InvalidObjectError(f"LootTable has invalid rolls! ({self.rolls})  ({self.identifier})")
        return self.rolls
    
    def getPools(self) -> list[LootPool]:
        ...

    def loadPools(self, pools:list) -> list[LootPool]:
        if isinstance(pools, list):
            new = []
            for pool in pools:
                if isinstance(pool, LootPool):
                    new.append(pool)
                elif isinstance(pool, dict):
                    if any(key in pool for key in ["rolls", "entries"]):
                        ...

            return new
            

    def createLootTable(self, **override_values) -> LootTable:
        # probably check that pools (if given) is valid/needs to be converted from json
        return LootTable(
            override_values.get("rolls", self.getRolls()),
            self.loadPools(override_values.get("pools", self.getPools()))
        )

    @classmethod
    def loadData(cls) -> list:
        files: list[str] = glob.glob("**/loot_tables/*.json", recursive=True)

        for file in files:
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)
            
            if m := re.match(r"Dungeons/(?P<namespace>[^/]+)/resources/(?P<path>(?:[^/]+/)+)(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                namespace:str = d["namespace"]
                path: str = d["path"]
                name: str = d["name"]
                cls._loaded.update({f"{namespace}:loot_tables/{name}": cls(Identifier(namespace, path, name), data)})

            elif m := re.match(r"resources/loot_tables/(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                name: str = d["name"]
                cls._loaded.update({f"engine:loot_tables/{name}": cls(Identifier("engine", "resources/loot_tables/", name), data)})

        for w, p in cls._link_parents:
            w: AbstractLootTable
            p: str
            w._set_parent(cls._loaded.get(p))

        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractLootTable
            try:
                pass # call getters
            except InvalidObjectError:
                e: AbstractLootTable = cls._loaded.pop(l)
                print(f"Failed to load loot_table: {e.identifier}")

        return cls._loaded



