# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .EngineErrors import EngineError, IdentifierError
except ImportError:
    from Identifier import Identifier
    from EngineErrors import EngineError, IdentifierError

class GameObject:
    _game_object_types = {}
    
    identifier: Identifier = None
    def __init_subclass__(cls) -> None:
        if cls.identifier is None:
            raise IdentifierError(f"New GameObject type: '{cls.__qualname__}' does not have an 'identifier' property defined")

        GameObject._game_object_types.update({cls.identifier.full(): cls})

    def bonuses(self, engine):
        return None

    def quickStats(self, engine):
        raise EngineError(f"game object has not defined quickStats() method!")

    def fullStats(self, engine, is_equipped=False):
        raise EngineError(f"game object has not defined fullStats() method!")


