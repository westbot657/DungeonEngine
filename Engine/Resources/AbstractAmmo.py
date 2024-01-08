# pylint: disable=[W,R,C,import-error]
try:
    from .Ammo import Ammo
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
    from .EngineDummy import Engine
    from .AbstractGameObject import AbstractGameObject
    from .DynamicValue import DynamicValue
    from .Logger import Log
    from .Loader import Loader
    from .Serializer import Serializer, Serializable
except ImportError:
    from Ammo import Ammo
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError
    from EngineDummy import Engine
    from AbstractGameObject import AbstractGameObject
    from DynamicValue import DynamicValue
    from Logger import Log
    from Loader import Loader
    from Serializer import Serializer, Serializable

import glob, json, re, random

@Serializable("AbstractAmmo")
class AbstractAmmo(AbstractGameObject):
    _loaded: dict = {}
    _link_parents: list = []
    identity: Identifier = Identifier("engine", "abstract/", "ammo")
    def __init__(self, identifier:Identifier, data:dict):
        Log["loadup"]["abstract"]["ammo"]("creating new AbstractAmmo")
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractAmmo] = []
        self.parent: AbstractAmmo|None = None

        if "parent" in data:
            AbstractAmmo._link_parents.append((self, data["parent"]))
    
        self.name: str|None = data.get("name", None)
        self.description: str|None = data.get("description", None)
        self.bonus_damage: int|None = data.get("bonus_damage", None)
        self.max_count: int|None = data.get("max_count", None)
        self.count: int|None = data.get("count", self.max_count)

        self.is_template: bool = data.get("template", False)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def getName(self):
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise InvalidObjectError(f"Ammo has no name! ({self.identifier})")
    
    def getDescription(self):
        n = self.description or (self.parent.getDescription() if self.parent else None)
        if n is not None: return n
        return ""
        # raise InvalidObjectError(f"Ammo has no name! ({self.identifier})")
    
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

    def createInstance(self, function_memory, **override_values) -> Ammo:
        if self.is_template:
            return random.choice(self.get_children()).createInstance(function_memory, **override_values)
            
        else:
            return Ammo(self,
                DynamicValue(override_values.get("name", self.getName())).getNew(function_memory),
                DynamicValue(override_values.get("description", self.getDescription())).getNew(function_memory),
                DynamicValue(override_values.get("bonus_damage", self.getBonusDamage())),
                override_values.get("max_count", self.getMaxCount()),
                DynamicValue(override_values.get("count", self.getCount())).getCachedOrNew(function_memory)
            )

    @classmethod
    def loadData(cls, engine) -> list:
        files: list[str] = glob.glob("**/ammo/*.json", recursive=True)

        Log["loadup"]["abstract"]["ammo"](f"found {len(files)} ammo file{'s' if len(files) != 1 else ''}")
        for file in files:
            file: str
            Log["loadup"]["abstract"]["ammo"](f"loading AbstractAmmo from '{file}'")
            # with open(file, "r+", encoding="utf-8") as f:
            #     data = json.load(f)
            data = Loader.load(file)
            
            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        Log["loadup"]["abstract"]["ammo"]("linking AbstractAmmo parents...")
        for a, p in cls._link_parents:
            a: AbstractAmmo
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is a:
                    Log["ERROR"]["loadup"]["abstract"]["ammo"]("cannot set object as it's own parent")
                    continue
                elif parent in a.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["ammo"]("circular parent loop found")
                    continue
                a._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["ammo"](f"parent does not exist: '{p}'")
        
        Log["loadup"]["abstract"]["ammo"]("verifying AbstractAmmo completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "ammo")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractAmmo
            if o.is_template:
                Log.success()
                continue
            try:
                o.getName()
                o.getBonusDamage()
                o.getMaxCount()
                Log.success()
            except InvalidObjectError as err:
                e: AbstractAmmo = cls._loaded.pop(l)
                Log.ERROR("loadup", "abstract", "ammo", f"failed to load ammo: {e.identifier}. {err}")

        Log.end_track()

        cls._link_parents.clear()

        Log["loadup"]["abstract"]["ammo"]("AbstractAmmo loading complete")
        return cls._loaded

    def serialize(self):
        return {
            "identifier": Serializer.serialize(self.identifier),
            "name": Serializer.serialize(self.name),
            "description": Serializer.serialize(self.description),
            "bonus_damage": Serializer.serialize(self.bonus_damage),
            "max_count": Serializer.serialize(self.max_count),
            "count": Serializer.serialize(self.count),
            "parent": Serializer.serialize(self.parent)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)


if __name__ == "__main__":
    print(AbstractAmmo.loadData(None))
