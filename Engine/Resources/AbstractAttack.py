# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .Attack import Attack
except ImportError:
    from Identifier import Identifier
    from Attack import Attack

class AbstractAttack:
    _loaded = {}
    _link_parents = []
    identity = Identifier("engine", "abstract/", "attack")
    def __init__(self, data:dict):
        ...

    @classmethod
    def fromDict(cls, data:dict):
        atk = cls(data)
        # TODO: link parent if needed (and whatever else needs to be done)
        return atk

    @classmethod
    def loadData(cls, engine):

        # TODO: load attacks

        return cls._loaded

