# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
except ImportError:
    from EngineDummy import Engine


class Location:

    def __init__(self, world_pos:str, x:int, y:int):
        self.world_pos = world_pos
        self.x = x
        self.y = y

    @classmethod
    def from_dict(cls, engine:Engine, data):
        # could check that position is invalid?
        return cls(data["room"], *data["position"])

