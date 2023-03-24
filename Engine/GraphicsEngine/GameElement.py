# pylint: disable=[W,R,C,import-error]

try:
    from .PhysicsElement import PhysicsElement
    from .VisualElement import VisualElement
    from .Util import Vector2d
except ImportError:
    from PhysicsElement import PhysicsElement
    from VisualElement import VisualElement
    from Util import Vector2d

from pygame import Surface


class GameElement:

    def __init__(self, parent, physicsElement:PhysicsElement, visualElement:VisualElement):
        self.parent = parent
        self.physicsElement = physicsElement
        self.visualElement = visualElement

        physicsElement.parent = self
        visualElement.parent = self

    def update(self, engine, surface:Surface, relativePosition:Vector2d):

        self.physicsElement.update(engine, surface, relativePosition)

        self.visualElement.update(engine, surface, relativePosition + self.physicsElement.position)




