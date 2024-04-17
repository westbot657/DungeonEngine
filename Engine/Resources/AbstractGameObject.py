# pylint: disable=[W,R,C,import-error]

from .GameObject import GameObject
from .Identifier import Identifier
from .EngineErrors import IdentifierError
from .Serializer import Serializer, Serializable

@Serializable("AbstractGameObject")
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

    def is_parent_of(self, other):
        p = other
        while p is not None:
            if self == p:
                return True
            p = p.parent
        return False
    
    def inherets_from(self, other):
        p = self
        while p is not None:
            if p == other:
                return True
            p = p.parent
        return False

    def get_children(self, depth:int=-1): # recursive way to get a flat list of all sub children to some depth
        children = []
        for child in self.children:
            if not child.is_template:
                children.append(child)
            if depth != 0:
                children += child.get_children(depth-1)
        return children

    def get_parent_chain(self):
        if self.parent is None:
            return []
        else:
            return [self.parent] + self.parent.get_parent_chain()

    def serialize(self):
        return {
            "children": Serializer.serialize(self.children),
            "parent": Serializer.serialize(self.parent),
            "is_template": Serializer.serialize(self.is_template)
        }
        
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

