# pylint: disable=[W,R,C,import-error]

from .EngineDummy import Engine

class Inventory:
    def __init__(self):
        self.contents: list
        self.equips: dict

    @classmethod
    def from_list(cls, function_memory, data:list): ...


