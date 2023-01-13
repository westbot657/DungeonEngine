# pylint: disable=[W,R,C,import-error]

try:
    from .EngineFunction import EngineFunction
    from .Identifier import Identifier
except ImportError:
    from EngineFunction import EngineFunction
    from Identifier import Identifier

import random, math, re

"""
functions:
engine:tool/cancel_use

engine:random/uniform
engine:random/weighted

engine:player/message
engine:player/give_item
engine:player/get_status_effect
engine:player/get_health
engine:player/get_max_health
engine:player/heal
engine:player/damage
engine:player/get_equipped_weapon
engine:player/get_equipped_armor
engine:player/has_item
engine:player/get_item


engine:status_effect/get_level
engine:status_effect/get_duration


"""


@EngineFunction.Method(
    Identifier("engine", "random", "uniform"),
    {
        "args": {
            "min": int,
            "max": int
        }
    }
)
def random_uniform_int(min_value, max_value):
    return random.randint(min_value, max_value)




















