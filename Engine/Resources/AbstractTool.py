# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Tool import Tool
    from .EngineErrors import InvalidObjectError
    from .AbstractGameObject import AbstractGameObject
except ImportError:
    from Identifier import Identifier
    from Tool import Tool
    from EngineErrors import InvalidObjectError
    from AbstractGameObject import AbstractGameObject


class AbstractTool(AbstractGameObject):
    identifier: Identifier = Identifier("engine", "abstract/", "tool")
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractTool] = []
        self.parent: AbstractTool|None = None

        self.is_template: bool = data.get("template", False)

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)
    
    def createInstance(self, **override_values) -> Tool:
        if self.is_template:
            ...
        else:
            return Tool(self
            )
    
    @classmethod
    def loadData(cls, inline_handler) -> list:
        ...
