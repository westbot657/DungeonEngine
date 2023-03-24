# pylint: disable=[W,R,C,import-error]

try:
    from .VisualElement import VisualElement
    from .Util import Vector2d
except ImportError:
    from VisualElement import VisualElement
    from Util import Vector2d

from pygame import Surface

class TextElement(VisualElement):

    def __init__(self, parent, text:str):
        super().__init__(parent)
        self.text = text

    def getWidth(self) -> int:
        return super().getWidth()
    
    def getHeight(self) -> int:
        return super().getHeight()
    
    def getSurface(self) -> Surface:
        return super().getSurface()

    def update(self, engine, surface, relativePosition: Vector2d):
        return super().update(engine, surface, relativePosition)

