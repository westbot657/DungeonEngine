# pylint: disable=[W,R,C,import-error]

class Location:

    def __init__(self, world_pos:str, x:int, y:int):
        self.world_pos = world_pos
        self.x = x
        self.y = y

    @classmethod
    def from_dict(cls, data):
        return cls(data["room"], *data["position"])

