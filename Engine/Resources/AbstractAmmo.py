# pylint: disable=[W,R,C,import-error]
try:
    from .Ammo import Ammo
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
    from .AbstractGameObject import AbstractGameObject
except ImportError:
    from Ammo import Ammo
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError
    from AbstractGameObject import AbstractGameObject

import glob, json, re

class AbstractAmmo(AbstractGameObject):
    _loaded: dict = {}
    _link_parents: list = []
    identifier: Identifier = Identifier("engine", "abstract/", "ammo")
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractAmmo] = []
        self.parent: AbstractAmmo|None = None

        if "parent" in data:
            AbstractAmmo._link_parents.append((self, data["parent"]))
    
        self.name: str|None = data.get("name", None)
        self.bonus_damage: int|None = data.get("bonus_damage", "None")
        self.max_count: int|None = data.get("max_count", None)
        self.count: int|None = data.get("count", self.max_count)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def getName(self):
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise InvalidObjectError(f"Ammo has no name! ({self.identifier})")
    
    def getBonusDamage(self):
        if self.bonus_damage is None:
            b = self.parent.getBonusDamage() if self.parent else None
        else:
            b = self.bonus_damage
        if b is not None:
            return b
        raise InvalidObjectError(f"Ammo has no bonus-damage! ({self.identifier})")
    
    def getMaxCount(self):
        if self.max_count is None:
            b = self.parent.getMaxCount() if self.parent else None
        else:
            b = self.max_count
        if b is not None:
            return b
        raise InvalidObjectError(f"Ammo has no max-count! ({self.identifier})")

    def getCount(self):
        if self.count is None:
            b = self.parent.getCount() if self.parent else None
        else:
            b = self.count
        if b is not None:
            return b
        raise InvalidObjectError(f"Ammo has no max-count! ({self.identifier})")

    def is_parent_of(self, other):
        p = other
        while p is not None:
            if self == p:
                return True
            p = p.parent
        return False
    
    def inherets_from(self, other):
        p = self
        while p is not None:
            if p == other:
                return True
            p = p.parent
        return False

    def createAmmo(self, **override_values) -> Ammo:
        return Ammo(self,
            override_values.get("name", self.getName()),
            override_values.get("bonus_damage", self.getBonusDamage()),
            override_values.get("max_count", self.getMaxCount()),
            override_values.get("count", self.getCount())
        )

    @classmethod
    def loadData(cls, inline_handler) -> list:
        files: list[str] = glob.glob("**/ammo/*.json", recursive=True)

        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)
            
            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

            # if m := re.match(r"Dungeons/(?P<namespace>[^/]+)/resources/(?P<path>(?:[^/]+/)+)(?P<name>[a-z0-9_]+)\.json", file):
            #     d: dict = m.groupdict()
            #     namespace:str = d["namespace"]
            #     path: str = f"Dungeons/{namespace}/resources/{d['path']}"
            #     name: str = d["name"]
            #     cls._loaded.update({f"{namespace}:ammo/{name}": cls(Identifier(namespace, path, name), data)})

            # elif m := re.match(r"resources/ammo/(?P<name>[a-z0-9_]+)\.json", file):
            #     d: dict = m.groupdict()
            #     name: str = d["name"]
            #     cls._loaded.update({f"engine:ammo/{name}": cls(Identifier("engine", "resources/ammo/", name), data)})

        for a, p in cls._link_parents:
            a: AbstractAmmo
            p: str
            a._set_parent(cls._loaded.get(p))
        
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractAmmo
            try:
                o.getName()
                o.getBonusDamage()
                o.getMaxCount()
            except InvalidObjectError:
                e: AbstractAmmo = cls._loaded.pop(l)
                print(f"Failed to load ammo: {e.identifier}")

        return cls._loaded


if __name__ == "__main__":
    print(AbstractAmmo.loadData(None))
