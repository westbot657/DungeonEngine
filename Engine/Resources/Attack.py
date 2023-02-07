# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
except ImportError:
    from Identifier import Identifier

class Attack:
    _loaded = {}
    _link_parents = []
    identifier = Identifier("engine", "", "attack")
    def __init__(self, data:dict):
        ...


    @classmethod
    def loadData(cls):
        ...

