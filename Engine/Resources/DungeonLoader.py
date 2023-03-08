# pylint: disable=[W,R,C,import-error]

try:
    from .AbstractAmmo import AbstractAmmo, Ammo
    from .AbstractArmor import AbstractArmor, Armor
    from .AbstractAttack import AbstractAttack, Attack
    from .AbstractCombat import AbstractCombat, Combat
    from .AbstractDungeon import AbstractDungeon, Dungeon
    from .AbstractEnemy import AbstractEnemy, Enemy
    from .AbstractItem import AbstractItem, Item
    from .AbstractRoom import AbstractRoom, Room
    from .AbstractStatusEffect import AbstractStatusEffect, StatusEffect
    from .AbstractTool import AbstractTool, Tool
    from .AbstractWeapon import AbstractWeapon, Weapon
    from .Functions import LoaderFunction
    from .Identifier import Identifier
    from .EngineDummy import Engine
    from .EngineErrors import InvalidObjectError, FunctionLoadError
    from .LootTable import LootTable
    from .TextPattern import TextPattern
    from .Player import Player
    from .AbstractGameObject import AbstractGameObject, GameObject
    from .Logger import Log
except ImportError:
    from AbstractAmmo import AbstractAmmo, Ammo
    from AbstractArmor import AbstractArmor, Armor
    from AbstractAttack import AbstractAttack, Attack
    from AbstractEnemy import AbstractEnemy, Enemy
    from AbstractCombat import AbstractCombat, Combat
    from AbstractDungeon import AbstractDungeon, Dungeon
    from AbstractItem import AbstractItem, Item
    from AbstractRoom import AbstractRoom, Room
    from AbstractStatusEffect import AbstractStatusEffect, StatusEffect
    from AbstractTool import AbstractTool, Tool
    from AbstractWeapon import AbstractWeapon, Weapon
    from Functions import LoaderFunction
    from Identifier import Identifier
    from EngineDummy import Engine
    from EngineErrors import InvalidObjectError, FunctionLoadError
    from LootTable import LootTable
    from TextPattern import TextPattern
    from Player import Player
    from AbstractGameObject import AbstractGameObject, GameObject
    from Logger import Log

from typing import Any
import re

class DungeonLoader:
    _loader = None
    def __new__(cls):
        if not cls._loader:
            cls._loader = self = super().__new__(cls)
            self.init()
        return cls._loader

    def init(self):
        self.loader_function = LoaderFunction
        self.abstract_ammo: dict[str, AbstractAmmo] = {}
        self.abstract_armor: dict[str, AbstractArmor] = {}
        self.abstract_attacks: dict[str, AbstractAttack] = {}
        self.abstract_combats: dict[str, AbstractCombat] = {}
        self.abstract_dungeons: dict[str, AbstractDungeon] = {}
        self.abstract_enemies: dict[str, AbstractEnemy] = {}
        self.abstract_items: dict[str, AbstractItem] = {}
        #self.abstract_loot_tables: dict[str, AbstractLootTable] = {}
        self.abstract_rooms: dict[str, AbstractRoom] = {}
        self.abstract_status_effects: dict[str, AbstractStatusEffect] = {}
        self.abstract_tools: dict[str, AbstractTool] = {}
        self.abstract_weapons: dict[str, AbstractWeapon] = {}

    def evaluateFunction(self, engine:Engine, data:dict):
        # TODO: function memory stuff can happen here I guess? (not sure what that is right now though)
        engine.function_memory.clear()
        val = self._evaluateFunction(engine, data)
        return val

    def _evaluateFunction(self, engine:Engine, data:dict):
        if (funcs := data.get("functions", None)) is not None:
            if (predicate := data.get("predicate", None)) is not None:
                if not engine.function_memory.checkPredicate(engine, predicate): return None
            result = None
            for func in funcs:
                res = self._evaluateFunction(engine, func)
                if res: result = res
            return result
        elif (func := data.get("function", None)) is not None:
            if f := self.loader_function.getFunction(func):
                f: LoaderFunction
                # Check predicate
                if (predicate := data.get("predicate", None)) is not None:
                    if not engine.function_memory.checkPredicate(engine, predicate): return None
                # Run function
                args = {}
                for key, item in data.items(): # gather the arguments for the function
                    if key in ["function", "#store", "predicate"]: continue # skip the function's id, predicate, and the special #store operator
                    if isinstance(item, dict):
                        args.update({key: self._evaluateFunction(engine, item)})
                    else:
                        args.update({key: item})
                r = f._call(engine, args)
                # if a #store operator was present with the function, the function's result is assigned to the name in #store
                if var := data.get("#store", None):
                    engine.function_memory.store(var, r)
                return r
        elif (var := data.get("#ref", None)) is not None:
            return engine.function_memory.ref(var)
        elif (store := data.get("#store", None)) is not None:
            if isinstance(store, dict):
                for key, value in store.items():
                    engine.function_memory.store(key, value)
        elif isinstance(data, dict):
            dat = {}
            for key, item in data.items():
                dat.update({key, self._evaluateFunction(engine, item)})
            return dat
        elif isinstance(data, list):
            dat = []
            for item in data:
                dat.append(self._evaluateFunction(engine, data))
            return dat
        else:
            return data

    def searchFor(self, identifier:Identifier) -> AbstractGameObject|type[AbstractGameObject]|LoaderFunction|None:
        if identifier.path:
            if func := self.loader_function._functions.get(identifier.full(), None):
                return func
            if abstractGameObjectType := AbstractGameObject._game_object_types.get(identifier.fullWith(path="abstract/", name=identifier.path.strip('/')), None):
                abstractGameObjectType: AbstractGameObject
                if abstractGameObject := abstractGameObjectType._loaded.get(identifier.full(), None):
                    return abstractGameObject
        else:
            if a := AbstractGameObject._game_object_types.get(identifier.fullWith(path="abstract/"), None):
                return a
            elif func := self.loader_function._functions.get(identifier.full(), None):
                return func
        return None


    def constructAmmo(self, data:dict) -> Ammo:
        ...
    def constructArmor(self, data:dict) -> Armor:
        ...
    def constructAttack(self, data:dict) -> Attack:
        ...
    def constructCombat(self, data:dict) -> Combat:
        ...
    # def constructDungeon(self, data:dict) -> Dungeon: # This shouldn't be needed, there should be no in-line dungeons inside a dungeon
    #     ...
    def constructEnemy(self, data:dict) -> Enemy:
        ...
    def constructItem(self, data:dict) -> Item:
        ...
    def constructLootTable(self, data:dict) -> LootTable:
        ...
    # def constructRoom(self, data:dict) -> Room: # also shouldn't be any in-line rooms
    #     ...
    def constructStatusEffect(self, data:dict) -> StatusEffect:
        ...
    def constructTool(self, data:dict) -> Tool:
        ...
    def constructWeapon(self, data:dict) -> Weapon:
        ...
    
    def constructGameObject(self, engine, data:dict) -> GameObject:
        Log["loadup"]["loader"]("Constructing new GameObject...")
        if obj_type := data.get("type", None):
            identifier = Identifier.fromString(obj_type)
            identifier.path = "abstract/"
            nm = identifier.full()
            if tp := AbstractGameObject._game_object_types.get(nm, None):
                if parent := data.get("parent", None):
                    if abstract := tp._loaded.get(parent, None):
                        Log["loadup"]["loader"]("GameObject Construction complete")
                        return abstract.createInstance(engine, **data)
                    raise InvalidObjectError(f"No parent GameObject with id: '{parent}'")
            raise InvalidObjectError(f"GameObject type: '{nm}' does not exist")
        elif parent := data.get("parent", None):
            ...
            # determine parent type
        else:
            raise InvalidObjectError("No type or parent given for GameObject")


    @TextPattern(r"\b(?:equip) *(?P<item_name>.*)\b")
    @staticmethod
    def checkTextEquip(engine:Engine, player:Player, raw_text:str, groupdict:dict):
        item_name: str = groupdict["item_name"].strip()

        for weapon in player.inventory.getOfType(Weapon):
            weapon: Weapon
            if weapon.name.lower() == item_name.lower():
                player.inventory.equip("engine:weapon", weapon)
                break
        else:
            for armor in player.inventory.getOfType(Armor):
                armor: Armor
                if armor.name.lower() == item_name.lower():
                    player.inventory.equip("engine:armor", armor)
                    break
            else:
                for tool in player.inventory.getOfType(Tool):
                    tool: Tool
                    if tool.name.lower() == item_name.lower():
                        player.inventory.equip("engine:tool", tool)
                        break
                else:
                    engine.sendOutput(player, f"You have no Weapon, Armor, or Tool called '{item_name}'")

    @TextPattern(r"\b(?P<keyword>use|eat|throw|apply|drink)(?: *(?P<amount>[1-9][0-9]*|an?|the|(?:some|all) *(?:(?:of *)?(?:the|my)))?)? *(?P<item_name>.*)\b")
    @staticmethod
    def checkTextUse(engine:Engine, player:Player, raw_text:str, groupdict:dict):
        keyword: str = groupdict["keyword"]
        amount: str = groupdict["amount"]
        item_name: str = groupdict["item_name"]

    @TextPattern(r"\b(inventory|bag|items)\b", TextPattern.CheckType.SEARCH)
    @staticmethod
    def checkTextInventory(engine:Engine, player:Player, raw_text:str, groupdict:dict):
        engine.sendOutput(player, player.inventory.fullStats(engine))

    def getAmmo(self, identifier:Identifier|str) -> AbstractAmmo:
        identifier: Identifier = Identifier.fromString(identifier)
        
    def getArmor(self, identifier:Identifier|str) -> AbstractArmor:
        identifier: Identifier = Identifier.fromString(identifier)
    
    def getItem(self, identifier:Identifier|str) -> AbstractItem:
        identifier: Identifier = Identifier.fromString(identifier)
    
    def getStatusEffect(self, identifier:Identifier|str) -> AbstractStatusEffect:
        identifier: Identifier = Identifier.fromString(identifier)

    def getTool(self, identifier:Identifier|str) -> AbstractTool:
        identifier: Identifier = Identifier.fromString(identifier)
    
    def getWeapon(self, identifier:Identifier|str) -> AbstractWeapon:
        identifier: Identifier = Identifier.fromString(identifier)

    def getGameObject(self, identifier:Identifier|str) -> AbstractGameObject:
        identifier: Identifier = Identifier.fromString(identifier)

        # TODO: actually search for object (however that needs to be done)

    def loadGame(self, engine:Engine):
        Log["loadup"]["loader"]("Loading Abstract Status Effects...")
        self.abstract_status_effects = AbstractStatusEffect.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Ammo...")
        self.abstract_ammo = AbstractAmmo.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Armors...")
        self.abstract_armor = AbstractArmor.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Tools...")
        self.abstract_tools = AbstractTool.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Weapons...")
        self.abstract_weapons = AbstractWeapon.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Items...")
        self.abstract_items = AbstractItem.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Attacks...")
        self.abstract_attacks = AbstractAttack.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Enemies...")
        self.abstract_enemies = AbstractEnemy.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Combats...")
        self.abstract_combats = AbstractCombat.loadData(self)
        #self.abstract_loot_tables = AbstractLootTable.loadData(self)
        
        # self.abstract_rooms = AbstractRoom.loadData(self)

        Log["loadup"]["loader"]("Loading Abstract Dungeons...")
        self.abstract_dungeons = AbstractDungeon.loadData(self)

        Log["loadup"]["loader"]("Engine resource loading completed")

    def saveGame(self, engine:Engine):
        # TODO: implement saving
        pass
