# pylint: disable=[W,R,C,import-error]

from .Identifier import Identifier
from .Weapon import Weapon

import glob, json, re


class AbstractWeapon:
    _loaded: dict = {}
    _link_parents = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self.children = []

        self.parent = None
        if "parent" in data:
            AbstractWeapon._link_parents.append((self, data["parent"]))

        self.name: str|None = data.get("name", None)
        self.damage: int|None = data.get("damage", None)
        self.range: int|None = data.get("range", None)
        self.durability: int|None = data.get("durability", None)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def getName(self) -> str:
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise Exception(f"Weapon has no name! ({self.identifier})")
    
    def getDamage(self) -> int:
        if self.damage is None:
            d = self.parent.getDamage() if self.parent else None
        else:
            d = self.damage
        if d is not None: return d
        raise Exception(f"Weapon has no damage! ({self.identifier})")

    def getRange(self) -> int:
        if self.range is None:
            r = self.parent.getRange() if self.parent else None
        else:
            r = self.range
        if r is not None: return r
        raise Exception(f"Weapon has no range! ({self.identifier})")
    
    def getDurability(self) -> int:
        if self.durability is None:
            d = self.parent.getDamage() if self.parent else None
        else:
            d = self.damage
        if d is not None: return d
        raise Exception(f"Weapon has no durability! ({self.identifier})")

    def createWeapon(self, **value_overrides) -> Weapon:
        return Weapon(
            value_overrides.get("name", self.getName()),
            value_overrides.get("damage", self.getDamage()),
            value_overrides.get("range", self.getRange()),
            value_overrides.get("durability", self.getDurability())
        )

    @classmethod
    def loadData(cls) -> list:
        files: list[str] = glob.glob("**/weapons/*.json", recursive=True)
        #print(files)
        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            if m := re.match(r"Dungeons/(?P<namespace>[^/]+)/resources/(?P<path>(?:[^/]+/)+)(?P<name>[a-z0-9_]+)\.json", file):
                d: dict = m.groupdict()
                namespace:str = d["namespace"]
                path: str = d["path"]
                name: str = d["name"]
                cls._loaded.update({f"{namespace}:weapons/{name}": cls(Identifier(namespace, path, name), data)})

        for w, p in cls._link_parents:
            w: AbstractWeapon
            p: str
            w._set_parent(cls._loaded.get(p))

        return cls._loaded


if __name__ == "__main__":
    print(AbstractWeapon.loadData())
