# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Weapon import Weapon
    from .AbstractAmmo import AbstractAmmo
    from .EngineErrors import InvalidObjectError
    from .EngineDummy import Engine
    from .AbstractGameObject import AbstractGameObject
except ImportError:
    from Identifier import Identifier
    from Weapon import Weapon
    from AbstractAmmo import AbstractAmmo
    from EngineErrors import InvalidObjectError
    from EngineDummy import Engine
    from AbstractGameObject import AbstractGameObject

import glob, json

""" example_dungeon:weapon/longsword
{
    "parent": "engine:weapon/sword",
    "name": "Longsword",
    "damage": 3,
    "range": 2,
    "max_durability": 100,
    "durability": 100,
    "ammo_type": "engine:ammo/none"
}
"""

class AbstractWeapon(AbstractGameObject):
    _loaded: dict = {}
    _link_parents = []
    identifier: Identifier = Identifier("engine", "abstract/", "weapon")
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractWeapon] = []
        self.parent: AbstractWeapon|None = None

        if "parent" in data:
            AbstractWeapon._link_parents.append((self, data["parent"]))

        self.name: str|None = data.get("name", None)
        self.damage: int|None = data.get("damage", None)
        self.range: int|None = data.get("range", None)
        self.max_durability: int|None = data.get("max_durability", None)
        self.durability: int|None = data.get("durability", self.max_durability)

        self.ammo_type: str|None = data.get("ammo_type", None)

        self.is_template: bool = data.get("template", False)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def getName(self) -> str:
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise InvalidObjectError(f"Weapon has no name! ({self.identifier})")
    
    def getDamage(self) -> int:
        if self.damage is None:
            d = self.parent.getDamage() if self.parent else None
        else:
            d = self.damage
        if d is not None: return d
        raise InvalidObjectError(f"Weapon has no damage! ({self.identifier})")

    def getRange(self) -> int:
        if self.range is None:
            r = self.parent.getRange() if self.parent else None
        else:
            r = self.range
        if r is not None: return r
        raise InvalidObjectError(f"Weapon has no range! ({self.identifier})")
    
    def getMaxDurability(self) -> int:
        if self.max_durability is None:
            d = self.parent.getMaxDurability() if self.parent else None
        else:
            d = self.max_durability
        if d is not None: return d
        raise InvalidObjectError(f"Weapon has no max_durability! ({self.identifier})")

    def getDurability(self) -> int:
        if self.durability is None:
            d = self.parent.getDurability() if self.parent else None
        else:
            d = self.durability
        if d is not None: return d
        raise InvalidObjectError(f"Weapon has no durability! ({self.identifier})")

    def getAmmoType(self) -> AbstractAmmo:
        if self.ammo_type is None:
            if self.parent and ((a := self.parent.getAmmoType()) is not None):
                return a
            return AbstractAmmo._loaded["engine:ammo/none"]
        return AbstractAmmo._loaded["engine:ammo/none"]

    def get_children(self, depth:int=-1): # recursive way to get a flat list of all sub children to some depth
        children = []
        for child in self.children:
            children.append(child)
            if depth != 0:
                children += child.get_children(depth-1)
        return children

    def createWeapon(self, **value_overrides) -> Weapon:
        if self.is_template:
            ...
        else:
            return Weapon(self,
                value_overrides.get("name", self.getName()),
                value_overrides.get("damage", self.getDamage()),
                value_overrides.get("range", self.getRange()),
                value_overrides.get("max_durability", self.getMaxDurability()),
                value_overrides.get("durability", self.getDurability()),
                value_overrides.get("ammo_type", self.getAmmoType())
            )

    @classmethod
    def loadData(cls, engine:Engine) -> list:
        files: list[str] = glob.glob("**/weapons/*.json", recursive=True)
        #print(files)
        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

            # if m := re.match(r"Dungeons/(?P<namespace>[^/]+)/resources/(?P<path>(?:[^/]+/)+)(?P<name>[a-z0-9_]+)\.json", file):
            #     d: dict = m.groupdict()
            #     namespace:str = d["namespace"]
            #     path: str = d["path"]
            #     name: str = d["name"]
            #     cls._loaded.update({f"{namespace}:weapons/{name}": cls(Identifier(namespace, path, name), data)})

            # elif m := re.match(r"resources/weapons/(?P<name>[a-z0-9_]+)\.json", file):
            #     d: dict = m.groupdict()
            #     name: str = d["name"]
            #     cls._loaded.update({f"engine:weapons/{name}": cls(Identifier("engine", "weapons/", name), data)})

        for w, p in cls._link_parents:
            w: AbstractWeapon
            p: str
            w._set_parent(cls._loaded.get(p))

        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractWeapon
            try:
                o.getName()
                o.getRange()
                o.getDamage()
                o.getMaxDurability()
                o.getDurability()
                o.getAmmoType()
            except InvalidObjectError as err:
                e: AbstractWeapon = cls._loaded.pop(l)
                print(f"Failed to load weapon: {e.identifier}  {err}")

        return cls._loaded

if __name__ == "__main__":
    print(AbstractWeapon.loadData(None))
