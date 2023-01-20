# pylint: disable=[W,R,C,import-error]

try:
    from .Armor import Armor
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
except ImportError:
    from Armor import Armor
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError

import glob, json, re

class AbstractArmor:
    _loaded: dict = {}
    _link_parents:list = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data

        self.parent: AbstractArmor|None = None
        self.children: list[AbstractArmor] = []

        if "parent" in data:
            AbstractArmor._link_parents.append((self, data["parent"]))
        
        self.name: str = data.get("name", None)
        self.max_durability: int = data.get("max_durability", None)
        self.durability: int = data.get("durability", self.max_durability)
        self.damage_reduction: int = data.get("damage_reduction", None)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def getName(self) -> str:
        if self.name is None:
            n = self.parent.getName() if self.parent else None
        else:
            n = self.name
        if n is not None:
            return n
        raise InvalidObjectError(f"Armor has no name! ({self.identifier})")
    
    def getMaxDurability(self) -> int:
        if self.max_durability is None:
            d = self.parent.getMaxDurability() if self.parent else None
        else:
            d = self.max_durability
        if d is not None:
            return d
        raise InvalidObjectError(f"Armor has no max_durability! ({self.identifier})")
    
    def getDurability(self) -> int:
        if self.durability is None:
            d = self.parent.getDurability() if self.parent else None
        else:
            d = self.durability
        if d is not None:
            return d
        raise InvalidObjectError(f"Armor has no durability! ({self.identifier})")

    def getDamageReduction(self) -> int:
        if self.damage_reduction is None:
            d = self.parent.getDamageReduction() if self.parent else None
        else:
            d = self.damage_reduction
        if d is not None:
            return d
        raise InvalidObjectError(f"Armor has no damage_reduction! ({self.identifier})")

    def createArmor(self, **override_values) -> Armor:
        return Armor(self,
            override_values.get("name", self.getName()),
            override_values.get("damage_reduction", self.getDamageReduction()),
            override_values.get("max_durability", self.getMaxDurability()),
            override_values.get("durability", self.getDurability())
        )

    @classmethod
    def loadData(cls, inline_handler) -> list:
        files: list[str] = glob.glob("**/armor/*.json", recursive=True)
        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            if m := re.match(r"Dungeons/(?P<namespace>[^/]+)/resources/(?P<path>(?:[^/]+/)+)(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                namespace:str = d["namespace"]
                path: str = d["path"]
                name: str = d["name"]
                cls._loaded.update({f"{namespace}:armor/{name}": cls(Identifier(namespace, path, name), data)})

            elif m := re.match(r"resources/armor/(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                name: str = d["name"]
                cls._loaded.update({f"engine:armor/{name}": cls(Identifier("engine", "resources/armor/", name), data)})

        for a, p in cls._link_parents:
            a: AbstractArmor
            p: str
            a._set_parent(cls._loaded.get(p))
        
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractArmor
            try:
                o.getName()
                o.getDamageReduction()
                o.getMaxDurability()
                o.getDurability()
            except InvalidObjectError:
                e: AbstractArmor = cls._loaded.pop(l)
                print(f"Failed to load armor: {e.identifier}")

        return cls._loaded


if __name__ == "__main__":
    ...


