# pylint: disable=[W,R,C,import-error]

try:
    from .Dungeon import Dungeon
    from .Identifier import Identifier
except ImportError:
    from Dungeon import Dungeon
    from Identifier import Identifier

import glob, json, re

""" meh_dungeon.json
{
    "name": "meh dungeon",
    "version": 0.1,
    "entry_point": ""
}
"""

class AbstractDungeon:

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data

    @classmethod
    def loadData(cls) -> list:
        ...

