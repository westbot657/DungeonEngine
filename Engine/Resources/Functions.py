# pylint: disable=[W,R,C,import-error]

try:
    from .EngineFunction import EngineFunction
    from .Identifier import Identifier
except ImportError:
    from EngineFunction import EngineFunction
    from Identifier import Identifier

import random


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




















