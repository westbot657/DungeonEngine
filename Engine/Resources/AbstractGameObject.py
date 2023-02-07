
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
    identity: Identifier = None
    def __init_subclass__(cls) -> None:
        if cls.identity is None:
            raise IdentifierError(f"New AbstractGameObject type: '{cls.__qualname__}' does not have an 'identity' property defined")

        AbstractGameObject._game_object_types.update({cls.identity.full(): cls})




