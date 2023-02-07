# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractAmmo import AbstractAmmo, Ammo
    from .AbstractArmor import AbstractArmor, Armor
    from .Identifier import Identifier
    from .AbstractItem import AbstractItem, Item
    from .AbstractStatusEffect import AbstractStatusEffect, StatusEffect
    from .AbstractTool import AbstractTool, Tool
    from .AbstractWeapon import AbstractWeapon, Weapon
    from .AbstractGameObject import AbstractGameObject, GameObject
    from .EngineDummy import Engine
    from .EngineErrors import InvalidObjectError
    from .Logger import Log
except ImportError:
    from AbstractAmmo import AbstractAmmo, Ammo
    from AbstractArmor import AbstractArmor, Armor
    from Identifier import Identifier
    from AbstractItem import AbstractItem, Item
    from AbstractStatusEffect import AbstractStatusEffect, StatusEffect
    from AbstractTool import AbstractTool, Tool
    from AbstractWeapon import AbstractWeapon, Weapon
    from AbstractGameObject import AbstractGameObject, GameObject
    from EngineDummy import Engine
    from EngineErrors import InvalidObjectError
    from Logger import Log

class Inventory:
    def __init__(self, contents:list[GameObject]):
        self.parent = None
        self.contents = contents
        self.equips = {}

    def fullStats(self):
        out = []
        for obj in self.contents:
            out.append(obj.fullStats(obj in self.equips.values()))
        if out: return "\n".join(out)
        return "[no items in inventory]"

    @classmethod
    def from_list(cls, engine:Engine, data:list):
        equips = {}
        contents = []
        Log["loadup"]["inventory"]("loading inventory from list...")
        for element in data:
            element: dict
            Log["loadup"]["inventory"]("constructing new GameObject")
            try:
                obj: GameObject = engine.loader.constructGameObject(element)
            except InvalidObjectError as e:
                Log["ERROR"]["loadup"]["inventory"](*e.args, sep=" ")
                continue
            contents.append(obj)
            Log["loadup"]["inventory"]("gameObject added to inventory")
            if element.get("equipped", False):
                equips.update({obj.identifier.ID(): obj})
        inv = cls(contents)
        inv.equips = equips
        Log["loadup"]["inventory"]("Inventory Construction finished")
        return inv
