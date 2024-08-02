# pylint: disable=[W,R,C,import-error]

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
from .Serializer import Serializer, Serializable

@Serializable("Inventory")
class Inventory(FunctionalElement):
    _default_equips: dict[str, AbstractGameObject] = {}

    def __init__(self, function_memory, contents:list[GameObject]):
        self.parent = None
        self.contents: list[GameObject] = contents
        self.equips: dict[str, GameObject|None] = {}
        self.defaults: dict[str, GameObject] = {}
        self.function_memory = function_memory
        self.slots: int = 50
        for key, abstract in Inventory._default_equips.items():
            self.defaults.update({key: abstract.createInstance(function_memory)})
            self.equips.update({key: self.defaults[key]})

    def serialize(self):
        return {
            "parent": Serializer.serialize(self.parent),
            "contents": Serializer.serialize(self.contents),
            "equips": Serializer.serialize(self.equips),
            "defaults": Serializer.serialize(self.defaults),
            "function_memory": Serializer.serialize(self.function_memory),
            "slots": Serializer.serialize(self.slots)
        }

    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    # def get_ui_data(self):
    #     return self

    def consolidate(self):
        
        c = self.contents.copy()
        c.reverse()
        
        while c:
            i = c.pop(0)
            
            new = []
            
            for i2 in c:
                if isinstance(i2, (Item, Ammo)):
                    if i2.stack(i):
                        self.unequipObject(i)
                        break
            else:
                new.append(i)
        
        new.reverse()
        
        self.contents.clear()
        self.contents += new

    def equip(self, objectType:str, gameObject:GameObject):
        if gameObject not in self.contents: self.contents.append(gameObject)
        self.equips.update({objectType: gameObject})
        self.function_memory.engine.sendOutput(9, "update-inventory-ui")

    def unequipObject(self, gameObject:GameObject):
        for key in self.equips.keys():
            if self.equips[key] is gameObject:
                self.equips[key] = self.defaults.get(key, None)
                self.function_memory.engine.sendOutput(9, "update-inventory-ui")
                
    def removeObject(self, game_object:GameObject):
        if game_object in self.contents:
            if self.isEquipped(game_object):
                self.unequipObject(game_object)
            self.contents.remove(game_object)
            game_object.owner = None
            self.function_memory.engine.sendOutput(9, "update-inventory-ui")

    def addObject(self, game_object:GameObject):

        if hasattr(game_object, "count"):
            for obj in self.contents:
                obj: Ammo|Item
                if obj.abstract == game_object.abstract:
                    if obj.count < obj.max_count == game_object.max_count:
                        diff = obj.max_count - obj.count
                        if diff < game_object.count:
                            game_object.count -= diff
                            obj.count = obj.max_count
                            # self.function_memory.engine.sendOutput(9, "update-inventory-ui")
                            break
                        else:
                            obj.count += game_object.count
                            self.function_memory.engine.sendOutput(9, "update-inventory-ui")
                            return

        game_object.owner = self.parent
        self.contents.append(game_object)
        self.function_memory.engine.sendOutput(9, "update-inventory-ui")
    
    def setParent(self, parent):
        self.parent = parent
        for game_object in self.contents:
            game_object.owner = parent

    def getOfType(self, objectType:type|tuple[type], priority="first"):
        matches = []
        c2 = self.contents.copy()
        if priority == "last":
            c2.reverse()
            
        for c in c2:
            if isinstance(c, objectType):
                matches.append(c)
        return matches

    def getPreferedEquip(self, abstract_type:AbstractGameObject, priority="first"):
        for c in self.equips.values():
            if c.abstract.inherets_from(abstract_type):
                return c
        return self.getOfAbstractType(abstract_type, priority)

    def containsGameObject(self, game_object:Identifier):
        for c in self.contents:
            if c.identifier == game_object:
                return True
        return False
    
    def getOfAbstractType(self, abstract_type:AbstractGameObject, priority="first"):
        c2 = self.contents.copy()
        if priority == "last":
            c2.reverse()
            
        for c in c2:
            if c.abstract.inherets_from(abstract_type):
                return c
        return None

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
            self.function_memory.engine.sendOutput(9, "update-inventory-ui")

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
        
        function_memory.engine.sendOutput(9, "update-inventory-ui")
        
        for obj in self.contents:
            out.append(obj.fullStats(function_memory, obj in self.equips.values()))
        if out: return "\n".join([st, *out])
        return f"{st}\n[no items in inventory]"

    def quickStats(self, function_memory:FunctionMemory):
        equip_stats = []
        for v in self.equips.values():
            v: GameObject|None
            if v is None: continue
            if (b := v.bonuses(function_memory)) is not None: equip_stats.append(b)
        
        out = []
        st = ""
        if equip_stats:
            st = " | ".join(equip_stats)
        
        function_memory.engine.sendOutput(9, "update-inventory-ui")
        
        for obj in self.contents:
            out.append(obj.quickStats(function_memory))
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
