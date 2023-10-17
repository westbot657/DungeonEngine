# pylint: disable=[W,R,C,import-error]

try:
    from .LoaderFunction import LoaderFunction
    from .Identifier import Identifier
    from .LootTable import LootTable
    from .EngineDummy import Engine
    from .EngineOperation import EngineOperation, _EngineOperation
    from .EngineErrors import LocationError, FunctionError, FunctionCallError
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
    from .AbstractGameObject import AbstractGameObject, GameObject
    from .FunctionMemory import FunctionMemory
    from .Currency import Currency
    from .Player import Player
    from .Logger import Log
    from .Interactable import Interactable
    from .Util import Util
    from .Location import Location
    from .Time import Time
except ImportError:
    from LoaderFunction import LoaderFunction
    from Identifier import Identifier
    from LootTable import LootTable
    from EngineDummy import Engine
    from EngineOperation import EngineOperation, _EngineOperation
    from EngineErrors import LocationError, FunctionError, FunctionCallError
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
    from AbstractGameObject import AbstractGameObject, GameObject
    from FunctionMemory import FunctionMemory
    from Currency import Currency
    from Player import Player
    from Logger import Log
    from Interactable import Interactable
    from Util import Util
    from Location import Location
    from Time import Time

from typing import Any

import random, math, re, json, time

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
engine:text/join
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
### XXX Engine Tool XXX ###
####XXX#############XXX####


class Engine_Tool_CancelUse(LoaderFunction):
    id = Identifier("engine", "tool/", "cancel_use")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.cancel_use
    @staticmethod
    def cancel_use(function_memory:FunctionMemory):
        ... # idk what to do here yet <-- TODO

class Engine_Tool_GetDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "get_durability")
    return_type = int

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "tool": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "tool": str()|dict()
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

    script_flags = {
        "required_args": 1,
        "optional_args": 1,
        "args": {
            "durability": "required parameter",
            "tool": "optional parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "tool": str()|dict(),
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

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Tool_GetName(LoaderFunction):
    id = Identifier("engine", "tool/", "get_name")
    return_type = str


    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Tool_SetName(LoaderFunction):
    id = Identifier("engine", "tool/", "set_name")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }

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
    id = Identifier("engine", "weapon/", "GetDurability")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Weapon_SetDurability(LoaderFunction):
    id = Identifier("engine", "weapon/", "SetDurability")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Weapon_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_max_durability")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Weapon_SetMaxDurability(LoaderFunction):
    id = Identifier("engine", "weapon/", "set_max_durability")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Weapon_GetDamage(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_damage")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Weapon_SetDamage(LoaderFunction):
    id = Identifier("engine", "weapon/", "set_damage")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Weapon_GetAmmoType(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_ammo_type")
    return_type = AbstractAmmo

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Weapon_GetParentType(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_parent_type")
    return_type = AbstractWeapon

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
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

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Armor_SetDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "set_durability")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Armor_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "get_max_durability")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Armor_SetMaxDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "set_max_durability")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Armor_GetDamageReduction(LoaderFunction):
    id = Identifier("engine", "armor/", "get_damage_reduction")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Armor_SetDamageReduction(LoaderFunction):
    id = Identifier("engine", "armor/", "set_damage_reduction")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
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

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Ammo_SetCount(LoaderFunction):
    id = Identifier("engine", "ammo/", "set_count")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Ammo_GetMaxCount(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_max_count")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Ammo_GetParentType(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_parent_type")
    return_type = AbstractAmmo

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Ammo_GetBonusDamage(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_bonus_damage")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
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

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "status_effect": "required parameter",
            "default": "required parameter"
        }
    }
    
    
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

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_StatusEffect_GetDuration(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_duration")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_StatusEffect_SetDuration(LoaderFunction):
    id = Identifier("engine", "status_effect/", "set_duration")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_StatusEffect_GetName(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_name")
    return_type = str

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_StatusEffect_GetCause(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_cause")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
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

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Item_SetCount(LoaderFunction):
    id = Identifier("engine", "item/", "set_count")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Item_GetMaxCount(LoaderFunction):
    id = Identifier("engine", "item/", "get_max_count")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
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

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "message": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "message" in args: return cls.send_message
        return None
    @staticmethod
    def send_message(function_memory:FunctionMemory, message:str):
        function_memory.engine.sendOutput(function_memory.ref("#player"), str(message))

class Engine_Player_SetTag(LoaderFunction):
    id = Identifier("engine", "player/", "set_tag")

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "tag": "required parameter",
            "value": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "tag": str(),
                "value": str()|bool()|int()|float()
            }: return cls.set_tag
            case _: return None
    @staticmethod
    def set_tag(function_memory:FunctionMemory, tag:str, value:int|float|bool|str):
        player: Player = function_memory.ref("#player")
        player.dungeon_data.update({
            tag: value
        })

class Engine_Player_GetTag(LoaderFunction):
    id = Identifier("engine", "player/", "get_tag")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "tag": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "tag": str()
            }: return cls.get_tag
            case _: return None
    @staticmethod
    def get_tag(function_memory:FunctionMemory, tag:str):
        player: Player = function_memory.ref("#player")
        return player.dungeon_data.get(tag, None)

class Engine_Player_InitTag(LoaderFunction):
    id = Identifier("engine", "player/", "init_tag")
    
    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "tag": "required parameter",
            "value": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "tag": str(),
                "value": str()|bool()|int()|float()
            }: return cls.init_tag
            case _: return None
    
    @staticmethod
    def init_tag(function_memory:FunctionMemory, tag:str, value:int|float|bool|str):
        player: Player = function_memory.ref("#player")
        if tag not in player.dungeon_data:
            player.dungeon_data.update({
                tag: value
            })

class Engine_Player_ClearTag(LoaderFunction):
    id = Identifier("engine", "player/", "clear_tag")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "tag": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "tag": str()
            }: return cls.get_tag
            case _: return None
    @staticmethod
    def get_tag(function_memory:FunctionMemory, tag:str):
        player: Player = function_memory.ref("#player")
        if tag in player.dungeon_data:
            player.dungeon_data.pop(tag)

class Engine_Player_GetHealth(LoaderFunction):
    id = Identifier("engine", "player/", "get_health")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_SetHealth(LoaderFunction):
    id = Identifier("engine", "player/", "set_health")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "get_max_health")
    return_type = int

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_SetMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "set_max_health")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_AddMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "add_max_health")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_SubtractMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "subtract_max_health")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_Heal(LoaderFunction):
    id = Identifier("engine", "player/", "heal")
    return_type = int

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "amount": "required parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "amount": int() | dict()
            }: return cls.heal
            case _: return None
    @staticmethod
    def heal(function_memory:FunctionMemory, amount:int|dict):
        player = function_memory.ref("#player")
        player.addHealth(amount)

class Engine_Player_Damage(LoaderFunction):
    id = Identifier("engine", "player/", "damage")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GiveGameObject(LoaderFunction):
    id = Identifier("engine", "player/", "give_game_object")

    script_flags = {
        "required_args": 1,
        "optional_args": 2,
        "args": {
            "object": "required parameter",
            "count": "optional parameter",
            "player": "optional parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "object": str()
            }: return cls.giveObject
            case {
                "object": GameObject()
            }: return cls.giveGameObj
            case _: return None
    @classmethod
    def giveObject(cls, function_memory:FunctionMemory, **kwargs):
        object_name = Identifier.fromString(kwargs.get("object"))
        count = int(kwargs.get("count", 1))
        
        data = kwargs.get("data", {})

        data.update({
                "type": f"engine:abstract/{object_name.path.strip('/').rstrip('s')}",
                "parent": object_name.full()
            })

        game_object = function_memory.engine.loader.constructGameObject(
            function_memory,
            data
        )


        if isinstance(game_object, (Ammo, Item)):
            game_object: Ammo|Item
            game_object.count = min(max(0, count), game_object.max_count)
        
        if "player" in kwargs:
            player: Player = Player.getPlayer(kwargs["player"])
        else:
            player: Player = function_memory.ref("#player")
        player.inventory.addObject(game_object)

        return game_object

    @staticmethod
    def giveGameObj(function_memory:FunctionMemory, **kwargs):
        game_object = kwargs.get("object")
        
        if "player" in kwargs:
            player: Player = Player.getPlayer(kwargs["player"])
        else:
            player: Player = function_memory.ref("#player")
        player.inventory.addObject(game_object)

class Engine_Player_GiveMoney(LoaderFunction):
    id = Identifier("engine", "player/", "give_money")

    script_flags = {
        "required_args": 0,
        "optional_args": 3,
        "args": {
            "gold": "optional parameter",
            "silver": "optional parameter",
            "copper": "optional parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "gold" in args or "silver" in args or "copper" in args:
            return cls.give_money
        return None

    @staticmethod
    def give_money(function_memory:FunctionMemory, gold=0, silver=0, copper=0):
        player: Player = function_memory.ref("#player")
        player.currency = player.currency + Currency(gold, silver, copper)

class Engine_Player_GiveStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "give_status_effect")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_HasStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "has_status_effect")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_RemoveStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "remove_status_effect")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "get_status_effect")

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "status_effect": "required parameter",
            "default": "required parameter"
        }
    }
    
    
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

class Engine_Player_HasGameObject(LoaderFunction):
    id = Identifier("engine", "player/", "has_game_object")
    return_type = bool

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "game_object": "required parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "game_object": str()
            }: return cls.has_item
            case _: return None
    @staticmethod
    def has_item(function_memory:FunctionMemory, game_object:str):
        object_identifier = Identifier.fromString(game_object)
        player = function_memory.ref("#player")

        return player.inventory.containsGameObject(object_identifier)

class Engine_Player_RemoveItem(LoaderFunction):
    id = Identifier("engine", "player/", "remove_item")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetItem(LoaderFunction):
    id = Identifier("engine", "player/", "get_item")
    return_type = Item

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetEquippedArmor(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_armor")
    return_type = Armor

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetEquippedWeapon(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_weapon")
    return_type = Weapon

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetEquippedTool(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_tool")
    return_type = Tool

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetInput(LoaderFunction): # NOTE: this function may (probably will) require special implementation
    id = Identifier("engine", "player/", "get_input")
    return_type = Tool

    script_flags = {
        "required_args": 0,
        "optional_args": 1,
        "args": {
            "prompt": "optional parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.getInput
    
    @classmethod
    def getInput(cls, function_memory:FunctionMemory, **args):
        prompt = args.get("prompt", "")
        x = yield EngineOperation.GetInput(function_memory.ref("#player"), prompt)
        return x[2]

class Engine_Player_SetLocation(LoaderFunction):
    id = Identifier("engine", "player/", "set_location")
    return_type = Tool

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "location": "required parameter"
        }
    }
    
    
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

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.getLocation

    @staticmethod
    def getLocation(function_memory:FunctionMemory):
        return function_memory.ref("#player").location.full()

class Engine_Player_AttackEnemy(LoaderFunction):
    id = Identifier("engine", "player/", "attack_enemy")

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "player": "required parameter",
            "enemy": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "player": Player(),
                "enemy": Enemy()
            }:
                return cls.attack_enemy
            case _: return None
    @staticmethod
    def attack_enemy(function_memory:FunctionMemory, player:Player, enemy:Enemy):
        return player.attackEnemy(function_memory, enemy)

class Engine_Player_CancelAttack(LoaderFunction):
    id = Identifier("engine", "player/", "cancel_attack")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.cancel_attack
            case _: return None
    @staticmethod
    def cancel_attack(function_memory:FunctionMemory, **kwargs):
        return Player.Operation.CancelAttack()

class Engine_Player_ForceHit(LoaderFunction):
    id = Identifier("engine", "player/", "force_hit")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.force_hit
            case _: return None
    @staticmethod
    def force_hit(function_memory:FunctionMemory, **kwargs):
        return Player.Operation.ForceHit()

class Engine_Player_ForceMiss(LoaderFunction):
    id = Identifier("engine", "player/", "force_miss")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.force_miss
            case _: return None
    @staticmethod
    def force_miss(function_memory:FunctionMemory, **kwargs):
        return Player.Operation.ForceMiss()

# ^ Player ^ #

####XXX##############XXX####
### XXX Engine Enemy XXX ###
####XXX##############XXX####


class Engine_Enemy_AttackPlayer(LoaderFunction):
    id = Identifier("engine", "enemy/", "attack_player")
    pre_evaluator = True

    script_flags = {
        "required_args": 0,
        "optional_args": 2,
        "args": {
            "enemy": "optional parameter",
            "player": "optional parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.attack_player
    @staticmethod
    def attack_player(function_memory:FunctionMemory, **kwargs):
        if "enemy" in kwargs: enemy = kwargs.get("enemy")
        else: enemy = function_memory.ref("#enemy")
        
        if "player" in kwargs: player = kwargs.get("player")
        else: player = function_memory.ref("#player")
        return enemy.attackPlayer(function_memory, player)

class Engine_Enemy_CancelAttack(LoaderFunction):
    id = Identifier("engine", "enemy/", "cancel_attack")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.cancel_attack
    @staticmethod
    def cancel_attack(function_memory:FunctionMemory, **kwargs):
        return Enemy.Operation.CancelAttack()

class Engine_Enemy_SetAttack(LoaderFunction):
    id = Identifier("engine", "enemy/", "set_attack")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "attack": "required parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "attack": Attack()|str()
            }: return cls.set_attack
            case _: return None
    @staticmethod
    def set_attack(function_memory:FunctionMemory, attack:Attack|str):
        return Enemy.Operation.ChooseAttack(attack)

class Engine_Enemy_ForceHit(LoaderFunction):
    id = Identifier("engine", "enemy/", "force_hit")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.force_hit
            case _: return None
    @staticmethod
    def force_hit(function_memory:FunctionMemory, **kwargs):
        return Enemy.Operation.ForceHit()

class Engine_Enemy_ForceMiss(LoaderFunction):
    id = Identifier("engine", "enemy/", "force_miss")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.force_miss
            case _: return None
    @staticmethod
    def force_miss(function_memory:FunctionMemory, **kwargs):
        return Enemy.Operation.ForceMiss()

class Engine_Enemy_SetHealth(LoaderFunction):
    id = Identifier("engine", "enemy/", "set_health")

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "enemy": "required parameter",
            "health": "required parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "enemy": Enemy(),
                "health": int()
            }: return cls.set_health
            case _: return None
    @staticmethod
    def set_health(function_memory:FunctionMemory, enemy:Enemy, health:int):
        ...

class Engine_Enemy_Heal(LoaderFunction):
    id = Identifier("engine", "enemy/", "heal")

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "enemy": "required parameter",
            "amount": "required parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "enemy": Enemy(),
                "amount": int()
            }: return cls.heal
            case _: return None
    @staticmethod
    def heal(function_memory:FunctionMemory, enemy:Enemy, amount:int):
        ...

class Engine_Enemy_Damage(LoaderFunction):
    id = Identifier("engine", "enemy/", "damage")
    pre_evaluator = True

    script_flags = {
        "required_args": 1,
        "optional_args": 1,
        "args": {
            "amount": "required parameter",
            "enemy": "optional parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "amount" in args:
            return cls.damage
        return None
    @staticmethod
    def damage(function_memory:FunctionMemory, **kwargs):
        amount = kwargs.get("amount")
        enemy = kwargs.get("enemy", function_memory.ref("#enemy"))
        enemy.damage(function_memory, amount)

class Engine_Enemy_SetMaxHealth(LoaderFunction):
    id = Identifier("engine", "enemy/", "set_max_health")

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "enemy": "required parameter",
            "max_health": "required parameter"
        }
    }
    
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "enemy": Enemy(),
                "max_health": int()
            }: return cls.set_max_health
            case _: return None
    @staticmethod
    def set_max_health(function_memory:FunctionMemory, enemy:Enemy, max_health:int):
        ...

# ^ Enemy ^ #

####XXX#################XXX####
### XXX Engine Location XXX ###
####XXX#################XXX####


class Engine_Location_Exists(LoaderFunction):
    id = Identifier("engine", "location/", "exists")
    return_type = bool

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "location": "required parameter"
        }
    }
    
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


# class Engine_Random_Uniform(LoaderFunction):
#     id = Identifier("engine", "random/", "uniform")
#     pre_evaluate_args = False

#     script_flags = {
#         "required_args": 2,
#         "optional_args": 0,
#         "args": {
#             "rolls": "required parameter",
#             "pool": "required parameter"
#         }
#     }
    
#     @classmethod
#     def check(cls, function_memory:FunctionMemory, args:dict):
#         match args:
#             case {
#                 "rolls": int(),
#                 "pool": list()
#             }: return cls.uniform_list
#             case _: return None
#     @staticmethod
#     def uniform_list(function_memory:FunctionMemory, rolls:int, pool:list, roll_size:int=1):
#         if roll_size > len(pool): raise FunctionError(f"Cannot pull more elements from list than are available")
#         result = []
#         for roll in range(rolls):
#             _pool = pool.copy()
#             for r in range(roll_size):
#                 p = random.choice(_pool)
#                 _pool.remove(p)
#                 result.append(p)
#         return result


class Engine_Random_Range(LoaderFunction):
    id = Identifier("engine", "random/", "range")

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "min": "required parameter",
            "max": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "min": int(),
                "max": int()
            }: return cls.rand_range
            case _: return None
    @staticmethod
    def rand_range(function_memory:FunctionMemory, min:int, max:int):
        return random.randint(min, max)

    @classmethod
    def getFullDisplay(self, function_memory:FunctionMemory, data: dict) -> str:
        return f"[{data['min']}-{data['max']}]"

    @classmethod
    def getQuickDisplay(self, function_memory:FunctionMemory, data: dict) -> str:
        return f"[{data['min']}-{data['max']}]"

class Engine_Random_Weighted(LoaderFunction):
    id = Identifier("engine", "random/", "weighted")
    pre_evaluate_args = False

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "weights": "required parameter",
            "values": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        print(f"random-weighted: {args}")
        match args:
            case {
                "weights": list(),
                "values": list()
            }: return cls.random_weighted
            case _: return None
    @staticmethod
    def random_weighted(function_memory:FunctionMemory, weights:list, values:list):
        
        # print(weights, values)
        pool = []

        for weight, val in zip(weights, values):
            for i in range(int(weight)):
                pool.append(int(val))
        
        # print(pool)
        return random.choice(pool)

    @classmethod
    def getFullDisplay(self, function_memory:FunctionMemory, data:dict) -> str:

        # print(data)

        weights = json.loads(data["weights"].replace("'", ""))
        values = json.loads(data["values"].replace("'", ""))
        out = []
        total = sum(weights)
        for weight, val in zip(weights, values):
            out.append(f"{f'{weight/total*100:.2f}'.rstrip('0').strip('.').lstrip('0')}%" + f":{val}")
        return f"[{' '.join(out)}]"

    @classmethod
    def getQuickDisplay(self, function_memory:FunctionMemory, data:dict) -> str:

        # print(data)

        weights = json.loads(data["weights"].replace("'", ""))
        values = json.loads(data["values"].replace("'", ""))

        low = min(values)
        high = max(values)
        return f"[{low}..{high}]"

class Engine_Random_LootTable(LoaderFunction):
    id = Identifier("engine", "random/", "loot_table")
    pre_evaluate_args = False

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            # "rolls": "required parameter",
            "pools": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                # "rolls": int(),
                "pools": list()
            }: return cls.loot_table
            case _: return None
    @staticmethod
    def loot_table(function_memory:FunctionMemory, pools:list[dict]):
        table = LootTable.fromDict({"pools": pools})
        return table.roll(function_memory)

class Engine_Random_Choice(LoaderFunction):
    id = Identifier("engine", "random/", "choice")
    pre_evaluate_args = False

    script_flags = {
        "required_args": 1,
        "optional_args": 1,
        "args": {
            "options": "required parameter",
            "evaluate_choice": "optional parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "options": list()
            }: return cls.choice
            case _: return None
    @staticmethod
    def choice(function_memory:FunctionMemory, options:list, evaluate_choice=True):
        ret = random.choice(options)
        
        if evaluate_choice:
            return function_memory.generatorEvaluateFunction(ret)
        return function_memory.evaluateFunction(ret)

# ^ Random ^ #

####XXX#############XXX####
### XXX Engine Text XXX ###
####XXX#############XXX####


class Engine_Text_Join(LoaderFunction):
    id = Identifier("engine", "text/", "join")
    return_type = str
    pre_evaluator = True

    script_flags = {
        "required_args": 1,
        "optional_args": 1,
        "args": {
            "text": "*parameters",
            "seperator": "optional parameter"
        }
    }
    
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

    script_flags = {
        "required_args": 2,
        "optional_args": -1,
        "args": {
            "text": "required parameter",
            "match_type": "optional parameter",
            "matches": "tags"
        },
        "tags": {
            "tag": "pattern",
            "scope": "functions"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "text" in args:
            return cls.pattern_match
        return None
    @staticmethod
    def pattern_match(function_memory:FunctionMemory, **kwargs):
        text = kwargs.pop("text")

        if "match_type" in kwargs:
            match_type = kwargs.pop("match_type")
        else:
            match_type = "match"

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
            
            match match_type:
                case "search": f = re.search
                case "findall": f = re.findall
                case "fullmatch": f = re.fullmatch
                case _: f = re.match

            if m := f(pattern, text):
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

    script_flags = {
        "required_args": 3,
        "optional_args": 0,
        "args": {
            "sequence": "required parameter",
            "replacement": "required parameter",
            "text": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "sequence": str(),
                "text": str(),
                "replacement": str()
            }: return cls.replace
            case _: return None

    @staticmethod
    def replace(function_memory:FunctionMemory, text:str, sequence:str, replacement:str):
        return text.replace(sequence, replacement)

class Engine_Text_ReplacePattern(LoaderFunction):
    id = Identifier("engine", "text/", "replace_pattern")


    script_flags = {
        "required_args": 3,
        "optional_args": 0,
        "args": {
            "pattern": "required parameter",
            "replacement": "required parameter",
            "text": "required parameter"
        }
    }

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

class Engine_Text_Format(LoaderFunction):
    id = Identifier("engine", "text/", "format")

    script_flags = {
        "required_args": 1,
        "optional_args": -1,
        "args": {
            "text": "required parameter",
            "options": "**parameters"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:list):
        if "text" in args:
            return cls.format
        else: return None
    @staticmethod
    def format(function_memory:FunctionMemory, text:str, options:dict):
        # print(options)
        # print(f"formatting text {text!r} with options:{options}")
        opts = {}
        for key, val in options.items():
            opts.update({key: str(val)})
        return text.format(**opts)

class Engine_Text_Substring(LoaderFunction):
    id = Identifier("engine", "text/", "substring")

    script_flags = {
        "required_args": 2,
        "optional_args": 1,
        "args": {
            "text": "required parameter",
            "start": "optional parameter",
            "end": "optional parameter"
        }
    }
    
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

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "text": "required parameter"
        }
    }
    
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

class Engine_Text_Convert(LoaderFunction):
    id = Identifier("engine", "text/", "convert")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "text": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "text" in args: return cls.to_str
    @staticmethod
    def to_str(function_memory:FunctionMemory, text:str):
        return str(text)


class Engine_Text_SetCase(LoaderFunction):
    id = Identifier("engine", "text/", "set_case")

    script_flags = {
        "required_args": 2,
        "optional_args": 2,
        "args": {
            "text": "required parameter",
            "case": "required parameter"
        }
    }

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

    script_flags = {
        "required_args": 1,
        "optional_args": 2,
        "args": {
            "dict": "required parameter",
            "key_name": "optional parameter",
            "value_name": "optional parameter",
            "run": "scope"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "dict": dict(),
                "run": dict()|list()
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
        
        key_name = args.get("key_name", "key")
        value_name = args.get("value_name", "value")

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
                key_name: key,
                value_name: element
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

class Engine_Dict_Access(LoaderFunction):
    id = Identifier("engine", "dict/", "access")
    # pre_evaluate_args = True

    script_flags = {
        "required_args": 2,
        "optional_args": -1,
        "args": {
            "dict": "required parameter",
            "keys": "*parameters"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "dict" in args and "keys" in args:
            return cls.access
        return None

    @staticmethod
    def access(function_memory:FunctionMemory, **kwargs):
        dct: dict = kwargs["dict"]
        path: list[str] = kwargs["keys"]

        p = dct
        while path:
            try:
                p = p[path.pop(0)]
            except KeyError:
                return None
            except Exception:
                return None # maybe raise an actual error here...
        return p
            

# ^ Dict ^ #

####XXX#############XXX####
### XXX Engine List XXX ###
####XXX#############XXX####


class Engine_List_ForEach(LoaderFunction):
    id = Identifier("engine", "list/", "for_each")
    pre_evaluate_args = False

    script_flags = {
        "required_args": 1,
        "optional_args": 1,
        "args": {
            "list": "required parameter",
            "element_name": "optional parameter",
            "run": "scope"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "list": list()|dict(),
                "run": list()|dict()
            }:
                return cls.for_each
            case _: return None

    @staticmethod
    def for_each(function_memory:FunctionMemory, **args):

        lst: list|dict = args.get("list")

        if isinstance(lst, dict):
            lst = function_memory.evaluateFunction(lst)

        element_name = args.get("element_name", "element")

        func: dict|list = args.get("run")
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
                element_name: element
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

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case _: return None
    @staticmethod
    def _(function_memory:FunctionMemory, ):
        return
    
class Engine_List_Pop(LoaderFunction):
    id = Identifier("engine", "list/", "pop")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case _: return None
    @staticmethod
    def _(function_memory:FunctionMemory, ):
        return
    
class Engine_List_Append(LoaderFunction):
    id = Identifier("engine", "list/", "append")

    script_flags = {
        "required_args": 2,
        "optional_args": -1,
        "args": {
            "list": "required parameter",
            "elements": "*paramaters"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if ("list" in args) and ("elements" in args):
            return cls.append
    @staticmethod
    def append(function_memory:FunctionMemory, **kwargs):
        ls: list = kwargs.get("list")
        elements = kwargs.get("elements")

        for element in elements:
            ls.append(element)

class Engine_List_Contains(LoaderFunction):
    id = Identifier("engine", "list/", "contains")

    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "list": "required parameter",
            "element": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if ("list" in args) and ("element" in args):
            return cls.contains
        return None

    @staticmethod
    def contains(function_memory:FunctionMemory, **kwargs):
        ls: list = kwargs.get("list")
        element = kwargs.get("element")
        return (element in ls)

class Engine_List_Length(LoaderFunction):
    id = Identifier("engine", "list/", "length")
    pre_evaluate_args = True

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "list": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "list" in args: return cls.length
        return None
    
    @staticmethod
    def length(function_memory:FunctionMemory, **kwargs):
        lst = kwargs["list"]
        return len(lst)

class Engine_List_Remove(LoaderFunction):
    id = Identifier("engine", "list/", "remove")
    
    script_flags = {
        "required_args": 2,
        "optional_args": 0,
        "args": {
            "list": "required parameter",
            "value": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "list" in args and "value" in args:
            return cls.remove
        return None
    
    @staticmethod
    def remove(function_memory:FunctionMemory, **kwargs):
        ls = kwargs.get("list")
        val = kwargs.get("value")
        if val in ls:
            ls.remove(val)
    

# ^ List ^ #

####XXX################XXX####
### XXX Engine Control XXX ###
####XXX################XXX####

class Engine_Control_While(LoaderFunction):
    id = Identifier("engine", "control/", "while")
    pre_evaluate_args = False

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "condition": "required parameter",
            "run": "scope"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "condition": list()|dict()|bool()|str()|int()|float(),
                "run": list()|dict()
            }:
                return cls._while
            case _: return None

    @staticmethod
    def _while(function_memory:FunctionMemory, **args):

        condition = args.get("condition")
        func: dict|list = args.get("run")
        while True:

            ev = function_memory.generatorEvaluateFunction(condition)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value if e.value is not None else (v if not isinstance(v, _EngineOperation) else None)
            element = v

            if not element:
                return

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

class Engine_Control_Break(LoaderFunction):
    id = Identifier("engine", "control/", "break")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls._break
    @staticmethod
    def _break(function_memory:FunctionMemory):
        return EngineOperation.StopLoop()

class Engine_Control_CheckPredicate(LoaderFunction):
    id = Identifier("engine", "control/", "check_predicate")
    pre_evaluate_args = False

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "predicate": "required parameter",
            "functions": "scope"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "predicate": dict(),
                "functions": dict()|list()
            }: return cls.check_predicate
            case _: return None
    @staticmethod
    def check_predicate(function_memory:FunctionMemory, predicate:dict, functions:dict|list):
        if function_memory.checkPredicate(predicate):
            ev = function_memory.generatorEvaluateFunction(functions)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = function_memory.engine.loader.stopIterationEval(e.value, v)
            return v

class Engine_Control_RaiseError(LoaderFunction):
    id = Identifier("engine", "control/", "raise_error")
    
    script_flags = {
        "required_args": 0,
        "optional_args": -1,
        "args": {
            "details": "*parameters"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "details": list()
            }: return cls.raise_error
            case _: return None

    @staticmethod
    def raise_error(function_memory:FunctionMemory, *details):
        raise FunctionCallError(*details)

class Engine_Control_Call(LoaderFunction):
    id = Identifier("engine", "control/", "call")
    pre_evaluate_args = False

    script_flags = {
        "required_args": 1,
        "optional_args": -1,
        "args": {
            "method": "required parameter",
            "parameters": "**parameters"
        }
    }
    
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
            v = function_memory.engine.loader.stopIterationEval(e.value, v)
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
                            if e.value is not None:
                                a = e.value
                            else:
                                a = a if not isinstance(a, _EngineOperation) else None
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            if e.value is not None:
                                b = e.value
                            else:
                                b = b if not isinstance(b, _EngineOperation) else None
                        

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
                            if e.value is not None:
                                a = e.value
                            else:
                                a = a if not isinstance(a, _EngineOperation) else None
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            if e.value is not None:
                                b = e.value
                            else:
                                b = b if not isinstance(b, _EngineOperation) else None
                        

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
                            if e.value is not None:
                                a = e.value
                            else:
                                a = a if not isinstance(a, _EngineOperation) else None
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            if e.value is not None:
                                b = e.value
                            else:
                                b = b if not isinstance(b, _EngineOperation) else None
                        

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
                            if e.value is not None:
                                a = e.value
                            else:
                                a = a if not isinstance(a, _EngineOperation) else None
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            if e.value is not None:
                                b = e.value
                            else:
                                b = b if not isinstance(b, _EngineOperation) else None
                            # b = e.value or (b if not isinstance(b, _EngineOperation) else None)
                        

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
                            if e.value is not None:
                                a = e.value
                            else:
                                a = a if not isinstance(a, _EngineOperation) else None
                        
                        ev = cls._compare(function_memory, y)
                        b = None
                        try:
                            b = ev.send(None)
                            while isinstance(b, _EngineOperation):
                                res = yield b
                                b = ev.send(res)
                        except StopIteration as e:
                            if e.value is not None:
                                b = e.value
                            else:
                                b = b if not isinstance(b, _EngineOperation) else None
                        

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
                            if e.value is not None:
                                a = e.value
                            else:
                                a = a if not isinstance(a, _EngineOperation) else None
                        

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
                            if e.value is not None:
                                a = e.value
                            else:
                                a = a if not isinstance(a, _EngineOperation) else None
                        

                        if a:
                            return True
                    return False
                case {
                    "not": dict()|bool()|int()|str()
                }:

                    ev = cls._compare(function_memory, branch["not"])
                    a = None
                    try:
                        a = ev.send(None)
                        while isinstance(a, _EngineOperation):
                            res = yield a
                            a = ev.send(res)
                    except StopIteration as e:
                        if e.value is not None:
                            a = e.value
                        else:
                            a = a if not isinstance(a, _EngineOperation) else None

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
                        if e.value is not None:
                            v = e.value
                        else:
                            v = v if not isinstance(v, _EngineOperation) else None
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
                    "pow": list()
                }:
                    mx = branch["pow"].copy()
                    m = cls._solve(mx.pop(0))
                    while mx:
                        m **= cls._solve(mx.pop(0))
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
                    "mod": list()
                }:
                    dx = branch["mod"].copy()
                    d = cls._solve(dx.pop(0))
                    while dx:
                        d %= cls._solve(dx.pop(0))
                    return d
                
                case {
                    "binand": list()
                }:
                    dx = branch["binand"].copy()
                    d = cls._solve(dx.pop(0))
                    while dx:
                        d &= cls._solve(dx.pop(0))
                    return d
                case {
                    "binor": list()
                }:
                    dx = branch["binor"].copy()
                    d = cls._solve(dx.pop(0))
                    while dx:
                        d |= cls._solve(dx.pop(0))
                    return d
                case {
                    "binxor": list()
                }:
                    dx = branch["binxor"].copy()
                    d = cls._solve(dx.pop(0))
                    while dx:
                        d ^= cls._solve(dx.pop(0))
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

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "interactable": "required parameter"
        }
    }
    
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


class Engine_Interaction_GetShopStock(LoaderFunction):
    id = Identifier("engine", "interaction/", "get_shop_stock")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "loot_table": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "loot_table" in args: return cls.get_stock
        return None
    
    @staticmethod
    def get_stock(function_memory:FunctionMemory, loot_table:dict):
        ls = Util.flatten_list(LootTable.fromDict(loot_table).roll(function_memory))
        out = []

        print(f"Shop stock: {ls}")

        for l in ls:
            item = function_memory.engine.loader.constructGameObject(function_memory, l["item"])
            out.append({
                "name": item.name,
                "item": item,
                "amount": f"x{item.count}" if hasattr(item, "count") else "",
                "cost": Currency(*l["cost"])
            })
        return out


# ^ Interaction ^ #

####XXX###############XXX####
### XXX Engine Combat XXX ###
####XXX###############XXX####


class Engine_Combat_Start(LoaderFunction):
    id = Identifier("engine", "combat/", "start")
    # pre_evaluate_args = False

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "combat": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "combat": str()
            }: return cls.start
            case _: return None
    @staticmethod
    def start(function_memory:FunctionMemory, combat:str|dict):
        if isinstance(combat, str): # reference external combat file
            yield EngineOperation.StartCombat(
                AbstractCombat.getCombat(function_memory, combat),
                function_memory.ref("#player")
            )

class Engine_Combat_Get(LoaderFunction):
    id = Identifier("engine", "combat/", "get")
    pre_evaluate_args = False

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "combat": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "combat": str()|dict()
            }: return cls.get
            case _: return None
    @staticmethod
    def get(function_memory:FunctionMemory, combat:str|dict):
        if isinstance(combat, str): # reference external combat file
            yield EngineOperation.StartCombat(
                AbstractCombat.getCombat(function_memory, combat),
                function_memory.ref("#player")
            )



class Engine_Combat_Trigger(LoaderFunction):
    id = Identifier("engine", "combat/", "trigger")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "trigger": "required parameter"
        }
    }
    
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
        combat: Combat = function_memory.ref("#combat")
        ev = function_memory.generatorEvaluateFunction(trig_f)
        trig = None
        try:
            trig = ev.send(None)
            while isinstance(trig, _EngineOperation):
                res = yield trig
                trig = ev.send(res)
        except StopIteration as e:
            trig = e.value or (trig if not isinstance(trig, _EngineOperation) else None)

        combat.addTask(Combat.Operation.Trigger(trig))

class Engine_Combat_UniqueName(LoaderFunction):
    id = Identifier("engine", "combat/", "unique_name")
    
    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
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

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.numbered_name
            case _: return None
    @staticmethod
    def numbered_name(function_memory:FunctionMemory, **kwargs):
        return Combat.Operation.NumberedName()

class Engine_Combat_NextTurn(LoaderFunction):
    id = Identifier("engine", "combat/", "next_turn")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.next_turn
    @staticmethod
    def next_turn(function_memory:FunctionMemory):
        combat: Combat = function_memory.ref("#combat")
        combat.addTask(Combat.Operation._NextTurn())

class Engine_Combat_Spawn(LoaderFunction):
    id = Identifier("engine", "combat/", "spawn")

    script_flags = {
        "required_args": 1,
        "optional_args": -1,
        "args": {
            "enemies": "*parameters",
            "prioity": "optional parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if ("enemy" in args) or ("enemies" in args):
            return cls.spawn
        return None
    @staticmethod
    def spawn(function_memory:FunctionMemory, **kwargs):
        priority = kwargs.get("priority", "last")
        priority = Combat.JoinPriority.RANDOM if priority == "random" else Combat.JoinPriority.NEXT if priority == "next" else Combat.JoinPriority.LAST
        combat: Combat = function_memory.ref("#combat")
        if (enemy := kwargs.get("enemy", None)):
            combat.addTask(Combat.Operation.Spawn([enemy], priority))
        if (enemies := kwargs.get("enemies", None)):
            combat.addTask(Combat.Operation.Spawn(enemies, priority))

class Engine_Combat_Despawn(LoaderFunction):
    id = Identifier("engine", "combat/", "despawn")

    script_flags = {
        "required_args": 1,
        "optional_args": -1,
        "args": {
            "enemies": "*parameters"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if ("enemy" in args) or ("enemies" in args):
            return cls.despawn
        return None
    @staticmethod
    def despawn(function_memory:FunctionMemory, **kwargs):
        combat: Combat = function_memory.ref("#combat")
        if (enemy := kwargs.get("enemy", None)):
            combat.addTask(Combat.Operation.Despawn([enemy]))
        elif (enemies := kwargs.get("enemies", None)):
            combat.addTask(Combat.Operation.Despawn(enemies))

class Engine_Combat_KillEnemy(LoaderFunction):
    id = Identifier("engine", "combat/", "kill_enemy")

    script_flags = {
        "required_args": 1,
        "optional_args": -1,
        "args": {
            "enemies": "*parameters"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if ("enemy" in args) or ("enemies" in args):
            return cls.despawn
        return None
    @staticmethod
    def despawn(function_memory:FunctionMemory, **kwargs):
        combat: Combat = function_memory.ref("#combat")
        if (enemy := kwargs.get("enemy", None)):
            combat.addTask(Combat.Operation.Despawn([enemy]), 0)
        elif (enemies := kwargs.get("enemies", None)):
            combat.addTask(Combat.Operation.Despawn(enemies), 0)

class Engine_Combat_Message(LoaderFunction):
    id = Identifier("engine", "combat/", "message")

    script_flags = {
        "required_args": 1,
        "optional_args": -1,
        "args": {
            "message": "required parameter",
            "players": "*parameters",
            "global_message": "optional parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {}: return cls.message
            case _: return None
    @staticmethod
    def message(function_memory:FunctionMemory, **kwargs):
        if "players" in kwargs: players = kwargs.get("players")
        elif "player" in kwargs: players = (kwargs.get("player"),)
        else: players = tuple()
        
        combat: Combat = function_memory.ref("#combat")
        combat.addTask(Combat.Operation.Message(kwargs.get("message"), *players, global_message=kwargs.get("global_message", False)))

class Engine_Combat_KillPlayer(LoaderFunction):
    id = Identifier("engine", "combat/", "kill_player")
    
    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "player": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "player": str()|Player()
            }: return cls.kill_player
            case _: return None
    
    @staticmethod
    def kill_player(function_memory:FunctionMemory, player:str|Player):
        ...
    
class Engine_Combat_RemovePlayer(LoaderFunction):
    id = Identifier("engine", "combat/", "remove_player")
    
    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "player": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "player": str()|Player()
            }: return cls.remove_player
            case _: return None
    
    @staticmethod
    def remove_player(function_memory:FunctionMemory, player:str|Player):
        ...
    

# ^ Combat ^ #

####XXX#################XXX####
### XXX Engine Variable XXX ###
####XXX#################XXX####


class Engine_Variable_IsDefined(LoaderFunction):
    id = Identifier("engine", "variable/", "is_defined")
    
    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "var_name": "required parameter"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "var_name": str()
            }: return cls.defined
            case _: return None
    @staticmethod
    def defined(function_memory:FunctionMemory, var_name:str):
        try:
            function_memory.ref(var_name)
            return True
        except MemoryError:
            return False

# ^ Variable ^ #

####XXX##############XXX####
### XXX Engine Debug XXX ###
####XXX##############XXX####


class Engine_Log_Debug(LoaderFunction):
    id = Identifier("engine", "log/", "debug")

    script_flags = {
        "required_args": 1,
        "optional_args": -1,
        "args": {
            "message": "required parameter",
            "tags": "*parameters"
        }
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.debug
    @staticmethod
    def debug(function_memory:FunctionMemory, **kwargs):
        Log["debug"]
        if tags := kwargs.get("tags", None):
            for tag in tags:
                Log[tag]
        Log(kwargs.get("message", "<no message>"))

class Engine_Debug_Breakpoint(LoaderFunction):
    id = Identifier("engine", "debug/", "breakpoint")

    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.debug
    @staticmethod
    def debug(function_memory:FunctionMemory):
        breakpoint()

class Engine_Debug_Memory(LoaderFunction):
    id = Identifier("engine", "debug/", "memory")
    
    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.memory

    @staticmethod
    def memory(function_memory:FunctionMemory):
        Log["debug"]["memory"](json.dumps(function_memory.getMemory(), indent=4, default=str))

# ^ Debug ^ #

####XXX#############XXX####
### XXX Engine Time XXX ###
####XXX#############XXX####


class Engine_Time_Get(LoaderFunction):
    id = Identifier("engine", "time/", "get")
    
    script_flags = {
        "required_args": 0,
        "optional_args": 0,
        "args": {}
    }
    
    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        return cls.get
    @staticmethod
    def get(function_memory:FunctionMemory):
        return Time(time.time())

class Engine_Time_Wait(LoaderFunction):
    id = Identifier("engine", "time/", "wait")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "delay": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "delay": float()|int()
            }: return cls.wait
            case _: return None
    @staticmethod
    def wait(function_memory:FunctionMemory, delay):
        # prompt = args.get("prompt", "")
        # x = yield EngineOperation.GetInput(function_memory.ref("#player"), prompt)
        # return x
        # print("waiting?")
        yield EngineOperation.Wait(delay)
        # print("waited")
        # return

class Engine_Time_Check(LoaderFunction):
    id = Identifier("engine", "time/", "check")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "time_frame": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        if "time_frame" in args: return cls.time_check
        return None

    @staticmethod
    def time_check(function_memory:FunctionMemory, time_frame:str):
        h, m = time.asctime()[11:16].split(":")
        h = int(h)
        m = int(m)
        # x = "am" if h < 12 else "pm"
        rules = time_frame.split(";")
        for rule in rules:
            if match := re.match(r"(?P<h1>\d+):(?P<m1>\d+)(?P<x1>am|pm)\-(?P<h2>\d+):(?P<m2>\d+)(?P<x2>am|pm)", rule):
                d = match.groupdict()
                h1 = int(d["h1"])
                m1 = int(d["m1"])
                x1 = d["x1"]
                if x1 == "am" and h1 == 12: h1 = 0
                elif x1 == "pm" and h1 != 12: h1 += 12
                h2 = int(d["h2"])
                m2 = int(d["m2"])
                x2 = d["x2"]
                if x2 == "am" and h2 == 12: h2 = 0
                elif x2 == "pm" and h2 != 12: h2 += 12
                if h1 <= h2:
                    if (h1 <= h and m1 <= m) and (h <= h2 and m <= m2):
                        return True
                else:
                    if (h2 <= h and m2 <= m) and (h <= h1 and m <= m1): # this may be wrong...
                        return True

            elif match := re.match(r"(?P<h1>\d+):(?P<m1>\d+)(?P<x1>am|pm)~(?P<h2>\d+):(?P<m2>\d+)", rule):
                d = match.groupdict()
                h1 = int(d["h1"])
                m1 = int(d["m1"])
                x1 = d["x1"]
                if x1 == "am" and h1 == 12: h1 = 0
                elif x1 == "pm" and h1 != 12: h1 += 12
                h2 = int(d["h2"])
                m2 = int(d["m2"])
                if (Util.wrapNumber(0, h1-h2, 23) <= h and m1-m2 <= h) and (h <= Util.wrapNumber(0, h1+h2, 23) and m <= m1+m2):
                    return True
                
            elif match := re.match(r"~(?P<h1>\d+):(?P<m1>\d+)", rule):
                d = match.groupdict()
                h1 = int(d["h1"])
                m1 = int(d["m1"])
                x1 = d["x1"]
                if x1 == "am" and h1 == 12: h1 = 0
                elif x1 == "pm" and h1 != 12: h1 += 12
                h2 = 0
                m2 = 5
                if (Util.wrapNumber(0, h1-h2, 23) <= h and m1-m2 <= h) and (h <= Util.wrapNumber(0, h1+h2, 23) and m <= m1+m2):
                    return True
            elif match := re.match(r"(?P<h>\d+):(?P<m>\d+)", rule):
                d = match.groupdict()
                if h == int(d["h"]) and m == int(d["m"]):
                    return True
        return False

        # time_frame format: "2:00pm~0:02;3:00pm-3:15pm;6:17pm"

# ^ Time ^ #

####XXX##############XXX####
### XXX Engine Sound XXX ###
####XXX##############XXX####


class Engine_Sound_Play(LoaderFunction):
    id = Identifier("engine", "sound/", "play")

    script_flags = {
        "required_args": 1,
        "optional_args": 0,
        "args": {
            "sound": "required parameter"
        }
    }

    @classmethod
    def check(cls, function_memory:FunctionMemory, args:dict):
        match args:
            case {
                "sound": str()
            }: return cls.send_message
            case _: return None
    @staticmethod
    def send_message(function_memory:FunctionMemory, sound:str):
        function_memory.engine.sendOutput(1, sound)

# ^ Sound ^ #


