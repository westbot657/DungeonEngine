# pylint: disable=[W,R,C,import-error]

try:
    from .VisualElement import VisualElement
    from .Util import Vector2d
except ImportError:
    from VisualElement import VisualElement
    from Util import Vector2d

from pygame import Surface

class ImageElement(VisualElement):

    def __init__(self, parent):
        super().__init__(parent)

    def getHeight(self) -> int:
        return super().getHeight()

    def getWidth(self) -> int:
        return super().getWidth()
    
    def getSurface(self) -> Surface:
        return super().getSurface()
    
    def update(self, engine, surface, relativePosition: Vector2d):
        return super().update(engine, surface, relativePosition)

