# pylint: disable=[W,R,C,import-error]

try:
    from .LoaderFunction import LoaderFunction
    from .Identifier import Identifier
    from .LootTable import LootTable
    from .EngineDummy import Engine

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

except ImportError:
    from LoaderFunction import LoaderFunction
    from Identifier import Identifier
    from LootTable import LootTable
    from EngineDummy import Engine

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

import random, math, re

"""
functions:
engine:tool/cancel_use
engine:tool/get_durability
engine:tool/set_durability
engine:tool/set_max_durability
engine:tool/get_max_durability

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

engine:status_effect/get_level
engine:status_effect/set_level
engine:status_effect/get_duration
engine:status_effect/set_duration

engine:weapon/get_durability
engine:weapon/set_durability
engine:weapon/get_max_durability
engine:weapon/set_max_durability
engine:weapon/get_damage
engine:weapon/set_damage
engine:weapon/get_parent_type
engine:weapon/get_ammo_type

engine:item/get_count
engine:item/set_count
engine:item/get_max_count

engine:armor/get_durability
engine:armor/set_durability
engine:armor/get_damage_reduction
engine:armor/set_damage_reduction
engine:armor/get_max_durability
engine:armor/set_max_durability

engine:ammo/get_count
engine:ammo/set_count
engine:ammo/get_max_count
engine:ammo/get_parent_type
engine:ammo/get_bonus_damage


engine:text/builder


engine:random/uniform X
engine:random/weighted

engine:logic/compare

engine:math/solve


"""

####XXX#############XXX####
### XXX Engine Tool XXX####
####XXX#############XXX####

class Engine_Tool_CancelUse(LoaderFunction):
    id = Identifier("engine", "tool/", "cancel_use")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        return cls.cancel_use
    @staticmethod
    def cancel_use(engine:Engine):
        ... # idk what to do here yet <-- TODO

class Engine_Tool_GetDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "get_durability")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {
                "tool": str()|dict() # FIXME: this may be incorrect syntax, I can't tell right now
            }: return cls.get_durability_given
            case _:
                if engine.function_context.tool:
                    return cls.get_durability_ctx
                return None
    @staticmethod
    def get_durability_given(engine:Engine, tool):
        ...
    @staticmethod
    def get_durability_ctx(engine:Engine):
        ...

class Engine_Tool_SetDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "set_durability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {
                "tool": str()|dict(), # FIXME: this may be incorrect syntax, I can't tell right now
                "durability": int()
            }: return cls.get_durability_given
            case {
                "durability": int()
            }:
                if engine.function_context.tool:
                    return cls.get_durability_ctx
                return None
            case _: return None
    @staticmethod
    def get_durability_given(engine:Engine, tool):
        ...
    @staticmethod
    def get_durability_ctx(engine:Engine):
        ...

class Engine_Tool_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "get_max_durability")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Tool_GetName(LoaderFunction):
    id = Identifier("engine", "tool/", "get_name")
    return_type = str
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Tool_SetName(LoaderFunction):
    id = Identifier("engine", "tool/", "set_name")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX###############XXX####
### XXX Engine Weapon XXX ###
####XXX###############XXX####

class Engine_Weapon_GetDurability(LoaderFunction):
    id = Identifier("engine", "Weapon/", "GetDurability")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_SetDurability(LoaderFunction):
    id = Identifier("engine", "Weapon/", "SetDurability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_max_durability")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_SetMaxDurability(LoaderFunction):
    id = Identifier("engine", "weapon/", "set_max_durability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetDamage(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_damage")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_SetDamage(LoaderFunction):
    id = Identifier("engine", "weapon/", "set_damage")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetAmmoType(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_ammo_type")
    return_type = AbstractAmmo
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetParentType(LoaderFunction):
    id = Identifier("engine", "weapon/", "get_parent_type")
    return_type = AbstractWeapon
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX##############XXX####
### XXX Engine Armor XXX ###
####XXX##############XXX####

class Engine_Armor_GetDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "get_durability")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "set_durability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "get_max_durability")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetMaxDurability(LoaderFunction):
    id = Identifier("engine", "armor/", "set_max_durability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_GetDamageReduction(LoaderFunction):
    id = Identifier("engine", "armor/", "get_damage_reduction")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetDamageReduction(LoaderFunction):
    id = Identifier("engine", "armor/", "set_damage_reduction")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX#############XXX####
### XXX Engine Ammo XXX ###
####XXX#############XXX####

class Engine_Ammo_GetCount(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_count")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_SetCount(LoaderFunction):
    id = Identifier("engine", "ammo/", "set_count")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetMaxCount(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_max_count")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetParentType(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_parent_type")
    return_type = AbstractAmmo
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetBonusDamage(LoaderFunction):
    id = Identifier("engine", "ammo/", "get_bonus_damage")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX#####################XXX####
### XXX Engine StatusEffect XXX ###
####XXX#####################XXX####

class Engine_StatusEffect_GetLevel(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_level")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_SetLevel(LoaderFunction):
    id = Identifier("engine", "status_effect/", "set_level")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetDuration(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_duration")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_SetDuration(LoaderFunction):
    id = Identifier("engine", "status_effect/", "set_duration")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetName(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_name")
    return_type = str
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetCause(LoaderFunction):
    id = Identifier("engine", "status_effect/", "get_cause")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX#############XXX####
### XXX Engine Item XXX ###
####XXX#############XXX####

class Engine_Item_GetCount(LoaderFunction):
    id = Identifier("engine", "item/", "get_count")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Item_SetCount(LoaderFunction):
    id = Identifier("engine", "item/", "set_count")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Item_GetMaxCount(LoaderFunction):
    id = Identifier("engine", "item/", "get_max_count")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX###############XXX####
### XXX Engine Player XXX ###
####XXX###############XXX####

class Engine_Player_Message(LoaderFunction):
    id = Identifier("engine", "player/", "message")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetHealth(LoaderFunction):
    id = Identifier("engine", "player/", "get_health")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SetHealth(LoaderFunction):
    id = Identifier("engine", "player/", "set_health")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "get_max_health")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SetMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "set_max_health")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_AddMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "add_max_health")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SubtractMaxHealth(LoaderFunction):
    id = Identifier("engine", "player/", "subtract_max_health")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_Heal(LoaderFunction):
    id = Identifier("engine", "player/", "heal")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {
                "amount": int() | dict()
            }: ...
            case _: return None
    @staticmethod
    def heal(engine:Engine, amount:int|dict):
        engine
class Engine_Player_Damage(LoaderFunction):
    id = Identifier("engine", "player/", "damage")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GiveObject(LoaderFunction):
    id = Identifier("engine", "player/", "give_object")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GiveStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "give_status_effect")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_HasStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "has_status_effect")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_RemoveStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "remove_status_effect")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetStatusEffect(LoaderFunction):
    id = Identifier("engine", "player/", "get_status_effect")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_HasItem(LoaderFunction):
    id = Identifier("engine", "player/", "has_item")
    return_type = bool
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_RemoveItem(LoaderFunction):
    id = Identifier("engine", "player/", "remove_item")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetItem(LoaderFunction):
    id = Identifier("engine", "player/", "get_item")
    return_type = Item
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedArmor(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_armor")
    return_type = Armor
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedWeapon(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_weapon")
    return_type = Weapon
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedTool(LoaderFunction):
    id = Identifier("engine", "player/", "get_equipped_tool")
    return_type = Tool
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_GetInput(LoaderFunction): # NOTE: this function may (probably will) require special implementation
    id = Identifier("engine", "player/", "get_input")
    return_type = Tool
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None

class Engine_Player_SetLocation(LoaderFunction):
    id = Identifier("engine", "player/", "set_location")
    return_type = Tool
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
            
class Engine_Player_GetLocation(LoaderFunction):
    id = Identifier("engine", "player/", "get_location")
    return_type = Tool
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX###############XXX####
### XXX Engine Random XXX ###
####XXX###############XXX####

class Engine_Random_Uniform(LoaderFunction):
    id = Identifier("engine", "random/", "uniform")
    return_type = int
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {
                "min": int(),
                "max": int()
            }: return cls.rand_range
            case {
                "rolls": int(),
                "pools": list()
            }: return cls.rand_choice
            case _: return None
    @staticmethod
    def rand_range(engine, min, max):
        return random.randint(min, max)
    @staticmethod
    def rand_choice(engine:Engine, rolls:int, pools:list[dict]):
        table = LootTable.fromDict({"rolls": rolls, "pools": pools})
        return table.roll(engine)

class Engine_Random_Weighted(LoaderFunction):
    id = Identifier("engine", "random/", "weighted")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {
                "rolls": int(),
                "pools": list()
            }: return cls.weighted_table
            case _: return None
    @staticmethod
    def weighted_table(engine:Engine, rolls:int, pools:list[dict]):
        table = LootTable.fromDict({"rolls": rolls, "pools": pools})
        return table.roll(engine)


####XXX#############XXX####
### XXX Engine Text XXX ###
####XXX#############XXX####
class Engine_Text_Builder(LoaderFunction):
    id = Identifier("engine", "text/", "builder")
    return_type = str
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {
                "text": list()
            }: return cls.builder
            case _: return None

    @staticmethod
    def builder(engine:Engine, text:list, seperator:str|dict=" "):
        out_text = []

        for element in text:
            if isinstance(element, str):
                out_text.append(element)
            elif isinstance(element, dict):
                ...

####XXX##############XXX####
### XXX Engine Logic XXX ###
####XXX##############XXX####
class Engine_Logic_Compare(LoaderFunction):
    id = Identifier("engine", "logic/", "compare")
    return_type = Tool
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None

####XXX#############XXX####
### XXX Engine Math XXX ###
####XXX#############XXX####
class Engine_Math_Solve(LoaderFunction):
    id = Identifier("engine", "math/", "solve")
    return_type = Tool
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None



