# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .Identifier import Identifier
except ImportError:
    from EngineDummy import Engine
    from Identifier import Identifier


class Location:

    def __init__(self, world_pos:Identifier, x:int, y:int):
        self.world_pos = world_pos
        self.x = x
        self.y = y

    @classmethod
    def from_dict(cls, engine:Engine, data):
        # could check that position is invalid?
        return cls(Identifier(data["world_pos"]), *data["position"])

    def __repr__(self):
        return f"{self.world_pos.full()} ({self.x}, {self.y})"

