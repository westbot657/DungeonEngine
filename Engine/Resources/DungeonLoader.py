# pylint: disable=[W,R,C,import-error]

from .AbstractAmmo import AbstractAmmo, Ammo
from .AbstractArmor import AbstractArmor, Armor
from .AbstractAttack import AbstractAttack, Attack
from .AbstractEnemy import AbstractEnemy, Enemy
from .AbstractCombat import AbstractCombat, Combat
from .AbstractDungeon import AbstractDungeon, Dungeon
from .AbstractItem import AbstractItem, Item
from .AbstractRoom import AbstractRoom, Room
from .AbstractStatusEffect import AbstractStatusEffect, StatusEffect, StatusEffectCause
from .StatusEffectManager import StatusEffectManager
from .AbstractTool import AbstractTool, Tool
from .AbstractWeapon import AbstractWeapon, Weapon
from .Functions import LoaderFunction
from .Identifier import Identifier
from .EngineDummy import Engine
from .EngineErrors import InvalidObjectError, FunctionLoadError, LocationError
from .LootTable import LootTable
from .TextPattern import TextPattern
from .Player import Player
from .AbstractGameObject import AbstractGameObject, GameObject
from .Util import Util
from .Currency import Currency
from .Logger import Log
from .FunctionMemory import FunctionMemory
from .EngineOperation import EngineOperation, _EngineOperation
from .Location import Location
from .Position import Position
from .Environment import Environment
from .AbstractInteractable import AbstractInteractable, Interactable
from .Entity import Entity
from .DynamicValue import DynamicValue
from .ES2 import EngineScript
from .Serializer import Serializer, Serializable
from .YieldTools import YieldTools


from typing import Any, Generator
import re, time, random

@Serializable("DungeonLoader")
class DungeonLoader:

    _loader = None
    def __new__(cls):
        if not cls._loader:
            cls._loader = self = super().__new__(cls)
            self.init()
        return cls._loader

    def init(self):
        self.loader_function = LoaderFunction # this can't be serialized
        self.abstract_ammo: dict[str, AbstractAmmo] = {}
        self.abstract_armor: dict[str, AbstractArmor] = {}
        self.abstract_attacks: dict[str, AbstractAttack] = {}
        self.abstract_combats: dict[str, AbstractCombat] = {}
        self.abstract_dungeons: dict[str, AbstractDungeon] = {}
        self.dungeons: dict[str, Dungeon] = {}
        self.abstract_enemies: dict[str, AbstractEnemy] = {}
        self.abstract_items: dict[str, AbstractItem] = {}
        self.abstract_interactables: dict[str, AbstractInteractable] = {}
        #self.abstract_loot_tables: dict[str, AbstractLootTable] = {}
        self.abstract_rooms: dict[str, AbstractRoom] = {}
        self.abstract_status_effects: dict[str, AbstractStatusEffect] = {}
        self.abstract_tools: dict[str, AbstractTool] = {}
        self.abstract_weapons: dict[str, AbstractWeapon] = {}
        self.players = {}
        
        self._load_current = None
        self._load_progress = [0, 0] # i0 = overall load progress; i1 = progress of _load_current
        self._load_grid = [""]
        
        self.gen_eval_depth = 0

        self.classes = { # This can't be serialized
            "Player": Player,
            "Enemy": Enemy,
            "Attack": Attack,
            "Weapon": Weapon,
            "Armor": Armor,
            "Ammo": Ammo,
            "Tool": Tool,
            "Combat": Combat,
            "Item": Item,
            "Room": Room,
            "Dungeon": Dungeon,
            "Interactable": Interactable,
            "StatusEffect": StatusEffect,
            "StatusEffectCause": StatusEffectCause,
            "StatusEffectManager": StatusEffectManager
        }

    def serialize(self):
        return {
            "abstract_ammo": Serializer.serialize(self.abstract_ammo),
            "abstract_armor": Serializer.serialize(self.abstract_armor),
            "abstract_attacks": Serializer.serialize(self.abstract_attacks),
            "abstract_combats": Serializer.serialize(self.abstract_combats),
            "abstract_dungeons": Serializer.serialize(self.abstract_dungeons),
            "dungeons": Serializer.serialize(self.dungeons),
            "abstract_enemies": Serializer.serialize(self.abstract_enemies),
            "abstract_items": Serializer.serialize(self.abstract_items),
            "abstract_interactables": Serializer.serialize(self.abstract_interactables),
            "abstract_rooms": Serializer.serialize(self.abstract_rooms),
            "abstract_status_effects": Serializer.serialize(self.abstract_status_effects),
            "abstract_tools": Serializer.serialize(self.abstract_tools),
            "abstract_weapons": Serializer.serialize(self.abstract_weapons),
            "players": Serializer.serialize(self.players)
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        cls._loader = instance
        Serializer.smartDeserialize(instance, data)
        
        instance.loader_function = LoaderFunction # this can't be serialized
        instance.classes = { # This can't be serialized
            "Player": Player,
            "Enemy": Enemy,
            "Attack": Attack,
            "Weapon": Weapon,
            "Armor": Armor,
            "Ammo": Ammo,
            "Tool": Tool,
            "Combat": Combat,
            "Item": Item,
            "Room": Room,
            "Dungeon": Dungeon,
            "Interactable": Interactable,
            "StatusEffect": StatusEffect,
            "StatusEffectCause": StatusEffectCause,
            "StatusEffectManager": StatusEffectManager
        }
        

    def evaluateFunction(self, function_memory:FunctionMemory, data:dict):
        val = self._evaluateFunction(function_memory, data)
        return val

    def scanFunction(self, function_memory:FunctionMemory, data:Any, allowed_functions:list, disallowed_functions:list):
        return not self._scanFunction(function_memory, data, allowed_functions, disallowed_functions)
    
    def _scanFunction(self, function_memory:FunctionMemory, data:Any, allowed_functions:list, disallowed_functions:list):
        if isinstance(data, dict):
            if (func := data.get("function", None)) is not None:
                func: str
                if not any(func.startswith(a) for a in allowed_functions):
                    return True
                if any(func.startswith(d) for d in disallowed_functions):
                    return True
                for key, item in data.items():
                    if key in ["function"]: continue
                    if self._scanFunction(function_memory, item, allowed_functions, disallowed_functions):
                        return True
            else:
                for key, item in data.items():
                    if self._scanFunction(function_memory, item, allowed_functions, disallowed_functions):
                        return True
        elif isinstance(data, list):
            for item in data:
                if self._scanFunction(function_memory, item, allowed_functions, disallowed_functions):
                    return True
        return False

    def generatorEvaluateFunction(self, function_memory:FunctionMemory, data:dict):
        yieldTools = YieldTools(f"DungeonLoader.generatorEvaluateFunction#{id(self)}")
        yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, data)
        return yieldTools.result()

    def _genEvalFunction(self, function_memory:FunctionMemory, data:Any, prepEval:bool=False):
        self.gen_eval_depth += 1
        yieldTools = YieldTools(f"DungeonLoader._genEvalFunction#{id(self)}:{self.gen_eval_depth}")
        v = None
        if isinstance(data, dict):
            
            if (script_file := data.get("#script", None)) is not None:
                d = EngineScript(script_file)
                data.clear()
                data.update(d.getScript())
                yield from yieldTools.call(self._genEvalFunction, function_memory, d.getScript())
                self.gen_eval_depth -= 1
                return yieldTools.result()
            
            elif (funcs := data.get("#functions", None)) is not None:
                result = None
                
                if isinstance(funcs, list):
                    for f in funcs:
                        yield from yieldTools.call(self._genEvalFunction, function_memory, f)
                        v = yieldTools.result()
                        if v: result = v
                    self.gen_eval_depth -= 1
                    return result
                
                elif isinstance(funcs, dict):
                    yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, funcs)
                    self.gen_eval_depth -= 1
                    return yieldTools.result()
                
            elif (func := data.get("#function", None)) is not None:
                if f := self.loader_function.getFunction(func):
                    f: LoaderFunction
                    args = {}
                    
                    for key, item in data.items():
                        if key in ["#function"]: continue
                        if (isinstance(item, dict) or isinstance(item, list)) and (not prepEval) and f.pre_evaluate_args:
                            args.update({key: self._generatorEvaluateFunction(function_memory, item)})
                        else:
                            args.update({key: item})
                            
                    r = f._call(function_memory, args)
                    if isinstance(r, Generator):
                        yield from yieldTools.handle(r)
                        res = yieldTools.result()
                    elif isinstance(r, Combat.Operation._Operation):
                        yield r
                        self.gen_eval_depth -= 1
                        return
                    else:
                        res = r

                    self.gen_eval_depth -= 1
                    return res
            elif (var := data.get("#ref", None)) is not None:
                self.gen_eval_depth -= 1
                return function_memory.ref(var)
            
            

    def _generatorEvaluateFunction(self, function_memory:FunctionMemory, data:Any, prepEval:bool=False):
        self.gen_eval_depth += 1
        yieldTools = YieldTools(f"DungeonLoader._generatorEvaluateFunction#{id(self)}:{self.gen_eval_depth}")
        v = None
        if isinstance(data, dict):
            if (script_file := data.get("#script", None)) is not None:
                d = EngineScript(script_file)
                data.clear()
                data.update(d.getScript())
                yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, d.getScript())
                self.gen_eval_depth -= 1
                return yieldTools.result()
            elif (funcs := data.get("functions", None)) is not None:
                if (predicate := data.get("predicate", None)) is not None:
                    if not function_memory.checkPredicate(predicate): return None
                result = None
                if isinstance(funcs, list):
                    for func in funcs:
                        yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, func)
                        v = yieldTools.result()
                        if v: result = v
                    self.gen_eval_depth -= 1
                    return result
                elif isinstance(funcs, dict):
                    yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, funcs)
                    self.gen_eval_depth -= 1
                    return yieldTools.result()
            elif (func := data.get("function", None)) is not None:
                if f := self.loader_function.getFunction(func):
                    f: LoaderFunction
                    if (predicate := data.get("predicate", None)) is not None:
                        if not function_memory.checkPredicate(predicate): return None
                    args = {}
                    for key, item in data.items():
                        if key in ["function", "#store", "predicate"]: continue
                        if (isinstance(item, dict) or (isinstance(item, list) and (not prepEval))) and f.pre_evaluate_args:
                            yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, item)
                            args.update({key: yieldTools.result()})
                        else:
                            args.update({key: item})
                    r = f._call(function_memory, args)
                    if isinstance(r, Generator):
                        yield from yieldTools.handle(r)
                        res = yieldTools.result()
                    elif isinstance(r, Combat.Operation._Operation):
                        # print(f"\033[38;2;255;0;0mCOMBAT TASK FROM FUNCTION!\033[0m")
                        yield r
                        self.gen_eval_depth -= 1
                        return
                    else:
                        res = r
                    if var := data.get("#store", None):
                        var: str
                        if var.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{var}'")
                        function_memory.store(var, res)
                    if var := data.get("#store-player", None):
                        var: str
                        if var.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{var}'")
                        dungeon_name = function_memory.context_data.get("#dungeon", "global")
                        function_memory.ref("#player").store(dungeon_name, var, res)
                    self.gen_eval_depth -= 1
                    return res
                else:
                    ...
                    # TODO: function doesn't exist, do something (raise error)
            elif (var := data.get("#ref", None)) is not None:
                self.gen_eval_depth -= 1
                return function_memory.ref(var)
            elif (var := data.get("#ref-player", None)) is not None:
                dungeon_name = function_memory.context_data.get("#dungeon", "global")
                self.gen_eval_depth -= 1
                return function_memory.ref("#player").ref(dungeon_name, var)
            
            elif (func_name := data.get("#call", None)) is not None:
                _func_mem = FunctionMemory(function_memory.engine)
                _func_mem.context_data = function_memory.context_data
                if (args := data.get("parameters", None)) is not None:
                    args: dict
                    for key, val in args.items():
                        yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, val)
                        v = yieldTools.result()
                        _func_mem.update({key: v})
                yield from yieldTools.call(_func_mem.call, func_name)
                if (store := data.get("#store", None)) is not None:
                    function_memory.update({
                        store: v
                    })
                self.gen_eval_depth -= 1
                return v
            
            elif (store := data.get("#store", None)) is not None:
                if isinstance(store, dict):
                    for key, value in store.items():
                        key: str
                        if key.startswith(("%")): raise MemoryError(f"Cannot create a variable with prefix '%': '{key}'")
                        elif key.startswith("$"):
                            function_memory.store(key, value)
                        else:
                            yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, value)
                            v = yieldTools.result()
                            function_memory.store(key, v)
            elif (store := data.get("#store-player", None)) is not None:
                if isinstance(store, dict):
                    dungeon_name = function_memory.context_data.get("#dungeon", "global")
                    for key, value in store.items():
                        if key.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{key}'")
                        function_memory.ref("#player").store(dungeon_name, key, value)
            elif (check := data.get("@check", None)) is not None:
                yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, check)
                res = yieldTools.result()
                if res and ((true_branch := data.get("true", None)) is not None):
                    yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, true_branch)
                    v = yieldTools.result()
                    self.gen_eval_depth -= 1
                    return v
                elif (false_branch := data.get("false", None)) is not None:
                    yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, false_branch)
                    v = yieldTools.result()
                    self.gen_eval_depth -= 1
                    return v
                else:
                    self.gen_eval_depth -= 1
                    return None
            else:
                dat = {}
                for key, item in data.items():
                    yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, item)
                    v = yieldTools.result()
                    dat.update({key: v})
                self.gen_eval_depth -= 1
                return dat
        elif isinstance(data, list):
            dat = []
            for item in data:
                yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, item, True)
                v = yieldTools.result()
                dat.append(v)
            self.gen_eval_depth -= 1
            return dat
        elif isinstance(data, EngineScript):
            yield from yieldTools.call(self._generatorEvaluateFunction, function_memory, data.getScript())
            v = yieldTools.result()
            self.gen_eval_depth -= 1
            return v
        else:
            self.gen_eval_depth -= 1
            return data

    # TODO: Validate that this runs in parity to _generatorEvaluateFunction
    def _evaluateFunction(self, function_memory:FunctionMemory, data:dict):
        if isinstance(data, dict):
            if (script_file := data.get("#script", None)) is not None:
                d = EngineScript(script_file)
                data.clear()
                data.update(d.getScript())
                return self._evaluateFunction(function_memory, d.getScript())
            elif (funcs := data.get("functions", None)) is not None:
                if (predicate := data.get("predicate", None)) is not None:
                    if not function_memory.checkPredicate(predicate): return None
                result = None
                if isinstance(funcs, list):
                    for func in funcs:
                        res = self._evaluateFunction(function_memory, func)
                        if res: result = res
                    return result
                elif isinstance(funcs, dict):
                    return self._evaluateFunction(function_memory, funcs)
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
                    if var := data.get("#store-player", None):
                        var: str
                        if var.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{var}'")
                        dungeon_name = function_memory.context_data.get("#dungeon", "global")
                        function_memory.ref("#player").store(dungeon_name, var, res)
                    return r
            elif (var := data.get("#ref", None)) is not None:
                return function_memory.ref(var)
            elif (var := data.get("#ref-player", None)) is not None:
                dungeon_name = function_memory.context_data.get("#dungeon", "global")
                return function_memory.ref("#player").ref(dungeon_name, var)
            
            elif (func_name := data.get("#call", None)) is not None:
                _func_mem = FunctionMemory(function_memory.engine)
                _func_mem.context_data = function_memory.context_data
                if (args := data.get("parameters", None)) is not None:
                    args: dict
                    for key, val in args.items():
                        v = self._evaluateFunction(function_memory, val)
                        _func_mem.update({key: v})
                v = _func_mem.call2(func_name)
                
                if (store := data.get("#store", None)) is not None:
                    function_memory.update({
                        store: v
                    })
                return v
            
            elif (store := data.get("#store", None)) is not None:
                if isinstance(store, dict):
                    for key, value in store.items():
                        key: str
                        if key.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{key}'")
                        elif key.startswith("$"):
                            function_memory.store(key, value)
                        else:
                            v = self._evaluateFunction(function_memory, value)
                            function_memory.store(key, v)
            elif (store := data.get("#store-player", None)) is not None:
                if isinstance(store, dict):
                    dungeon_name = function_memory.context_data.get("#dungeon", "global")
                    for key, value in store.items():
                        if key.startswith(("#", "%")): raise MemoryError(f"Cannot create a variable with prefix '#' or '%': '{key}'")
                        function_memory.ref("#player").store(dungeon_name, key, value)
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
        elif isinstance(data, EngineScript):
            return self._evaluateFunction(function_memory, data.getScript())
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
        Log["loadup"]["loader"](f"Constructing new GameObject: data={data}")
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

    def getLocation(self, function_memory:FunctionMemory, location:Location) -> Room|Dungeon:
        for dungeon_name, dungeon in function_memory.engine.loader.dungeons.items():
            dungeon_name: str
            dungeon: Dungeon
            location = Location.fromString(location)

            if location.full() == dungeon_name:
                return dungeon

            name = dungeon_name.split(":", 1)[1]
            
            if location.dungeon == name:
                if (room := dungeon.rooms.get(location.full(), None)) is not None:
                    return room
                elif (not location.room_path) and (not location.room):
                    return dungeon
        raise LocationError(f"Could not find location: '{location.full()}'")

    # TODO: 
    def getSaveData(self, function_memory:FunctionMemory, obj:Any):
        match obj:
            case str()|int()|float()|bool():
                return obj
            case list():
                return [self.getSaveData(function_memory, o) for o in obj]
            case dict():
                d = {"%ENGINE:DATA-TYPE%": "dict"}
                for key, value in obj:
                    d.update({key: self.getSaveData(function_memory, value)})
                return d
            case Ammo(): ...
            case Armor(): ...
            case Attack(): ...
            case Combat(): ...
            case DynamicValue(): ...
            case Enemy(): ...
            case Environment(): ...
            case Identifier():
                return {
                    "%ENGINE:DATA-TYPE%": "Identifier",
                    "value": obj.full()
                }
            case Currency(): ...
            case Interactable(): ...
            case Item(): ...
            case Location():
                return {
                    "%ENGINE:DATA-TYPE%": "Location",
                    "value": obj.full()
                }
            case LootTable(): ...
            case Player():
                return {
                    "%ENGINE:DATA-TYPE%": "Player",
                    "id": obj.uuid
                }
            case Position():
                return {
                    "%ENGINE:DATA-TYPE%": "Position",
                    "x": obj.x,
                    "y": obj.y
                }
            case StatusEffect(): ...
            case Tool(): ...
            case Weapon(): ...

            case _:
                raise Exception(f"Unrecognized object type for: {obj}")

    def rebuildData(self, function_memory:FunctionMemory, data:Any):
        ...

    @TextPattern(r"\b(?:[Ee]quip) *(?P<item_name>.*)\b", TextPattern.CheckType.SEARCH, ["common"])
    @staticmethod
    def checkTextEquip(function_memory:FunctionMemory, player:Player, raw_text:str, groupdict:dict):
        item_name: str = groupdict["item_name"].strip()

        for weapon in player.inventory.getOfType(Weapon):
            weapon: Weapon
            if weapon.name.lower() == item_name.lower():
                player.inventory.equip("engine:weapon", weapon)
                function_memory.engine.sendOutput(player, f"You equipped `{weapon.name}`")
                break
        else:
            for armor in player.inventory.getOfType(Armor):
                armor: Armor
                if armor.name.lower() == item_name.lower():
                    player.inventory.equip("engine:armor", armor)
                    function_memory.engine.sendOutput(player, f"You equipped `{armor.name}`")
                    break
            else:
                for tool in player.inventory.getOfType(Tool):
                    tool: Tool
                    if tool.name.lower() == item_name.lower():
                        player.inventory.equip("engine:tool", tool)
                        function_memory.engine.sendOutput(player, f"You equipped `{tool.name}`")
                        break
                else:
                    for ammo in player.inventory.getOfType(Ammo):
                        ammo: Ammo
                        if ammo.name.lower() == item_name.lower():
                            player.inventory.equip("engine:ammo", ammo)
                            function_memory.engine.sendOutput(player, f"You equipped `{ammo.name}`")
                            break
                    else:
                        function_memory.engine.sendOutput(player, f"You have no Weapon, Armor, Tool, or Ammo called '{item_name}'")

    @TextPattern(r"\b(?P<keyword>[Uu]se|[Ee]at|[Tt]hrow|[Aa]pply|[Dd]rink)\b *(?P<item_name>.*)", TextPattern.CheckType.SEARCH, ["common"])
    @staticmethod
    def checkTextUse(function_memory:FunctionMemory, player:Player, raw_text:str, groupdict:dict):
        keyword: str = groupdict["keyword"]
        item_name: str = groupdict["item_name"]

        found_item = False
        for item in player.inventory.getOfType(Item, "last"):
            item: Item
            if item.name.lower().strip() == item_name.lower().strip():
                found_item = True
                if item.checkKeyword(keyword):
                    
                    function_memory_1 = FunctionMemory(function_memory.engine)
                    function_memory_1.addContextData({
                        "#player": player,
                        "#item": item
                    })
                    return item.onUse(function_memory_1, player.inventory)

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
                        return tool.onUse(function_memory_1)

        if not found_item:
            function_memory.engine.sendOutput(player, f"You do not have '{item_name}'")

    @TextPattern(r"\b(?:[Ii]nventory|[Bb]ag|[Ii]tems)\b", TextPattern.CheckType.SEARCH, ["global"])
    @staticmethod
    def checkTextInventory(function_memory:FunctionMemory, player:Player, raw_text:str, groupdict:dict):
        if "full" in raw_text:
            function_memory.engine.sendOutput(player, player.fullInventoryStats(function_memory))
        else:
            function_memory.engine.sendOutput(player, player.quickInventoryStats(function_memory))

    @TextPattern(r"\b(?:[Cc]ombat|[Bb]attle|[Ss]tats)\b", TextPattern.CheckType.SEARCH, ["global"])
    @staticmethod
    def checkTextCombat(function_memory:FunctionMemory, player:Player, raw_text:str, groupdict:dict):
        if player.in_combat:
            if player._combat:
                function_memory.engine.sendOutput(player, player._combat.fullStats(function_memory))
        else:
            function_memory.engine.sendOutput(player, "You are not in combat")

    _element_types = {
        "engine:text": str,
        "engine:boolean": bool,
        "engine:list": list,
        "engine:number": (int, float),
        "engine:weapon": Weapon,
        "engine:ammo": Ammo,
        "engine:armor": Armor,
        "engine:tool": Tool,
        "engine:item": Item,
        "engine:status_effect": StatusEffect,
        "engine:status_effect_cause": StatusEffectCause,
        "engine:room": Room,
        "engine:dungeon": Dungeon,
        "engine:loot_table": LootTable,
        "engine:player": Player,
        "engine:enemy": Enemy,
        "engine:entity": Entity,
        "engine:attack": Attack,
        "engine:combat": Combat,
        "engine:environment": Environment,
        "engine:location": Location,
        "engine:position": Position,
        "engine:interactable": Interactable,
        "engine:identifier": Identifier,
        "engine:currency": Currency,
        "engine:dict": dict
    }
    def isElementOfType(self, element:Any, element_type:str):
        return isinstance(
            element,
            self._element_types.get(element_type, None)
        )

    def console_load_bars(self):
        ...

    def loadGame(self, engine:Engine):

        start_time = time.time()

        if engine.is_console:
            Log.silent = True

        EngineScript.load()
        EngineScript.preCompileAll()

        Log["loadup"]["loader"]("Loading Abstract Status Effects...")
        self.abstract_status_effects = AbstractStatusEffect.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Ammo...")
        self.abstract_ammo = AbstractAmmo.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Armor...")
        self.abstract_armor = AbstractArmor.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Tools...")
        self.abstract_tools = AbstractTool.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Weapons...")
        self.abstract_weapons = AbstractWeapon.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Items...")
        self.abstract_items = AbstractItem.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Attacks...")
        self.abstract_attacks = AbstractAttack.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Enemies...")
        self.abstract_enemies = AbstractEnemy.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Combats...")
        self.abstract_combats = AbstractCombat.loadData(engine)
        
        Log["loadup"]["loader"]("Loading Abstract Interactables...")
        self.abstract_interactables = AbstractInteractable.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Rooms...")
        self.abstract_rooms = AbstractRoom.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Dungeons...")
        self.abstract_dungeons: list[AbstractDungeon] = AbstractDungeon.loadData(engine)

        Log["loadup"]["loader"]("Loading Dungeons...")
        self.dungeons = {}
        for k, v in self.abstract_dungeons.items():
            self.dungeons.update({k: v.createInstance(engine._function_memory)})

        for dungeon in self.dungeons.values():
            for room in dungeon.rooms.values():
                room: Room
                room.onLoad(engine._function_memory)

        Log["loadup"]["loader"]("Loading Players...")
        self.players = Player.loadData(engine)

        FunctionMemory.global_environment_variables.update({
            "%dungeons": self.dungeons,
            "%players": self.players
        })

        Log.silent = False

        Log["loadup"]["loader"]("Engine resource loading completed")

        Log["loadup"]["loader"](f"Loading finished in {time.time()-start_time} seconds")

    def saveGame(self, engine:Engine):
        # TODO: implement saving

        Log["loadup"]["loader"]("Saving Dungeons...")
        AbstractDungeon.saveData(engine._function_memory)

        Log["loadup"]["loader"]("Saving Players...")
        Player.saveData(engine._function_memory)

        Log["loadup"]["loader"]("Finished saving")

    def unloadGame(self):

        Log["loader"]["shutdown"]("Unloading Weapons")
        AbstractWeapon._loaded.clear()
        self.abstract_weapons.clear()

        Log["loader"]["shutdown"]("Unloading Ammo")
        AbstractAmmo._loaded.clear()
        self.abstract_ammo.clear()

        Log["loader"]["shutdown"]("Unloading Armor")
        AbstractArmor._loaded.clear()
        self.abstract_armor.clear()

        Log["loader"]["shutdown"]("Unloading Tools")
        AbstractTool._loaded.clear()
        self.abstract_tools.clear()

        Log["loader"]["shutdown"]("Unloading Items")
        AbstractItem._loaded.clear()
        self.abstract_items.clear()

        Log["loader"]["shutdown"]("Unloading Combats")
        AbstractCombat._loaded.clear()
        self.abstract_combats.clear()

        Log["loader"]["shutdown"]("Unloading Enemies")
        AbstractEnemy._loaded.clear()
        self.abstract_enemies.clear()

        Log["loader"]["shutdown"]("Unloading Attacks")
        AbstractAttack._loaded.clear()
        self.abstract_attacks.clear()

        Log["loader"]["shutdown"]("Unloading Interactables")
        AbstractInteractable._loaded.clear()
        self.abstract_interactables.clear()

        Log["loader"]["shutdown"]("Unloading Dungeons")
        AbstractDungeon._loaded.clear()
        self.abstract_dungeons.clear()
        self.dungeons.clear()

        Log["loader"]["shutdown"]("Unloading Rooms")
        AbstractRoom._loaded.clear()
        self.abstract_rooms.clear()

        Log["loader"]["shutdown"]("Unloading Status Effects")
        AbstractStatusEffect._loaded.clear()
        self.abstract_status_effects.clear()

        Log["loader"]["shutdown"]("Unloading Scripts")
        EngineScript.unload()


