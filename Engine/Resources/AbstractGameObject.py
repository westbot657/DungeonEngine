# pylint: disable=[W,R,C,import-error]

try:
    from .GameObject import GameObject
    from .Identifier import Identifier
    from .EngineErrors import IdentifierError
except ImportError:
    from GameObject import GameObject
    from Identifier import Identifier
    from EngineErrors import IdentifierError

class AbstractGameObject:
    _game_object_types = {}
    identifier: Identifier = None
    def __init_subclass__(cls) -> None:
        if cls.identifier is None:
            raise IdentifierError(f"New AbstractGameObject type: '{cls.__qualname__}' does not have an 'identifier' property defined")

        AbstractGameObject._game_object_types.update({cls.identifier.full(): cls})




