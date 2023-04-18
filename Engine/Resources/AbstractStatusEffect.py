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


        self.name: str|None = data.get("name", None)
        self.level: int|None = data.get("level", None)
        self.duration: int|None = data.get("duration", None)
        self.cause: int|None = data.get("cause", None)
        self.events: dict|None = data.get("events", None)


        self.is_template: bool = data.get("template", False)


    @classmethod
    def loadData(cls, engine) -> list:
        ...

