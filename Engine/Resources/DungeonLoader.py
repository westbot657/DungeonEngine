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
    from .Util import Util
    from .Logger import Log
    from .FunctionMemory import FunctionMemory
    from .EngineOperation import EngineOperation, _EngineOperation
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
    from Util import Util
    from Logger import Log
    from FunctionMemory import FunctionMemory
    from EngineOperation import EngineOperation, _EngineOperation

from typing import Any, Generator
import re

class DungeonLoader:

    # TODO:
    # convert to generators:
    # checkTextUse()

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

    def evaluateFunction(self, function_memory:FunctionMemory, data:dict):
        # TODO: function memory stuff can happen here I guess? (not sure what that is right now though)
        #function_memory.clear()
        val = self._evaluateFunction(function_memory, data)
        return val

    def generatorEvaluateFunction(self, function_memory:FunctionMemory, data:dict):
        ev = self._generatorEvaluateFunction(function_memory, data)
        try:
            v = ev.send(None)
            while isinstance(v, (EngineOperation, _EngineOperation)):
                res = yield v
                v = ev.send(res)
        except StopIteration as e:
            res = e.value or v

    def _generatorEvaluateFunction(self, function_memory:FunctionMemory, data:dict):
        
        if isinstance(data, dict):
            if (funcs := data.get("functions", None)) is not None:
                if (predicate := data.get("predicate", None)) is not None:
                    if not function_memory.checkPredicate(predicate): return None
                result = None
                for func in funcs:
                    ev = self._generatorEvaluateFunction(function_memory, func)
                    try:
                        v = ev.send(None)
                        while isinstance(v, (EngineOperation, _EngineOperation)):
                            res = yield v
                            v = ev.send(res)
                    except StopIteration as e:
                        res = e.value or v
                        if res: result = res
                return result
            elif (func := data.get("function", None)) is not None:
                if f := self.loader_function.getFunction(func):
                    f: LoaderFunction
                    if (predicate := data.get("function", None)) is not None:
                        if not function_memory.checkPredicate(predicate): return None
                    args = {}
                    for key, item in data.items():
                        if key in ["function", "#store", "predicate"]: continue
                        if isinstance(item, dict):
                            ev = self._generatorEvaluateFunction(function_memory, item)
                            try:
                                v = ev.send(None)
                                while isinstance(v, (EngineOperation, _EngineOperation)):
                                    res = yield v
                                    v = ev.send(res)
                            except StopIteration as e:
                                res = e.value or v
                                args.update({key: res})
                        else:
                            args.update({key: item})
                    r = f._call(function_memory, args)

                    if isinstance(r, Generator):
                        try:
                            v = r.send(None)
                            while isinstance(v, (EngineOperation, _EngineOperation)):
                                res = yield v
                                v = ev.send(res)
                        except StopIteration as e:
                            res = e.value or v
                    else:
                        res = r
                    
                    if var := data.get("#store", None):
                        var: str
                        if var.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{var}'")
                        function_memory.store(var, res)
                    return res
        
            elif (var := data.get("#ref", None)) is not None:
                return function_memory.ref(var)
            elif (store := data.get("#store", None)) is not None:
                if isinstance(store, dict):
                    for key, value in store.items():
                        if key.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{key}'")
                        function_memory.store(key, value)

            elif (check := data.get("@check", None)) is not None:
                ev = self._generatorEvaluateFunction(function_memory, check)
                try:
                    v = ev.send(None)
                    while isinstance(v, (EngineOperation, _EngineOperation)):
                        res = yield v
                        v = ev.send(res)
                except StopIteration as e:
                    res = e.value or v
                if res and ((true_branch := data.get("true", None)) is not None):

                    ev = self._generatorEvaluateFunction(function_memory, true_branch)
                    try:
                        v = ev.send(None)
                        while isinstance(v, (EngineOperation, _EngineOperation)):
                            res = yield v
                            v = ev.send(res)
                    except StopIteration as e:
                        return e.value or v

                elif (false_branch := data.get("false", None)) is not None:

                    ev = self._generatorEvaluateFunction(function_memory, false_branch)
                    try:
                        v = ev.send(None)
                        while isinstance(v, (EngineOperation, _EngineOperation)):
                            res = yield v
                            v = ev.send(res)
                    except StopIteration as e:
                        return e.value or v
                else:
                    return None
            else:
                dat = {}
                for key, item in data.items():

                    ev = self._generatorEvaluateFunction(function_memory, item)
                    try:
                        v = ev.send(None)
                        while isinstance(v, (EngineOperation, _EngineOperation)):
                            res = yield v
                            v = ev.send(res)
                    except StopIteration as e:
                        res = e.value or v

                        dat.update({key: res})
                return dat
            
        elif isinstance(data, list):
            dat = []
            for item in data:

                ev = self._generatorEvaluateFunction(function_memory, item)
                try:
                    v = ev.send(None)
                    while isinstance(v, (EngineOperation, _EngineOperation)):
                        res = yield v
                        v = ev.send(res)
                except StopIteration as e:
                    res = e.value or v

                dat.append(res)
            return dat
        else:
            return data

    def _evaluateFunction(self, function_memory:FunctionMemory, data:dict):
        engine = function_memory.engine
        
        if isinstance(data, dict):
            if (funcs := data.get("functions", None)) is not None:
                if (predicate := data.get("predicate", None)) is not None:
                    if not function_memory.checkPredicate(predicate): return None
                result = None
                for func in funcs:
                    res = self._evaluateFunction(function_memory, func)
                    if res: result = res
                return result
            elif (func := data.get("function", None)) is not None:
                if f := self.loader_function.getFunction(func):
                    f: LoaderFunction
                    # Check predicate
                    if (predicate := data.get("predicate", None)) is not None:
                        if not function_memory.checkPredicate(predicate): return None
                    # Run function
                    args = {}
                    for key, item in data.items(): # gather the arguments for the function
                        if key in ["function", "#store", "predicate"]: continue # skip the function's id, predicate, and the special #store operator
                        if isinstance(item, dict):
                            args.update({key: self._evaluateFunction(function_memory, item)})
                        else:
                            args.update({key: item})
                    r = f._call(function_memory, args)
                    # if a #store operator was present with the function, the function's result is assigned to the name in #store
                    if var := data.get("#store", None):
                        var: str
                        if var.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{var}'")
                        function_memory.store(var, r)
                    return r
            elif (var := data.get("#ref", None)) is not None:
                return function_memory.ref(var)
            elif (store := data.get("#store", None)) is not None:
                if isinstance(store, dict):
                    for key, value in store.items():
                        if key.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{key}'")
                        function_memory.store(key, value)
            elif (check := data.get("@check", None)) is not None:
                res = self._evaluateFunction(function_memory, check)
                if res and ((true_branch := data.get("true", None)) is not None):
                    return self._evaluateFunction(function_memory, true_branch)
                elif (false_branch := data.get("false", None)) is not None:
                    return self._evaluateFunction(function_memory, false_branch)
                else:
                    return None
            else:
                dat = {}
                for key, item in data.items():
                    dat.update({key: self._evaluateFunction(function_memory, item)})
                return dat
        elif isinstance(data, list):
            dat = []
            for item in data:
                dat.append(self._evaluateFunction(function_memory, item))
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
    
    def constructGameObject(self, function_memory:FunctionMemory, data:dict) -> GameObject:
        Log["loadup"]["loader"]("Constructing new GameObject...")
        if obj_type := data.get("type", None):
            identifier = Identifier.fromString(obj_type)
            identifier.path = "abstract/"
            nm = identifier.full()
            if tp := AbstractGameObject._game_object_types.get(nm, None):
                if parent := data.get("parent", None):
                    if abstract := tp._loaded.get(parent, None):
                        Log["loadup"]["loader"]("GameObject Construction complete")
                        return abstract.createInstance(function_memory, **data)
                    raise InvalidObjectError(f"No parent GameObject with id: '{parent}'")
            raise InvalidObjectError(f"GameObject type: '{nm}' does not exist")
        elif parent := data.get("parent", None):
            ...
            # determine parent type
        else:
            raise InvalidObjectError("No type or parent given for GameObject")


    @TextPattern(r"\b(?:equip) *(?P<item_name>.*)\b")
    @staticmethod
    def checkTextEquip(function_memory:FunctionMemory, player:Player, raw_text:str, groupdict:dict):
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
                    function_memory.engine.sendOutput(player, f"You have no Weapon, Armor, or Tool called '{item_name}'")

    @TextPattern(r"\b(?P<keyword>use|eat|throw|apply|drink)(?: *(?P<amount>[1-9][0-9]*|an?|the|(?:some|all) *(?:(?:of *)?(?:the|my)))?)? *(?P<item_name>.*)\b")
    @staticmethod
    def checkTextUse(function_memory:FunctionMemory, player:Player, raw_text:str, groupdict:dict):
        keyword: str = groupdict["keyword"]
        
        item_name: str = groupdict["item_name"]

        amount: int = TextPattern.interpretAmount(groupdict["amount"])

        found_item = False
        for item in player.inventory.getOfType(Item):
            item: Item
            if item.name.lower().strip() == item_name.lower().strip():
                found_item = True
                if item.checkKeyword(keyword):
                    
                    function_memory_1 = FunctionMemory(function_memory.engine)
                    function_memory_1.addContextData({
                        "#player": player,
                        "#item": item
                    })
                    return item.onUse(function_memory_1, amount)

        if not found_item:
            if tool := player.inventory.getEquipped(Tool):
                tool: Tool
                if tool.name.lower().strip() == item_name.lower().strip():
                    found_item = True
                    if tool.checkKeyword(keyword):
                        function_memory_1 = FunctionMemory(function_memory.engine)
                        function_memory_1.addContextData({
                            "#player": player,
                            "#tool": tool
                        })
                        return tool.onUse(function_memory_1, amount)

        if not found_item:
            function_memory.engine.sendOutput(player, f"You do not have '{item_name}'")

        


    @TextPattern(r"\b(inventory|bag|items)\b", TextPattern.CheckType.SEARCH)
    @staticmethod
    def checkTextInventory(function_memory, player:Player, raw_text:str, groupdict:dict):
        function_memory.engine.sendOutput(player, player.inventory.fullStats(function_memory.engine))

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

    def getGameObject(self, identifier) -> AbstractGameObject:
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
