# pylint: disable=[W,R,C,import-error]

try:
    from .LoaderFunction import LoaderFunction
    from .Identifier import Identifier
    from .LootTable import LootTable
    from .EngineDummy import Engine
    from .EngineOperation import EngineOperation, _EngineOperation
    from .EngineErrors import LocationError, FunctionError
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
    from .FunctionMemory import FunctionMemory
    from .Player import Player
    from .Logger import Log
    from .Interactable import Interactable
    from .Util import Util
    from .Location import Location
except ImportError:
    from LoaderFunction import LoaderFunction
    from Identifier import Identifier
    from LootTable import LootTable
    from EngineDummy import Engine
    from EngineOperation import EngineOperation, _EngineOperation
    from EngineErrors import LocationError, FunctionError
    from AbstractAmmo import AbstractAmmo, Ammo
    from AbstractArmor import AbstractArmor, Armor
    from AbstractAttack import AbstractAttack, Attack
    from AbstractCombat import AbstractCombat, Combat
    from AbstractDungeon import AbstractDungeon, Dungeon
    from AbstractEnemy import AbstractEnemy, Enemy
    from AbstractItem import AbstractItem, Item
    from AbstractRoom import AbstractRoom, Room
    from AbstractStatusEffect import AbstractStatusEffect, StatusEffect
    from AbstractTool import AbstractTool, Tool
    from AbstractWeapon import AbstractWeapon, Weapon
    from FunctionMemory import FunctionMemory
    from Player import Player
    from Logger import Log
    from Interactable import Interactable
    from Util import Util
    from Location import Location

from typing import Any

import random, math, re

"""
functions:

# v Tool v #
engine:tool/cancel_use
engine:tool/get_durability
engine:tool/set_durability
engine:tool/set_max_durability
engine:tool/get_max_durability
# ^ Tool ^ #

# v Player v #
engine:player/message
engine:player/give_item
engine:player/get_status_effect
enigne:player/give_status_effect
engine:player/has_status_effect
engine:player/get_health
engine:player/set_health
engine:player/get_max_health
engine:player/heal
engine:player/damage
engine:player/get_equipped_weapon
engine:player/get_equipped_armor
engine:player/has_item
engine:player/get_item
engine:player/get_input
engine:player/set_location
engine:player/get_location
# ^ Player ^ #

# v Status Effect v #
engine:status_effect/get_level
engine:status_effect/set_level
engine:status_effect/get_duration
engine:status_effect/set_duration
# ^ Status Effect ^ #

# v Weapon v #
engine:weapon/get_durability
engine:weapon/set_durability
engine:weapon/get_max_durability
engine:weapon/set_max_durability
engine:weapon/get_damage
engine:weapon/set_damage
engine:weapon/get_parent_type
engine:weapon/get_ammo_type
# ^ Weapon ^ #

# v Item v #
engine:item/get_count
engine:item/set_count
engine:item/get_max_count
# ^ Item ^ #

# v Armor v #
engine:armor/get_durability
engine:armor/set_durability
engine:armor/get_damage_reduction
engine:armor/set_damage_reduction
engine:armor/get_max_durability
engine:armor/set_max_durability
# ^ Armor ^ #

# v Ammo v #
engine:ammo/get_count
engine:ammo/set_count
engine:ammo/get_max_count
engine:ammo/get_parent_type
engine:ammo/get_bonus_damage
# ^ Ammo ^ #

# v Text v #
engine:text/builder
# ^ Text ^ #

# v Random v #
engine:random/uniform X
engine:random/weighted
# ^ Random ^ #

# v Logic v #
engine:logic/compare
# ^ Logic ^ #

# v Math v #
engine:math/solve
# ^ Math ^ #

# v Interaction v #
engine:interaction/interact
# ^ Interaction ^ #

# v  v #

# ^  ^ #

# v  v #


# quick replace regex stuff:

## ([a-zA-Z_]+) ([a-z_]+/)([a-z_]+)

class Engine_$1(LoaderFunction):
    id = Identifier("engine", "$2", "$3")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.$3
            case _: return None
    @staticmethod
    def $3(function_memory:FunctionMemory, **kwargs):
        ...

"""




####XXX#############XXX####
### XXX Engine Tool XXX####
####XXX#############XXX####

class Engine_Tool_CancelUse(LoaderFunction):
    id = Identifier("engine", "tool/", "cancel_use")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.cancel_use
    @staticmethod
    def cancel_use(function_memory:FunctionMemory):
        ... # idk what to do here yet <-- TODO

class Engine_Tool_GetDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "get_durability")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "tool": str()|dict() # FIXME: this may be incorrect syntax, I can't tell right now
            }: return cls.get_durability_given
            case _:
                if function_memory.ref("#tool"):
                    return cls.get_durability_ctx
                return None
    @staticmethod
    def get_durability_given(function_memory:FunctionMemory, tool):
        ...
    @staticmethod
    def get_durability_ctx(function_memory:FunctionMemory):
        ...

class Engine_Tool_SetDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "set_durability")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "tool": str()|dict(), # FIXME: this may be incorrect syntax, I can't tell right now
                "durability": int()
            }: return cls.get_durability_given
            case {
                "durability": int()
            }:
                if function_memory.tool:
                    return cls.get_durability_ctx
                return None
            case _: return None
    @staticmethod
    def get_durability_given(function_memory:FunctionMemory, tool):
        ...
    @staticmethod
    def get_durability_ctx(function_memory:FunctionMemory):
        ...

class Engine_Tool_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "get_max_durability")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Tool_GetName(LoaderFunction):
    id = Identifier("engine", "tool/", "get_name")
    return_type = str
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Tool_SetName(LoaderFunction):
    id = Identifier("engine", "tool/", "set_name")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
# ^ Tool ^ #

####XXX###############XXX####
### XXX Engine Weapon XXX ###
####XXX###############XXX####

class Engine_Weapon_GetDurability(LoaderFunction):
    id = Identifier("engine", "Weapon/", "GetDurability")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_SetDurability(LoaderFunction):
    id = Identifier("engine", "Weapon/", "SetDurability")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_max_durability")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_SetMaxDurability(LoaderFunction):
    id = Identifier("engine", "weapon/", "set_max_durability")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetDamage(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_damage")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_SetDamage(LoaderFunction):
    id = Identifier("engine", "weapon/", "set_damage")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetAmmoType(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_ammo_type")
    return_type = AbstractAmmo
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetParentType(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_parent_type")
    return_type = AbstractWeapon
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
# ^ Weapon ^ #

####XXX##############XXX####
### XXX Engine Armor XXX ###
####XXX##############XXX####

class Engine_Armor_GetDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "get_durability")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "set_durability")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "get_max_durability")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetMaxDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "set_max_durability")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_GetDamageReduction(LoaderFunction):
    id = Identifier("engine", "armor/", "get_damage_reduction")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetDamageReduction(LoaderFunction):
    id = Identifier("engine", "armor/", "set_damage_reduction")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
# ^ Armor ^ #

####XXX#############XXX####
### XXX Engine Ammo XXX ###
####XXX#############XXX####

class Engine_Ammo_GetCount(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_count")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_SetCount(LoaderFunction):
    id = Identifier("engine", "ammo/", "set_count")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetMaxCount(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_max_count")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetParentType(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_parent_type")
    return_type = AbstractAmmo
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetBonusDamage(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_bonus_damage")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
# ^ Ammo ^ #

####XXX#####################XXX####
### XXX Engine StatusEffect XXX ###
####XXX#####################XXX####

class Engine_StatusEffect_GetLevel(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_level")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "status_effect": StatusEffect()|None,
                "default": int()
            }: ...
            case _: return None
    @staticmethod
    def get_level(function_memory:FunctionMemory, status_effect:StatusEffect|None, default:int):
        if status_effect is not None:
            return status_effect.level
        return default
class Engine_StatusEffect_SetLevel(LoaderFunction):
    id = Identifier("engine", "status_effect/", "set_level")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetDuration(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_duration")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_SetDuration(LoaderFunction):
    id = Identifier("engine", "status_effect/", "set_duration")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetName(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_name")
    return_type = str
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetCause(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_cause")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
# ^ Status Effect ^ #

####XXX#############XXX####
### XXX Engine Item XXX ###
####XXX#############XXX####

class Engine_Item_GetCount(LoaderFunction):
    id = Identifier("engine", "item/", "get_count")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Item_SetCount(LoaderFunction):
    id = Identifier("engine", "item/", "set_count")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Item_GetMaxCount(LoaderFunction):
    id = Identifier("engine", "item/", "get_max_count")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
# ^ Item ^ #

####XXX###############XXX####
### XXX Engine Player XXX ###
####XXX###############XXX####

class Engine_Player_Message(LoaderFunction):
    id = Identifier("engine", "player/", "message")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "message": str()
            }: return cls.send_message
            case _: return None
    @staticmethod
    def send_message(function_memory:FunctionMemory, message:str):
        function_memory.engine.sendOutput(function_memory.ref("#player"), message)
        
class Engine_Player_GetHealth(LoaderFunction):
    id = Identifier("engine", "player/", "get_health")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SetHealth(LoaderFunction):
    id = Identifier("engine", "player/", "set_health")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "get_max_health")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SetMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "set_max_health")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_AddMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "add_max_health")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SubtractMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "subtract_max_health")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_Heal(LoaderFunction):
    id = Identifier("engine", "player/", "heal")
    return_type = int
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "amount": int() | dict()
            }: ...
            case _: return None
    @staticmethod
    def heal(function_memory:FunctionMemory, amount:int|dict):
        player = function_memory.ref("#player")
        player.addHealth(amount)
class Engine_Player_Damage(LoaderFunction):
    id = Identifier("engine", "player/", "damage")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GiveObject(LoaderFunction):
    id = Identifier("engine", "player/", "give_object")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "object": str()
            }: return cls.giveObject
            case _: return None
    @classmethod
    def giveObject(cls, function_memory:FunctionMemory, **kwargs):
        object_name = Identifier.fromString(kwargs.get("object"))
        count = int(kwargs.get("count", 1))

        game_object = function_memory.engine.loader.constructGameObject(
            function_memory,
            {
                "type": f"{object_name.namespace}:abstract/{object_name.path.strip('/').rstrip('s')}",
                "parent": object_name.full()
            }
        )


        if isinstance(game_object, (Ammo, Item)):
            game_object: Ammo|Item
            game_object.count = min(max(0, count), game_object.max_count)
        
        player: Player = function_memory.ref("#player")
        player.inventory.addObject(game_object)

        return game_object

class Engine_Player_GiveStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "give_status_effect")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_HasStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "has_status_effect")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_RemoveStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "remove_status_effect")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "get_status_effect")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "status_effect": str()|None,
                "default": dict()|None
            }: return cls.get_status_effect
            case _: return None
    @staticmethod
    def get_status_effect(function_memory, status_effect, default) -> StatusEffect:
        ...
class Engine_Player_HasItem(LoaderFunction):
    id = Identifier("engine", "player/", "has_item")
    return_type = bool
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_RemoveItem(LoaderFunction):
    id = Identifier("engine", "player/", "remove_item")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetItem(LoaderFunction):
    id = Identifier("engine", "player/", "get_item")
    return_type = Item
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedArmor(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_armor")
    return_type = Armor
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedWeapon(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_weapon")
    return_type = Weapon
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedTool(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_tool")
    return_type = Tool
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetInput(LoaderFunction): # NOTE: this function may (probably will) require special implementation
    id = Identifier("engine", "player/", "get_input")
    return_type = Tool
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.getInput
    
    @classmethod
    def getInput(cls, function_memory:FunctionMemory, **args):
        prompt = args.get("prompt", "")
        x = yield EngineOperation.GetInput(function_memory.ref("#player"), prompt)
        return x

class Engine_Player_SetLocation(LoaderFunction):
    id = Identifier("engine", "player/", "set_location")
    return_type = Tool
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        Log["debug"]["loader function"]["set location"]["check"](f"args: {args}")
        match args:
            case {
                "location": str()|Location()
            }: return cls.setLocation
            case _: return None

    @staticmethod
    def setLocation(function_memory:FunctionMemory, location):
        player: Player = function_memory.ref("#player")

        # NOTE: yield instead of return, otherwise the EngineOperation may be ignored
        yield EngineOperation.MovePlayer(player, location)

class Engine_Player_GetLocation(LoaderFunction):
    id = Identifier("engine", "player/", "get_location")
    return_type = Tool
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.getLocation

    @staticmethod
    def getLocation(function_memory:FunctionMemory):
        return function_memory.ref("#player").location.full()
# ^ Player ^ #

####XXX#################XXX####
### XXX Engine Location XXX ###
####XXX#################XXX####
class Engine_Location_Exists(LoaderFunction):
    id = Identifier("engine", "location/", "exists")
    return_type = bool
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "location": str()
            }: return cls.exists
            case _: return None

    @staticmethod
    def exists(function_memory:FunctionMemory, location):
        try:
            function_memory.getLocation(location)
            return True
        except LocationError:
            return False

# ^ Location ^ #

####XXX###############XXX####
### XXX Engine Random XXX ###
####XXX###############XXX####

class Engine_Random_Uniform(LoaderFunction):
    id = Identifier("engine", "random/", "uniform")
    pre_evaluate_args = False
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "min": int(),
                "max": int()
            }: return cls.rand_range
            case {
                "rolls": int(),
                "pool": list()
            }: return cls.uniform_list
            case _: return None
    @staticmethod
    def rand_range(function_memory:FunctionMemory, min:int, max:int):
        return random.randint(min, max)
    @staticmethod
    def uniform_list(function_memory:FunctionMemory, rolls:int, pool:list, roll_size:int=1):
        if roll_size > len(pool): raise FunctionError(f"Cannot pull more elements from list than are available")
        result = []
        for roll in range(rolls):
            _pool = pool.copy()
            for r in range(roll_size):
                p = random.choice(_pool)
                _pool.remove(p)
                result.append(p)
        return result

class Engine_Random_Weighted(LoaderFunction):
    id = Identifier("engine", "random/", "weighted")
    pre_evaluate_args = False
    @classmethod
    def chek(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "rolls": int(),
                "pool": dict()
            }: ...
            case _: return None
    @staticmethod
    def random_weighted(function_memory:FunctionMemory, rolls:int, pool:dict):
        weighted_list = []
        for weight, value in pool.items():
            for w in range(weight):
                weighted_list.append(value)
        result = []
        for roll in rolls:
            result.append(random.choice(weighted_list))


class Engine_Random_LootTable(LoaderFunction):
    id = Identifier("engine", "random/", "loot_table")
    pre_evaluate_args = False
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "rolls": int(),
                "pools": list()
            }: return cls.loot_table
            case _: return None
    @staticmethod
    def loot_table(function_memory:FunctionMemory, rolls:int, pools:list[dict]):
        table = LootTable.fromDict({"rolls": rolls, "pools": pools})
        return table.roll(function_memory)

# ^ Random ^ #

####XXX#############XXX####
### XXX Engine Text XXX ###
####XXX#############XXX####

class Engine_Text_Builder(LoaderFunction):
    id = Identifier("engine", "text/", "builder")
    return_type = str
    pre_evaluator = True
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "text": list()
            }: return cls.builder
            case _: return None

    @staticmethod
    def builder(function_memory:FunctionMemory, text:list, seperator:str|dict=" "):
        return seperator.join(str(t) for t in text)

class Engine_Text_Match(LoaderFunction):
    id = Identifier("engine", "text/", "match")
    pre_evaluate_args = False
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "text" in args:
            return cls.pattern_match
        return None
    @staticmethod
    def pattern_match(function_memory:FunctionMemory, **kwargs):
        text = kwargs.pop("text")

        if not isinstance(text, str):
            ev = function_memory.generatorEvaluateFunction(text)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            text = str(v)

        patterns: list[dict] = Util.deepCopy(kwargs.pop("matches"))

        for option in patterns:
            pattern = option.pop("pattern")
            if not isinstance(pattern, str):
                ev = function_memory.generatorEvaluateFunction(pattern)
                v = None
                try:
                    v = ev.send(None)
                    while isinstance(v, _EngineOperation):
                        res = yield v
                        v = ev.send(res)
                except StopIteration as e:
                    v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                pattern = str(v)
            
            if m := re.match(pattern, text):
                d = m.groupdict()
                if d:
                    function_memory.update(d)
                ev = function_memory.generatorEvaluateFunction(option)
                v = None
                try:
                    v = ev.send(None)
                    while isinstance(v, _EngineOperation):
                        res = yield v
                        v = ev.send(res)
                except StopIteration as e:
                    if isinstance(e.value, _EngineOperation):
                        yield e.value
                    else:
                        yield e.value or (v if not isinstance(v, _EngineOperation) else None)

class Engine_Text_Replace(LoaderFunction):
    id = Identifier("engine", "text/", "replace")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "text": str(),
                "sequence": str(),
                "replacement": str()
            }: return cls.replace
            case _: return None

    @staticmethod
    def replace(function_memory:FunctionMemory, text:str, sequence:str, replacement:str):
        return text.replace(sequence, replacement)

class Engine_Text_ReplacePattern(LoaderFunction):
    id = Identifier("engine", "text/", "replace_pattern")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "text": str(),
                "pattern": str(),
                "replacement": str()
            }: return cls.replace
            case _: return None

    @staticmethod
    def replace(function_memory:FunctionMemory, text:str, pattern:str, replacement:str):
        return re.sub(pattern, replacement, text)

class Engine_Text_Substring(LoaderFunction):
    id = Identifier("engine", "text/", "substring")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "text": str()
            } if any([n in args for n in ["start", "end"]]):
                return cls.substring
            case _: return None

    @staticmethod
    def substring(function_memory:FunctionMemory, text:str, start:int=0, end:int=None):
        return text[start:end]

class Engine_Text_Length(LoaderFunction):
    id = Identifier("engine", "text/", "length")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "text": str()
            }: return cls.length
            case _: return None
    @staticmethod
    def length(function_memory:FunctionMemory, text:str):
        return len(text)

class Engine_Text_SetCase(LoaderFunction):
    id = Identifier("engine", "text/", "set_case")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "text": str(),
                "case": str()
            } if args["case"] in ["upper", "lower", "title"]:
                return cls.setcase
            case _: return None
    @staticmethod
    def setcase(function_memory:FunctionMemory, text:str, case:str):
        if case == "upper":
            return text.upper()
        if case == "lower":
            return text.lower()
        if case == "title":
            return text.title()
        return text


# ^ Text ^ #


####XXX###############XXX####
### XXX Engine Number XXX ###
####XXX###############XXX####



# ^ Number ^ #

####XXX#############XXX####
### XXX Engine Dict XXX ###
####XXX#############XXX####

class Engine_Dict_ForEach(LoaderFunction):
    id = Identifier("engine", "dict/", "for_each")
    pre_evaluate_args = False
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "dict": dict(),
                "run": dict()
            }:
                return cls.for_each
            case _: return None

    @staticmethod
    def for_each(function_memory:FunctionMemory, **args):

        _dct: dict = args.get("dict")

        ev = function_memory.generatorEvaluateFunction(_dct)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield v
                v = ev.send(res)
        except StopIteration as e:
            v = e.value or (v if not isinstance(v, _EngineOperation) else None)
        dct = v

        func: dict = args.get("run")
        for key, val in dct.items():

            ev = function_memory.generatorEvaluateFunction(val)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            element = v

            function_memory.update({
                "key": key,
                "value": element
            })

            ev = function_memory.generatorEvaluateFunction(Util.deepCopy(func))
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    if isinstance(v, EngineOperation.StopLoop):
                        return
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                if isinstance(e.value, EngineOperation.StopLoop):
                    return

# ^ Dict ^ #


####XXX#############XXX####
### XXX Engine List XXX ###
####XXX#############XXX####

class Engine_List_ForEach(LoaderFunction):
    id = Identifier("engine", "list/", "for_each")
    pre_evaluate_args = False
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "list": list(),
                "run": list()
            }:
                return cls.for_each
            case _: return None

    @staticmethod
    def for_each(function_memory:FunctionMemory, **args):

        lst: list = args.get("list")
        func: dict = args.get("run")
        for l in lst:

            ev = function_memory.generatorEvaluateFunction(l)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            element = v

            function_memory.update({
                "element": element
            })

            ev = function_memory.generatorEvaluateFunction(Util.deepCopy(func))
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    if isinstance(v, EngineOperation.StopLoop):
                        return
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                if isinstance(e.value, EngineOperation.StopLoop):
                    break

class Engine_List_Subset(LoaderFunction):
    id = Identifier("engine", "list/", "subset")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case _: return None
    @staticmethod
    def _(function_memory:FunctionMemory, ):
        return
    
class Engine_List_Pop(LoaderFunction):
    id = Identifier("engine", "list/", "pop")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case _: return None
    @staticmethod
    def _(function_memory:FunctionMemory, ):
        return
    
class Engine_List_Append(LoaderFunction):
    id = Identifier("engine", "list/", "append")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case _: return None
    @staticmethod
    def _(function_memory:FunctionMemory, ):
        return

class Engine_List_Builder(LoaderFunction):
    id = Identifier("engine", "list/", "builder")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "list": list()
            }: return cls.list_builder
            case _: return None

    @staticmethod
    def list_builder(function_memory:FunctionMemory, **kwargs):
        _list = kwargs.get("list")
        return _list # idk if this will work the way I think it will...



# ^ List ^ #

####XXX################XXX####
### XXX Engine Control XXX ###
####XXX################XXX####

class Engine_Control_Break(LoaderFunction):
    id = Identifier("engine", "control/", "break")

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls._break
    @staticmethod
    def _break(function_memory:FunctionMemory):
        return EngineOperation.StopLoop()

class Engine_Control_Call(LoaderFunction):
    id = Identifier("engine", "control/", "call")
    pre_evaluate_args = False
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "method" in args:
            return cls._call
        return None
    @staticmethod
    def _call(function_memory:FunctionMemory, method:str, parameters:dict={}):
        func = {
            "#call": method,
            "parameters": parameters
        }
        ev = function_memory.generatorEvaluateFunction(func)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield v
                v = ev.send(res)
        except StopIteration as e:
            v = e.value or (v if not isinstance(v, _EngineOperation) else None)
        return v


# ^ Control ^ #


####XXX##############XXX####
### XXX Engine Logic XXX ###
####XXX##############XXX####
class Engine_Logic_Compare(LoaderFunction):
    id = Identifier("engine", "logic/", "compare")
    return_type = Tool
    pre_evaluator = True
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.compare
    @classmethod
    def compare(cls, function_memory:FunctionMemory, **args):
        return cls._compare(function_memory, args)
    
    @classmethod
    def _compare(cls, function_memory:FunctionMemory, branch):
        if isinstance(branch, dict):
            match branch:
                case {
                    "==": list()
                }:
                    ls = branch["=="].copy()
                    ls.append(None) # add a thing so that last 2 items before this get checked
                    x = ls.pop(0)
                    y = ls.pop(0)

                    while ls:
                        ev = cls._compare(function_memory, x)
                        a = None
                        try:
                            a = ev.send(None)
                            while isinstance(a, _EngineOperation):
                                res = yield a
                                a = ev.send(res)
                        except StopIteration as e:
                            a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            b = e.value or (b if not isinstance(b, _EngineOperation) else None)
                        

                        if not (a == b):
                            return False
                        x = y
                        y = ls.pop(0)
                    return True
                
                case {
                    "!=": list()
                }:
                    ls = branch["!="].copy()
                    ls.append(None) # add a thing so that last 2 items before this get checked
                    x = ls.pop(0)
                    y = ls.pop(0)

                    while ls:

                        ev = cls._compare(function_memory, x)
                        a = None
                        try:
                            a = ev.send(None)
                            while isinstance(a, _EngineOperation):
                                res = yield a
                                a = ev.send(res)
                        except StopIteration as e:
                            a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            b = e.value or (b if not isinstance(b, _EngineOperation) else None)
                        

                        if not (a != b):
                            return False
                        x = y
                        y = ls.pop(0)
                    return True
                
                case {
                    "<": list()
                }:
                    ls = branch["<"].copy()
                    ls.append(None) # add a thing so that last 2 items before this get checked
                    x = ls.pop(0)
                    y = ls.pop(0)

                    while ls:

                        ev = cls._compare(function_memory, x)
                        a = None
                        try:
                            a = ev.send(None)
                            while isinstance(a, _EngineOperation):
                                res = yield a
                                a = ev.send(res)
                        except StopIteration as e:
                            a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            b = e.value or (b if not isinstance(b, _EngineOperation) else None)
                        

                        if not (a < b):
                            return False
                        x = y
                        y = ls.pop(0)
                    return True
                
                case {
                    "<=": list()
                }:
                    ls = branch["<="].copy()
                    ls.append(None) # add a thing so that last 2 items before this get checked
                    x = ls.pop(0)
                    y = ls.pop(0)

                    while ls:

                        ev = cls._compare(function_memory, x)
                        a = None
                        try:
                            a = ev.send(None)
                            while isinstance(a, _EngineOperation):
                                res = yield a
                                a = ev.send(res)
                        except StopIteration as e:
                            a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            b = e.value or (b if not isinstance(b, _EngineOperation) else None)
                        

                        if not (a <= b):
                            return False
                        x = y
                        y = ls.pop(0)
                    return True
                case {
                    ">": list()
                }:
                    ls = branch[">"].copy()
                    ls.append(None) # add a thing so that last 2 items before this get checked
                    x = ls.pop(0)
                    y = ls.pop(0)

                    while ls:

                        ev = cls._compare(function_memory, x)
                        a = None
                        try:
                            a = ev.send(None)
                            while isinstance(a, _EngineOperation):
                                res = yield a
                                a = ev.send(res)
                        except StopIteration as e:
                            a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            b = e.value or (b if not isinstance(b, _EngineOperation) else None)
                        

                        if not (a > b):
                            return False
                        x = y
                        y = ls.pop(0)
                    return True
                case {
                    ">=": list()
                }:
                    ls = branch[">="].copy()
                    ls.append(None) # add a thing so that last 2 items before this get checked
                    x = ls.pop(0)
                    y = ls.pop(0)

                    while ls:

                        ev = cls._compare(function_memory, x)
                        a = None
                        try:
                            a = ev.send(None)
                            while isinstance(a, _EngineOperation):
                                res = yield a
                                a = ev.send(res)
                        except StopIteration as e:
                            a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            b = e.value or (b if not isinstance(b, _EngineOperation) else None)
                        

                        if not (a >= b):
                            return False
                        x = y
                        y = ls.pop(0)
                    return True
                case {
                    "and": list()
                }:
                    ls = branch["and"].copy()
                    for l in ls:

                        ev = cls._compare(function_memory, l)
                        a = None
                        try:
                            a = ev.send(None)
                            while isinstance(a, _EngineOperation):
                                res = yield a
                                a = ev.send(res)
                        except StopIteration as e:
                            a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        

                        if not a:
                            return False
                    return True
                case {
                    "or": list()
                }:
                    ls = branch["or"].copy()
                    for l in ls:

                        ev = cls._compare(function_memory, l)
                        a = None
                        try:
                            a = ev.send(None)
                            while isinstance(a, _EngineOperation):
                                res = yield a
                                a = ev.send(res)
                        except StopIteration as e:
                            a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        

                        if a:
                            return True
                    return False
                case {
                    "not": dict()|bool()
                }:

                    ev = cls._compare(function_memory, branch["not"])
                    a = None
                    try:
                        a = ev.send(None)
                        while isinstance(a, _EngineOperation):
                            res = yield a
                            a = ev.send(res)
                    except StopIteration as e:
                        a = e.value or (a if not isinstance(a, _EngineOperation) else None)
                        

                    return not a
                case _:
                    ev = function_memory.generatorEvaluateFunction(branch)
                    v = None
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield v
                            v = ev.send(res)
                    except StopIteration as e:
                        v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                    return v
        else:
            return branch


# ^ Logic ^ #

####XXX#############XXX####
### XXX Engine Math XXX ###
####XXX#############XXX####
class Engine_Math_Solve(LoaderFunction):
    id = Identifier("engine", "math/", "solve")
    return_type = [int, float]
    pre_evaluator = True
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.solve
    
    @classmethod
    def solve(cls, function_memory:FunctionMemory, **args):
        return cls._solve(args)

    @classmethod
    def _solve(cls, branch):
        if isinstance(branch, dict):
            match branch:
                case {
                    "add": list()
                }:
                    return sum([cls._solve(a) for a in branch["add"]])
                
                case {
                    "subtract": list()
                }:
                    return sum([-cls._solve(s) for s in branch["subtract"]], cls._solve(branch["subtract"][0])*2)
                
                case {
                    "multiply": list()
                }:
                    mx = branch["multiply"].copy()
                    m = cls._solve(mx.pop(0))
                    while mx:
                        m *= cls._solve(mx.pop(0))
                    return m
                
                case {
                    "divide": list()
                }:
                    dx = branch["divide"].copy()
                    d = cls._solve(dx.pop(0))
                    while dx:
                        d /= cls._solve(dx.pop(0))
                    return d
                
                case {
                    "max": list()
                }:
                    return max([cls._solve(m) for m in branch["max"]])
                
                case {
                    "min": list()
                }:
                    return min([cls._solve(m) for m in branch["min"]])
                case {
                    "round": dict()|float()|int()
                }:
                    return int(cls._solve(branch["round"]))

        else:
            return branch

# ^ Math ^ #

####XXX####################XXX####
### XXX Engine Interaction XXX ###
####XXX####################XXX####

class Engine_Interaction_Interact(LoaderFunction):
    id = Identifier("engine", "interaction/", "interact")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "interactable": str()
            }: return cls.interact
            case _: return None

    @staticmethod
    def interact(function_memory:FunctionMemory, **kwargs):
        interactable_id = kwargs.get("interactable")
        interactable: Interactable = function_memory.ref(interactable_id)
        player: Player = function_memory.ref("#player")

        return interactable.onInteract(function_memory, player)

# ^ Interaction ^ #

####XXX###############XXX####
### XXX Engine Combat XXX ###
####XXX###############XXX####

class Engine_Combat_Start(LoaderFunction):
    id = Identifier("engine", "combat/", "start")
    pre_evaluate_args = False
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "combat": str()|dict()
            }: return cls.start
            case _: return None
    @staticmethod
    def start(function_memory:FunctionMemory, combat:str|dict):
        if isinstance(combat, str): # reference external combat file
            return EngineOperation.StartCombat(
                AbstractCombat.getCombat(combat),
                function_memory.ref("#player")
            )
        elif isinstance(combat, dict): # inline combat

            identifier = Identifier("engine", "inline_combat/", "")

            abstract: AbstractCombat = AbstractCombat(identifier, combat)
            identifier.name = f"combat_{id(abstract)}"

            return EngineOperation.StartCombat(
                abstract.createInstance(function_memory),
                function_memory.ref("#player")
            )


class Engine_Combat_Trigger(LoaderFunction):
    id = Identifier("engine", "combat/", "trigger")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "trigger": str()|dict()
            }: return cls.trigger
            case _: return None
    @staticmethod
    def trigger(function_memory:FunctionMemory, **kwargs):
        trig_f = kwargs.get("trigger")

        ev = function_memory.generatorEvaluateFunction(trig_f)
        trig = None
        try:
            trig = ev.send(None)
            while isinstance(trig, _EngineOperation):
                res = yield trig
                trig = ev.send(res)
        except StopIteration as e:
            trig = e.value or (trig if not isinstance(trig, _EngineOperation) else None)

        return Combat.Operation.Trigger(trig)

class Engine_Combat_UniqueName(LoaderFunction):
    id = Identifier("engine", "combat/", "unique_name")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.unique_name
            case _: return None
    @staticmethod
    def unique_name(function_memory:FunctionMemory, **kwargs):
        
        return Combat.Operation.UniqueName()

class Engine_Combat_NumberedName(LoaderFunction):
    id = Identifier("engine", "combat/", "numbered_name")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.numbered_name
            case _: return None
    @staticmethod
    def numbered_name(function_memory:FunctionMemory, **kwargs):
        ...

class Engine_Combat_Spawn(LoaderFunction):
    id = Identifier("engine", "combat/", "spawn")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if ("enemy" in args) or ("enemies" in args):
            return cls.spawn
        return None
    @staticmethod
    def spawn(function_memory:FunctionMemory, **kwargs):
        priority = kwargs.get("priority", "last")
        priority = Combat.JoinPriority.RANDOM if priority == "random" else Combat.JoinPriority.NEXT if priority == "next" else Combat.JoinPriority.LAST
        if (enemy := kwargs.get("enemy", None)):
            return Combat.Operation.Spawn([enemy], priority)
        elif (enemies := kwargs.get("enemies", None)):
            return Combat.Operation.Spawn(enemies, priority)

class Engine_Combat_Despawn(LoaderFunction):
    id = Identifier("engine", "combat/", "despawn")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if ("enemy" in args) or ("enemies" in args):
            return cls.despawn
        return None
    @staticmethod
    def despawn(function_memory:FunctionMemory, **kwargs):
        if (enemy := kwargs.get("enemy", None)):
            return Combat.Operation.Despawn([enemy])
        elif (enemies := kwargs.get("enemies", None)):
            return Combat.Operation.Despawn(enemies)
        

class Engine_Combat_Message(LoaderFunction):
    id = Identifier("engine", "combat/", "message")
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.message
            case _: return None
    @staticmethod
    def message(function_memory:FunctionMemory, **kwargs):
        ...


# ^ Combat ^ #






