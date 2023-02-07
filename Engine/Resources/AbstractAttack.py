# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
except ImportError:
    from Identifier import Identifier

class AbstractAttack:
    _loaded = {}
    _link_parents = []
    identity = Identifier("engine", "abstract/", "attack")
    def __init__(self, data:dict):
        ...


    @classmethod
    def loadData(cls):
        ...

