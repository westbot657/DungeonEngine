# pylint: disable=[W,R,C,import-error]

try:
    from .StatusEffect import StatusEffect
    from .Identifier import Identifier
except ImportError:
    from StatusEffect import StatusEffect
    from Identifier import Identifier

import glob, json, re

class AbstractStatusEffect:
    _loaded = {}
    _link_parents = []

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.parent: AbstractStatusEffect|None = None
        self.children: list[AbstractStatusEffect] = []

        if "parent" in data:
            AbstractStatusEffect._link_parents.append((self, data["parent"]))

    @classmethod
    def loadData(cls, inline_handler) -> list:
        ...

