# pylint: disable=[W,R,C,import-error]

try:
    from .Armor import Armor
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
    from .EngineDummy import Engine
    from .AbstractGameObject import AbstractGameObject
    from .DynamicValue import DynamicValue
    from .Logger import Log
except ImportError:
    from Armor import Armor
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError
    from EngineDummy import Engine
    from AbstractGameObject import AbstractGameObject
    from DynamicValue import DynamicValue
    from Logger import Log

import glob, json, re

class AbstractArmor(AbstractGameObject):
    _loaded: dict = {}
    _link_parents:list = []
    identity: Identifier = Identifier("engine", "abstract/", "armor")
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

        self.is_template: bool = data.get("template", False)

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

    def createInstance(self, engine:Engine, **override_values) -> Armor:
        if self.is_template:
            ...
        else:
            return Armor(self,
                override_values.get("name", self.getName()),
                DynamicValue(override_values.get("damage_reduction", self.getDamageReduction())),
                override_values.get("max_durability", self.getMaxDurability()),
                DynamicValue(override_values.get("durability", self.getDurability())).getCachedOrNew(engine)
            )

    @classmethod
    def loadData(cls, inline_handler) -> list:
        files: list[str] = glob.glob("**/armor/*.json", recursive=True)
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
            #     cls._loaded.update({f"{namespace}:armor/{name}": cls(Identifier(namespace, path, name), data)})

            # elif m := re.match(r"resources/armor/(?P<name>[a-z0-9_]+)\.json", file):
            #     d: dict = m.groupdict()
            #     name: str = d["name"]
            #     cls._loaded.update({f"engine:armor/{name}": cls(Identifier("engine", "resources/armor/", name), data)})

        Log["loadup"]["abstract"]["armor"]("linking AbstractArmor parents...")
        for a, p in cls._link_parents:
            a: AbstractArmor
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is a:
                    Log["ERROR"]["loadup"]["abstract"]["armor"]("cannot set object as it's own parent")
                    continue
                elif parent in a.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["armor"]("circular parent loop found")
                    continue
                a._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["armor"](f"parent does not exist: '{p}'")
        
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


