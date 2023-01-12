# pylint: disable=[W,R,C,import-error]

try:
    from .Room import Room
    from .Identifier import Identifier
except ImportError:
    from Room import Room
    from Identifier import Identifier

import glob, json, re

class AbstractRoom:
    _loaded = {}
    _link_parents = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.parent: AbstractRoom|None = None
        self.children: list[AbstractRoom] = []
        
        if "parent" in data:
            AbstractRoom._link_parents.append((self, data["parent"]))

    @classmethod
    def loadData(cls) -> list:
        ...

