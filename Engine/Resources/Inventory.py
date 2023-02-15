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
    _default_equips = {}

    def __init__(self, contents:list[GameObject]):
        self.parent = None
        self.contents = contents
        self.equips = {}
        self.defaults = {}
        for key, abstract in Inventory._default_equips.items():
            self.defaults.update({key: abstract.createInstance()})
            self.equips.update({key: self.defaults[key]})

    def equip(self, objectType:str, gameObject:GameObject):
        if gameObject not in self.contents: self.contents.append(gameObject)
        self.equips.update({objectType: gameObject})

    def unequipObject(self, gameObject:GameObject):
        for key in self.equips.keys():
            if self.equips[key] is gameObject:
                self.equips[key] = self.defaults.get(key, None)
                return
    
    def unequipType(self, objectType:str):
        if objectType in self.equips:
            self.equips[objectType] = self.defaults.get(objectType, None)

    def fullStats(self):
        equip_stats = []
        for v in self.equips.values():
            if (b := v.bonuses()) is not None: equip_stats.append(b)
        
        out = []
        st = ""
        if equip_stats:
            st = " | ".join(equip_stats)
        
        
        for obj in self.contents:
            out.append(obj.fullStats(obj in self.equips.values()))
        if out: return "\n".join([st, *out])
        return f"{st}\n[no items in inventory]"

    @classmethod
    def from_list(cls, engine:Engine, data:list):
        equips = {}
        contents = []
        Log["loadup"]["inventory"]("loading inventory from list...")
        for element in data:
            element: dict
            Log["loadup"]["inventory"]("Constructing new GameObject")

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
