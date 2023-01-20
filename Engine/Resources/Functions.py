# pylint: disable=[W,R,C,import-error]

try:
    from .LoaderFunction import LoaderFunction
    from .Identifier import Identifier
except ImportError:
    from LoaderFunction import LoaderFunction
    from Identifier import Identifier

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
engine:item/set_max_count

engine:armor/get_durability
engine:armor/set_durability
engine:armor/get_damage_reduction
engine:armor/set_damage_reduction
engine:armor/get_max_durability
engine:armor/set_max_durability

"""


class Engine_Random_Uniform(LoaderFunction):
    id = Identifier("engine", "random/", "uniform")

    @classmethod
    def check(cls, engine, args):
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
    def rand_choice(engine, pools, rolls):
        ...


class Engine_Random_Weighted(LoaderFunction):
    id = Identifier("engine", "random/", "weighted")

    @classmethod
    def check(cls, engine, args):
        ...
    

