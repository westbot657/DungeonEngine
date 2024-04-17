# pylint: disable=[W,R,C,import-error]

from Identifier import Identifier
from EngineErrors import InvalidObjectError
from EngineDummy import Engine
from AbstractAttack import AbstractAttack, Attack
from DynamicValue import DynamicValue
from Enemy import Enemy
from Logger import Log
from Position import Position
from Location import Location
from FunctionMemory import FunctionMemory
from Util import Util
from Loader import Loader
from Serializer import Serializer, Serializable

import glob, json, re


"""
Example Enemy:
{
    "name": "Goblin",
    "max_health": 10,
    "attacks": [
        "engine:attacks/stab",
        "engine:attacks/bite"
    ]
}

"""

@Serializable("AbstractEnemy")
class AbstractEnemy:
    _loaded: dict = {}
    _link_parents: list = []
    identity: Identifier = Identifier("engine", "abstract/", "enemy")
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractEnemy] = []
        self.parent: AbstractEnemy|None = None
    
        if "parent" in data:
            AbstractEnemy._link_parents.append((self, data["parent"]))
        
        self.name: str|None = data.get("name", None)
        self.max_health: int|None = data.get("max_health", None)
        self.health: int|None = data.get("health", self.max_health)
        self.attacks: list = data.get("attacks", [])
        self._id = data.get("id", None)
    
        self.is_template: bool = data.get("template", False)

        self.events = data.get("events", {})
    
    def __repr__(self):
        return f"AbstractEnemy: {self.identifier.full()}"

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)
    
    def getName(self):
        if self.name is None:
            if self.parent:
                return self.parent.getName()
        else:
            return self.name
        raise InvalidObjectError(f"Enemy has no name! ({self.identifier})")

    def getMaxHealth(self):
        if self.max_health is None:
            if self.parent:
                return self.parent.getMaxHealth()
        else:
            return self.max_health
        raise InvalidObjectError(f"Enemy has no max_health! ({self.identifier})")

    def getHealth(self):
        if self.health is None:
            if self.parent:
                return self.parent.getHealth()
        else:
            return self.health
        raise InvalidObjectError(f"Enemy has no health! ({self.identifier})")

    def getAttacks(self) -> list[AbstractAttack]:

        out = []
        for atk in self.attacks:
            if isinstance(atk, dict):
                out.append(
                    AbstractAttack.fromDict(
                        Identifier(
                            self.identifier.namespace + "_inline",
                            path="attack/",
                            name=re.sub(
                                r"[ \-!?+()|<>.,:;'\"*&^%$#@~`\[\]\\/=]+",
                                "_",
                                atk.get("name", None) or atk.get("parent", "broken_gameobject")
                            ).lower()
                        ),
                        atk
                    )
                )
            elif abstract := AbstractAttack._loaded.get(atk, None):
                out.append(abstract)
            else:
                Log["ERROR"]["loadup"]["abstract"]["enemy"](f"Failed to load attack; does not exist: '{atk}'")
                continue
        
        if (not out) and self.parent:
            out = self.parent.getAttacks()

        return out

    def _assertListAttackType(self, function_memory:FunctionMemory, attacks) -> list[Attack]:
        out = []
        for atk in attacks:
            if isinstance(atk, AbstractAttack):
                out.append(atk.createInstance(function_memory))
            elif isinstance(atk, str):
                if abstract := AbstractAttack._loaded.get(atk, None):
                    abstract: AbstractAttack
                    out.append(abstract.createInstance(function_memory))
                else:
                    raise InvalidObjectError(f"attack '{atk}' does not exist! ({self.identifier})")
            else:
                raise InvalidObjectError(f"invalid attack object: {atk} ({self.identifier})")

        return out

    def get_parent_chain(self):
        if self.parent is None:
            return []
        else:
            return [self.parent] + self.parent.get_parent_chain()

    def createInstance(self, function_memory:FunctionMemory, location:Location, position:Position, **override_values) -> Enemy:
        enemy = Enemy(self,
            override_values.get("name", self.getName()),
            override_values.get("max_health", self.getMaxHealth()),
            DynamicValue(override_values.get("health", self.getHealth())).getCachedOrNew(function_memory),
            self._assertListAttackType(function_memory, override_values.get("attacks", self.getAttacks())),
            location,
            position,
            override_values.get("uid", None)
        )

        enemy.setEvents(Util.deepCopy(self.events))

        return enemy
    
    @classmethod
    def getFromIdentifier(cls, identifier:Identifier|str):
        identifier = Identifier.fromString(identifier)

        if (abstract := cls._loaded.get(identifier, None)) is not None:
            return abstract
    
        raise InvalidObjectError(f"No Abstract Enemy exists with id: '{identifier}'")

    @classmethod
    def loadFromDict(cls, data:dict):
        ...

    def linkParent(self):

        if not AbstractEnemy._link_parents:
            return

        _, parent = AbstractEnemy._link_parents.pop()
        self._set_parent(AbstractEnemy._loaded.get(parent))

        try:
            self.getName()
            self.getMaxHealth()
            self.getHealth()
            self.getAttacks()
        except InvalidObjectError as err:
            Log["loadup"]["abstract"]["enemy"](f"Failed to load enemy: {self.identifier}  {err}")
        
        AbstractEnemy._link_parents.clear()

    @classmethod
    def loadData(cls, engine:Engine) -> list:
        files: list[str] = glob.glob("**/enemies/*.json", recursive=True)
        
        Log["loadup"]["abstract"]["enemy"](f"found {len(files)} enemy file{'s' if len(files) != 1 else ''}")
        for file in files:
            file: str
            Log["loadup"]["abstract"]["enemy"](f"loading AbstractEnemy from '{file}'")
            data = Loader.load(file)

            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        Log["loadup"]["abstract"]["enemy"]("linking AbstractEnemy parents...")
        for w, p in cls._link_parents:
            w: AbstractEnemy
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is w:
                    Log["ERROR"]["loadup"]["abstract"]["enemy"]("cannot set object as it's own parent")
                    continue
                elif parent in w.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["enemy"]("circular parent loop found")
                    continue
                w._set_parent(cls._loaded.get(p))
            else:
                Log["ERROR"]["loadup"]["abstract"]["enemy"](f"parent does not exist: '{p}'")

        Log["loadup"]["abstract"]["enemy"]("verifying AbstractEnemy completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "enemy")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractEnemy
            try:
                o.getName()
                o.getMaxHealth()
                o.getHealth()
                o.getAttacks()
                Log.success()
            except InvalidObjectError as err:
                e: AbstractEnemy = cls._loaded.pop(l)
                Log.ERROR("loadup", "abstract", "enemy", f"failed to load enemy: {e.identifier}. {err}")

        Log.end_track()

        cls._link_parents.clear()

        Log["loadup"]["abstract"]["enemy"]("AbstractEnemy loading complete")
        return cls._loaded

    def serialize(self):
        return {
            "identifier": Serializer.serialize(self.identifier),
            "_raw_data": Serializer.serialize(self._raw_data),
            "children": Serializer.serialize(self.children),
            "parent": Serializer.serialize(self.parent),
            "name": Serializer.serialize(self.name),
            "max_health": Serializer.serialize(self.max_health),
            "health": Serializer.serialize(self.health),
            "attacks": Serializer.serialize(self.attacks),
            "_id": Serializer.serialize(self._id),
            "is_template": Serializer.serialize(self.is_template),
            "events": Serializer.serialize(self.events)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)




