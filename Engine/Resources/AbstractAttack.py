# pylint: disable=[W,R,C,import-error]

from .Identifier import Identifier
from .AbstractGameObject import AbstractGameObject
from .Attack import Attack
from .EngineErrors import InvalidObjectError
from .DynamicValue import DynamicValue
from .Logger import Log
from .FunctionMemory import FunctionMemory
from .Loader import Loader
from .Serializer import Serializer, Serializable

import glob, json, random

@Serializable("AbstractAttack")
class AbstractAttack(AbstractGameObject):
    _loaded = {}
    _link_parents = []
    identity = Identifier("engine", "abstract/", "attack")
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractAttack] = []
        self.parent: AbstractAttack|None = None

        if "parent" in data:
            AbstractAttack._link_parents.append((self, data["parent"]))

        self.name: str|None = data.get("name", None)
        self.range: int|None = data.get("range", None)
        self.damage: int|dict|None = data.get("damage", None)
        self.accuracy: int|None = data.get("accuracy", None)

        self.data: dict = data.get("data", {})
        self.events: dict = data.get("events", {})

        self.is_template = data.get("is_template", False)

    def getName(self):
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise InvalidObjectError(f"Attack has no name! ({self.identifier})")
    
    def getDamage(self) -> int|dict:
        if self.damage is None:
            d = self.parent.getDamage() if self.parent else None
        else:
            d = self.damage
        if d is not None: return d
        raise InvalidObjectError(f"Attack has no damage! ({self.identifier})")

    def getRange(self) -> int:
        if self.range is None:
            r = self.parent.getRange() if self.parent else None
        else:
            r = self.range
        if r is not None: return r
        raise InvalidObjectError(f"Attack has no range! ({self.identifier})")

    def getAccuracy(self) -> int:
        if self.accuracy is None:
            a = self.parent.getAccuracy() if self.parent else None
        else:
            a = self.accuracy
        if a is not None: return a
        raise InvalidObjectError(f"Attack has no accuracy! ({self.identifier})")

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    @classmethod
    def fromDict(cls, identifier:Identifier, data:dict):
        atk = cls(identifier, data)
        if cls._link_parents:
            for w, p in cls._link_parents:
                w: AbstractAttack
                p: str
                w._set_parent(cls._loaded.get(p))
        return atk

    def createInstance(self, function_memory:FunctionMemory, **override_values) -> Attack:
        if self.is_template:
            return random.choice(self.get_children()).createInstance(function_memory, **override_values)
        
        else:
            return Attack(self,
                override_values.get("name", self.getName()),
                DynamicValue(override_values.get("damage", self.getDamage())),
                override_values.get("range", self.getRange()),
                DynamicValue(self.getAccuracy()).getCachedOrNew(function_memory),
                self.data,
                self.events
            )

    @classmethod
    def loadData(cls, engine):

        # TODO: load attacks
        files: list[str] = glob.glob("**/attacks/*.json", recursive=True)

        Log["loadup"]["abstract"]["attack"](f"found {len(files)} attack file{'s' if len(files) != 1 else ''}")
        for file in files:

            Log["loadup"]["abstract"]["attack"](f"loading AbstractAttack from '{file}'")
            data = Loader.load(file)

            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        Log["loadup"]["abstract"]["attack"]("linking AbstractAttack parents...")
        for a, p in cls._link_parents:
            a: AbstractAttack
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is a:
                    Log["ERROR"]["loadup"]["abstract"]["attack"]("cannot set object as it's own parent")
                    continue
                elif parent in a.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["attack"]("circular parent loop found")
                    continue
                a._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["attack"](f"parent does not exist: '{p}'")

        Log["loadup"]["abstract"]["attack"]("verifying AbstractAttack completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "attack")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractAttack
            if o.is_template:
                Log.success()
                continue
            try:
                o.getName()
                o.getDamage()
                o.getRange()
                Log.success()
            except InvalidObjectError as err:
                e: AbstractAttack = cls._loaded.pop(l)
                Log.ERROR("loadup", "abstract", "attack", f"failed to load attack: {e.identifier}  {err}")

        Log.end_track()

        cls._link_parents.clear()
        return cls._loaded

    def serialize(self):
        return {
            "name": Serializer.serialize(self.name),
            "range": Serializer.serialize(self.range),
            "damage": Serializer.serialize(self.damage),
            "accuracy": Serializer.serialize(self.accuracy),
            "data": Serializer.serialize(self.data),
            "events": Serializer.serialize(self.events),
            "is_template": Serializer.serialize(self.is_template)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)
