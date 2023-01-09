# pylint: disable=[W,R,C,import-error]

try:
    from .Dungeon import Dungeon, Room
    from .Identifier import Identifier
except ImportError:
    from Dungeon import Dungeon, Room
    from Identifier import Identifier


class AbstractDungeon:

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data

    @classmethod
    def loadData(cls) -> list:
        ...

