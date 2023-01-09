# pylint: disable=[W,R,C,import-error]

try:
    from .StatusEffect import StatusEffect
    from .Identifier import Identifier
except ImportError:
    from StatusEffect import StatusEffect
    from Identifier import Identifier

import glob, json, re

class AbstractStatusEffect:
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.parent: AbstractStatusEffect|None = None
        self.children: list[AbstractStatusEffect] = []

    @classmethod
    def loadData(cls) -> list:
        ...

