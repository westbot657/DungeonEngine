# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
except ImportError:
    from Identifier import Identifier


class AbstractItem:

    def __new__(cls, identifier:Identifier, data:dict):
        self = super().__new__(cls)
        
        self.identifier = identifier
        self._raw_data = data

        self.parent = None
        self.children = []

        self.name = data.get("name", None)
        self.max_count = data.get("max_count", None)
        self.count = data.get("count", self.max_count)

        return self

