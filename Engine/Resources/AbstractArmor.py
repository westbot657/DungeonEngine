# pylint: disable=[W,R,C,import-error]

from .Armor import Armor
from .Identifier import Identifier
from .EngineErrors import InvalidObjectError
from .EngineDummy import Engine
from .AbstractGameObject import AbstractGameObject
from .DynamicValue import DynamicValue
from .Logger import Log
from .Loader import Loader
from .Serializer import Serializer, Serializable

import glob, json, re, random

from mergedeep import merge

@Serializable("AbstractArmor")
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
        self.description: str|None = data.get("description", None)
        self.max_durability: int = data.get("max_durability", None)
        self.durability: int = data.get("durability", self.max_durability)
        self.damage_reduction: int = data.get("damage_reduction", None)
        self.events: dict = data.get("events", {})

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
    
    def getDescription(self) -> str:
        n = self.description or (self.parent.getDescription() if self.parent else None)
        if n is not None: return n
        return ""
    
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

    def getEvents(self) -> dict:
        return merge({}, self.parent.getEvents() if self.parent else {}, self.events)

    def createInstance(self, function_memory, **override_values) -> Armor:
        if self.is_template:
            return random.choice(self.get_children()).createInstance(function_memory, **override_values)
            
        else:
            return Armor(self,
                DynamicValue(override_values.get("name", self.getName())).getNew(function_memory),
                DynamicValue(override_values.get("description", self.getDescription())).getNew(function_memory),
                DynamicValue(override_values.get("damage_reduction", self.getDamageReduction())),
                override_values.get("max_durability", self.getMaxDurability()),
                DynamicValue(override_values.get("durability", self.getDurability())).getCachedOrNew(function_memory),
                self.getEvents()
            )

    @classmethod
    def loadData(cls, engine) -> list:
        files: list[str] = glob.glob("**/armor/*.json", recursive=True)
        
        Log["loadup"]["abstract"]["armor"](f"found {len(files)} armor file{'s' if len(files) != 1 else ''}")
        for file in files:
            file: str
            Log["loadup"]["abstract"]["armor"](f"loading AbstractArmor from '{file}'")
            data = Loader.load(file)

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
        
        Log["loadup"]["abstract"]["armor"]("verifying AbstractArmor completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "armor")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractArmor
            try:
                o.getName()
                o.getDamageReduction()
                o.getMaxDurability()
                o.getDurability()
                Log.success()
            except InvalidObjectError:
                e: AbstractArmor = cls._loaded.pop(l)
                Log.ERROR("loadup", "abstract", "armor", f"failed to load armor: {e.identifier}")

        Log.end_track()

        cls._link_parents.clear()

        Log["loadup"]["abstract"]["armor"]("AbstractArmor loading complete")
        return cls._loaded

    def serialize(self):
        return {
            "name": Serializer.serialize(self.name),
            "description": Serializer.serialize(self.description),
            "max_durability": Serializer.serialize(self.max_durability),
            "durability": Serializer.serialize(self.durability),
            "damage_reduction": Serializer.serialize(self.damage_reduction),
            "events": Serializer.serialize(self.events)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)



if __name__ == "__main__":
    ...


