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
    from .FunctionMemory import FunctionMemory
    from .FunctionalElement import FunctionalElement
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
    from FunctionMemory import FunctionMemory
    from FunctionalElement import FunctionalElement

class Inventory(FunctionalElement):
    _default_equips = {}

    def __init__(self, function_memory, contents:list[GameObject]):
        self.parent = None
        self.contents = contents
        self.equips = {}
        self.defaults = {}
        for key, abstract in Inventory._default_equips.items():
            self.defaults.update({key: abstract.createInstance(function_memory)})
            self.equips.update({key: self.defaults[key]})

    def equip(self, objectType:str, gameObject:GameObject):
        if gameObject not in self.contents: self.contents.append(gameObject)
        self.equips.update({objectType: gameObject})

    def unequipObject(self, gameObject:GameObject):
        for key in self.equips.keys():
            if self.equips[key] is gameObject:
                self.equips[key] = self.defaults.get(key, None)
                
    def removeObject(self, game_object:GameObject):
        if game_object in self.contents:
            if self.isEquipped(game_object):
                self.unequipObject(game_object)
            self.contents.remove(game_object)
            game_object.owner = None

    def addObject(self, game_object:GameObject):

        if hasattr(game_object, "count"):
            for obj in self.contents:
                if obj.abstract == game_object.abstract:
                    if obj.count < obj.max_count == game_object.max_count:
                        diff = obj.max_count - obj.count
                        if diff < game_object.count:
                            game_object.count -= diff
                            obj.count = obj.max_count
                            break
                        else:
                            obj.count += game_object.count
                            return

        game_object.owner = self.parent
        self.contents.append(game_object)
    
    def setParent(self, parent):
        self.parent = parent
        for game_object in self.contents:
            game_object.owner = parent

    def getOfType(self, objectType:type|tuple[type]):
        matches = []
        for c in self.contents:
            if isinstance(c, objectType):
                matches.append(c)
        return matches

    def isEquipped(self, gameObject:GameObject):
        return gameObject in self.equips.values()

    def getEquipped(self, objectType:type):
        for e in self.equips.values():
            if isinstance(e, objectType):
                return e
        return None

    def unequipType(self, objectType:str):
        if objectType in self.equips:
            self.equips[objectType] = self.defaults.get(objectType, None)

    def fullStats(self, function_memory:FunctionMemory):
        equip_stats = []
        for v in self.equips.values():
            v: GameObject|None
            if v is None: continue
            if (b := v.bonuses(function_memory)) is not None: equip_stats.append(b)
        
        out = []
        st = ""
        if equip_stats:
            st = " | ".join(equip_stats)
        
        
        for obj in self.contents:
            out.append(obj.fullStats(function_memory, obj in self.equips.values()))
        if out: return "\n".join([st, *out])
        return f"{st}\n[no items in inventory]"

    @classmethod
    def from_list(cls, engine, data:list):
        equips = {}
        contents = []
        Log["loadup"]["inventory"]("loading inventory from list...")
        for element in data:
            element: dict
            Log["loadup"]["inventory"]("Constructing new GameObject")

            try:
                obj: GameObject = engine.loader.constructGameObject(engine._function_memory, element)
            except InvalidObjectError as e:
                Log["ERROR"]["loadup"]["inventory"](*e.args, sep=" ")
                continue
            
            contents.append(obj)
            Log["loadup"]["inventory"]("gameObject added to inventory")
            if element.get("equipped", False):
                equips.update({obj.identifier.ID(): obj})
        inv = cls(engine._function_memory, contents)
        inv.equips = equips
        Log["loadup"]["inventory"]("Inventory Construction finished")
        return inv

    def _get_save(self, function_memory:FunctionMemory):
        d = []

        for obj in self.contents:
            obj: Weapon|Ammo|Tool|Item|Armor
            dat: dict = obj._get_save(function_memory)
            if self.isEquipped(obj):
                dat.update({"equipped": True})
            
            d.append(dat)

        return d
