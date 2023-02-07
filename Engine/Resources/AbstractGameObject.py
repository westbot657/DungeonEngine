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
    identity: Identifier = None
    def __init_subclass__(cls) -> None:
        if cls.identity is None:
            raise IdentifierError(f"New AbstractGameObject type: '{cls.__qualname__}' does not have an 'identity' property defined")

        AbstractGameObject._game_object_types.update({cls.identity.full(): cls})

    def __init__(self, *args, **kwargs):
        self.children: list = []
        self.parent: AbstractGameObject|None = None
        self.is_template: bool = False

    def get_children(self, depth:int=-1): # recursive way to get a flat list of all sub children to some depth
        children = []
        for child in self.children:
            if child.is_template: continue
            children.append(child)
            if depth != 0:
                children += child.get_children(depth-1)
        return children



