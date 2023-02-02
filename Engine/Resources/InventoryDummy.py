
try:
    from .EngineDummy import Engine
except ImportError:
    from EngineDummy import Engine

class Inventory:
    def __init__(self):
        self.contents: list
        self.equips: dict

    @classmethod
    def from_list(cls, engine:Engine, data:list): ...


