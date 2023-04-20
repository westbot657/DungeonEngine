# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Weapon import Weapon
    from .AbstractAmmo import AbstractAmmo
    from .EngineErrors import InvalidObjectError
    from .DynamicValue import DynamicValue
    from .EngineDummy import Engine
    from .AbstractGameObject import AbstractGameObject
    from .Logger import Log
except ImportError:
    from Identifier import Identifier
    from Weapon import Weapon
    from AbstractAmmo import AbstractAmmo
    from EngineErrors import InvalidObjectError
    from DynamicValue import DynamicValue
    from EngineDummy import Engine
    from AbstractGameObject import AbstractGameObject
    from Logger import Log

import glob, json, random

""" example_dungeon:weapon/longsword
{
    "parent": "engine:weapon/sword",
    "name": "Longsword",
    "damage": 3,
    "range": 2,
    "max_durability": 100,
    "durability": 100,
    "ammo_type": "engine:ammo/none",
}


# Paramater Break down:
{
    "parent": <identifier of another object>
}


"""

class AbstractWeapon(AbstractGameObject):
    _loaded: dict = {}
    _link_parents = []
    identity: Identifier = Identifier("engine", "abstract/", "weapon")
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

    def _assertAmmoType(self, tp) -> AbstractAmmo:
        if isinstance(tp, AbstractAmmo): return tp
        if abstract := AbstractAmmo._loaded.get(tp, None):
            return abstract
        raise InvalidObjectError(f"AmmoType: '{tp}' does not exist")

    def createInstance(self, function_memory, **value_overrides) -> Weapon:
        if self.is_template:
            # go through children (and sub children probably) and pick a random one?
            # or
            # create instance of first non-template child?
            return random.choice(self.get_children()).createInstance(function_memory, **override_values)
            
        else:
            return Weapon(self,
                value_overrides.get("name", self.getName()),
                DynamicValue(value_overrides.get("damage", self.getDamage())),
                DynamicValue(value_overrides.get("range", self.getRange())),
                value_overrides.get("max_durability", self.getMaxDurability()),
                DynamicValue(value_overrides.get("durability", self.getDurability())).getCachedOrNew(function_memory),
                self._assertAmmoType(value_overrides.get("ammo_type", self.getAmmoType()))
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

        Log["loadup"]["abstract"]["weapon"]("linking AbstractWeapon parents...")
        for a, p in cls._link_parents:
            a: AbstractWeapon
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is a:
                    Log["ERROR"]["loadup"]["abstract"]["weapon"]("cannot set object as it's own parent")
                    continue
                elif parent in a.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["weapon"]("circular parent loop found")
                    continue
                a._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["weapon"](f"parent does not exist: '{p}'")

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
                continue
            

        return cls._loaded

if __name__ == "__main__":
    print(AbstractWeapon.loadData(None))
