# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
except ImportError:
    from Identifier import Identifier

class EngineFunction:
    _instance = None
    _functions = {}

    @classmethod
    def Method(cls, identifier:Identifier, argument_data:dict=None):

        def wrapper(callback):
            cls._functions.update({identifier.ID(): (callback, argument_data)})
            return callback

        return wrapper

    @classmethod
    def get(cls, identity:str|Identifier, default:str|Identifier|None=None):
        if isinstance(identity, Identifier): identity = Identifier.ID()
        if identity in cls._functions:
            return cls._functions.get(identity)
        elif default is not None:
            if isinstance(default, Identifier): default = default.ID()
            if default in cls._functions: return cls._functions.get(default)
            else: raise Exception(f"Functions do not exist: {identity}, {default}")





