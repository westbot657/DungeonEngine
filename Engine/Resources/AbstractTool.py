# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Tool import Tool
    from .EngineErrors import InvalidObjectError
except ImportError:
    from Identifier import Identifier
    from Tool import Tool
    from EngineErrors import InvalidObjectError


class AbstractTool:

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractTool] = []
        self.parent: AbstractTool|None = None

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)
    
    @classmethod
    def loadData(cls) -> list:
        ...
