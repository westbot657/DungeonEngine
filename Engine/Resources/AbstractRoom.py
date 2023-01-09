# pylint: disable=[W,R,C,import-error]

try:
    from .Room import Room
    from .Identifier import Identifier
except ImportError:
    from Room import Room
    from Identifier import Identifier

import glob, json, re

class AbstractRoom:

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.parent: AbstractRoom|None = None
        self.children: list[AbstractRoom] = []
        

    @classmethod
    def loadData(cls) -> list:
        ...

