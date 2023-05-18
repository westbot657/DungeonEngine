# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .EngineErrors import InvalidObjectError
    from .EngineDummy import Engine
    from .AbstractAttack import AbstractAttack, Attack
    from .DynamicValue import DynamicValue
    from .Enemy import Enemy
    from .Logger import Log
    from .Position import Position
    from .Location import Location
except ImportError:
    from Identifier import Identifier
    from EngineErrors import InvalidObjectError
    from EngineDummy import Engine
    from AbstractAttack import AbstractAttack, Attack
    from DynamicValue import DynamicValue
    from Enemy import Enemy
    from Logger import Log
    from Position import Position
    from Location import Location

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
    
        self.is_template: bool = data.get("template", False)
    
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
        return out

    def _assertListAttackType(self, attacks) -> list[AbstractAttack]:
        out = []
        for atk in attacks:
            if isinstance(atk, AbstractAttack):
                out.append(atk)
            elif isinstance(atk, str):
                if abstract := AbstractAttack._loaded.get(atk, None):
                    out.append(abstract)
                else:
                    raise InvalidObjectError(f"attack '{atk}' does not exist! ({self.identifier})")
            else:
                raise InvalidObjectError(f"invalid attack object: {atk} ({self.identifier})")

        return out

    def createInstance(self, function_memory, location:Location, position:Position, **override_values) -> Enemy:
        return Enemy(self,
            override_values.get("name", self.getName()),
            override_values.get("max_health", self.getMaxHealth()),
            DynamicValue(override_values.get("health", self.getHealth())).getCachedOrNew(function_memory),
            self._assertListAttackType(override_values.get("attacks", self.getAttacks())),
            location,
            position
        )
    
    @classmethod
    def getFromIdentifier(cls, identifier:Identifier|str):
        identifier = Identifier.fromString(identifier)

        if (abstract := cls._loaded.get(identifier, None)) is not None:
            return abstract
    
        raise InvalidObjectError(f"No Abstract Enemy exists with id: '{identifier}'")

    @classmethod
    def loadData(cls, engine:Engine) -> list:
        files: list[str] = glob.glob("**/enemies/*.json", recursive=True)
        #print(files)
        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        for w, p in cls._link_parents:
            w: AbstractEnemy
            p: str
            w._set_parent(cls._loaded.get(p))

        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractEnemy
            try:
                o.getName()
                o.getMaxHealth()
                o.getHealth()
                o.getAttacks()
            except InvalidObjectError as err:
                e: AbstractEnemy = cls._loaded.pop(l)
                print(f"Failed to load enemy: {e.identifier}  {err}")

        cls._link_parents.clear()

        return cls._loaded






