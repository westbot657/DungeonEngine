# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .AbstractGameObject import AbstractGameObject
    from .Attack import Attack
    from .EngineErrors import InvalidObjectError
    from .DynamicValue import DynamicValue
    from .Logger import Log
except ImportError:
    from Identifier import Identifier
    from AbstractGameObject import AbstractGameObject
    from Attack import Attack
    from EngineErrors import InvalidObjectError
    from DynamicValue import DynamicValue
    from Logger import Log

import glob, json

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

        self.is_template = data.get("is_template", False)

    def getName(self):
        n = self.name or (self.parent.getName() if self.parent else None)
        if n is not None: return n
        raise InvalidObjectError(f"Attack has no name! ({self.identifier})")
    
    def getDamage(self) -> int:
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

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    @classmethod
    def fromDict(cls, identifier:Identifier, data:dict):
        atk = cls(identifier, data)
        # TODO: link parent if needed (and whatever else needs to be done)
        return atk

    def createInstance(self, **override_values) -> Attack:
        if self.is_template:
            ...
        else:
            return Attack(self,
                DynamicValue(override_values.get("name", self.getName())),
                DynamicValue(override_values.get("damage", self.getDamage())),
                DynamicValue(override_values.get("range", self.getRange()))
            )

    @classmethod
    def loadData(cls, engine):

        # TODO: load attacks
        files: list[str] = glob.glob("**/attacks/*.json", recursive=True)

        for file in files:
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)

            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        for w, p in cls._link_parents:
            w: AbstractAttack
            p: str
            w._set_parent(cls._loaded.get(p))

        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractAttack
            try:
                ...
            except InvalidObjectError as err:
                e: AbstractAttack = cls._loaded.pop(l)
                print(f"Failed to load attack: {e.identifier}  {err}")

        return cls._loaded

