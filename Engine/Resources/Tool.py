# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier

class Tool(GameObject):
    identifier = Identifier("engine", "object/", "tool")
    def __init__(self, abstract):
        self.abstract = abstract
        ...
        

