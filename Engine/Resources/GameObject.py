# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .EngineErrors import EngineError, IdentifierError
    from .FunctionalElement import FunctionalElement
except ImportError:
    from Identifier import Identifier
    from EngineErrors import EngineError, IdentifierError
    from FunctionalElement import FunctionalElement

class GameObject(FunctionalElement):
    _game_object_types = {}
    
    identifier: Identifier = None
    def __init_subclass__(cls) -> None:
        if cls.identifier is None:
            raise IdentifierError(f"New GameObject type: '{cls.__qualname__}' does not have an 'identifier' property defined")

        GameObject._game_object_types.update({cls.identifier.full(): cls})

    def __init__(self):
        self.owner = None

    def bonuses(self, function_memory):
        return None

    def quickStats(self, function_memory):
        raise EngineError(f"game object has not defined quickStats() method!")

    def fullStats(self, function_memory, is_equipped=False):
        raise EngineError(f"game object has not defined fullStats() method!")


