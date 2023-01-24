# pylint: disable=[W,R,C,import-error]

try:
    from .LoaderFunction import LoaderFunction
    from .Identifier import Identifier
    from .LootTable import LootTable
    from .EngineDummy import Engine

except ImportError:
    from LoaderFunction import LoaderFunction
    from Identifier import Identifier
    from LootTable import LootTable
    from EngineDummy import Engine

import random, math, re

"""
functions:
engine:tool/cancel_use
engine:tool/get_durability
engine:tool/set_durability
engine:tool/set_max_durability
engine:tool/get_max_durability

engine:random/uniform X
engine:random/weighted

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

"""




####XXX###############XXX####
### XXX Engine Random XXX ###
####XXX###############XXX####

class Engine_Random_Uniform(LoaderFunction):
    id = Identifier("engine", "random/", "uniform")
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
    def rand_choice(engine:Engine, pools:list[dict], rolls:int):
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
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Tool_SetDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "set_durability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Tool_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "tool/", "get_max_durability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Tool_GetName(LoaderFunction):
    id = Identifier("engine", "tool/", "get_name")
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
    id = Identifier("engine", "Weapon/", "GetMaxDurability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_SetMaxDurability(LoaderFunction):
    id = Identifier("engine", "Weapon/", "SetMaxDurability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetDamage(LoaderFunction):
    id = Identifier("engine", "Weapon/", "GetDamage")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_SetDamage(LoaderFunction):
    id = Identifier("engine", "Weapon/", "SetDamage")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetAmmoType(LoaderFunction):
    id = Identifier("engine", "Weapon/", "GetAmmoType")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Weapon_GetParentType(LoaderFunction):
    id = Identifier("engine", "Weapon/", "GetParentType")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX##############XXX####
### XXX Engine Armor XXX ###
####XXX##############XXX####

class Engine_Armor_GetDurability(LoaderFunction):
    id = Identifier("engine", "Armor/", "GetDurability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetDurability(LoaderFunction):
    id = Identifier("engine", "Armor/", "SetDurability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_GetMaxDurability(LoaderFunction):
    id = Identifier("engine", "Armor/", "GetMaxDurability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetMaxDurability(LoaderFunction):
    id = Identifier("engine", "Armor/", "SetMaxDurability")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_GetDamageReduction(LoaderFunction):
    id = Identifier("engine", "Armor/", "GetDamageReduction")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Armor_SetDamageReduction(LoaderFunction):
    id = Identifier("engine", "Armor/", "SetDamageReduction")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX#############XXX####
### XXX Engine Ammo XXX ###
####XXX#############XXX####

class Engine_Ammo_GetCount(LoaderFunction):
    id = Identifier("engine", "Ammo/", "GetCount")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_SetCount(LoaderFunction):
    id = Identifier("engine", "Ammo/", "SetCount")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetMaxCount(LoaderFunction):
    id = Identifier("engine", "Ammo/", "GetMaxCount")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetParentType(LoaderFunction):
    id = Identifier("engine", "Ammo/", "GetParentType")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Ammo_GetBonusDamage(LoaderFunction):
    id = Identifier("engine", "Ammo/", "GetBonusDamage")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX#####################XXX####
### XXX Engine StatusEffect XXX ###
####XXX#####################XXX####

class Engine_StatusEffect_GetLevel(LoaderFunction):
    id = Identifier("engine", "StatusEffect/", "GetLevel")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_SetLevel(LoaderFunction):
    id = Identifier("engine", "StatusEffect/", "SetLevel")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetDuration(LoaderFunction):
    id = Identifier("engine", "StatusEffect/", "GetDuration")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_SetDuration(LoaderFunction):
    id = Identifier("engine", "StatusEffect/", "SetDuration")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetName(LoaderFunction):
    id = Identifier("engine", "StatusEffect/", "GetName")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_StatusEffect_GetCause(LoaderFunction):
    id = Identifier("engine", "StatusEffect/", "GetCause")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX#############XXX####
### XXX Engine Item XXX ###
####XXX#############XXX####

class Engine_Item_GetCount(LoaderFunction):
    id = Identifier("engine", "Item/", "GetCount")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Item_SetCount(LoaderFunction):
    id = Identifier("engine", "Item/", "SetCount")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Item_GetMaxCount(LoaderFunction):
    id = Identifier("engine", "Item/", "GetMaxCount")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None


####XXX###############XXX####
### XXX Engine Player XXX ###
####XXX###############XXX####

class Engine_Player_Message(LoaderFunction):
    id = Identifier("engine", "Player/", "Message")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetHealth(LoaderFunction):
    id = Identifier("engine", "Player/", "GetHealth")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SetHealth(LoaderFunction):
    id = Identifier("engine", "Player/", "SetHealth")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetMaxHealth(LoaderFunction):
    id = Identifier("engine", "Player/", "GetMaxHealth")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SetMaxHealth(LoaderFunction):
    id = Identifier("engine", "Player/", "SetMaxHealth")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_AddMaxHealth(LoaderFunction):
    id = Identifier("engine", "Player/", "AddMaxHealth")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_SubtractMaxHealth(LoaderFunction):
    id = Identifier("engine", "Player/", "SubtractMaxHealth")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_Heal(LoaderFunction):
    id = Identifier("engine", "Player/", "Heal")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_Damage(LoaderFunction):
    id = Identifier("engine", "Player/", "Damage")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GiveObject(LoaderFunction):
    id = Identifier("engine", "Player/", "GiveObject")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GiveStatusEffect(LoaderFunction):
    id = Identifier("engine", "Player/", "GiveStatusEffect")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_HasStatusEffect(LoaderFunction):
    id = Identifier("engine", "Player/", "HasStatusEffect")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_RemoveStatusEffect(LoaderFunction):
    id = Identifier("engine", "Player/", "RemoveStatusEffect")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetStatusEffect(LoaderFunction):
    id = Identifier("engine", "Player/", "GetStatusEffect")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_HasItem(LoaderFunction):
    id = Identifier("engine", "Player/", "HasItem")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_RemoveItem(LoaderFunction):
    id = Identifier("engine", "Player/", "RemoveItem")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetItem(LoaderFunction):
    id = Identifier("engine", "Player/", "GetItem")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedArmor(LoaderFunction):
    id = Identifier("engine", "Player/", "GetEquippedArmor")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedWeapon(LoaderFunction):
    id = Identifier("engine", "Player/", "GetEquippedWeapon")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None
class Engine_Player_GetEquippedTool(LoaderFunction):
    id = Identifier("engine", "Player/", "GetEquippedTool")
    @classmethod
    def check(cls, engine:Engine, args:dict):
        match args:
            case {}: ...
            case _: return None

