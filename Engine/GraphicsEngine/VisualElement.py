# pylint: disable=[W,R,C,import-error]

try:
    from .Util import Vector2d
except ImportError:
    from Util import Vector2d

from pygame import Surface

"""
Base class for anything that renders
"""
class VisualElement:
    def __init__(self, parent):
        self.parent = parent
    def getWidth(self) -> int:
        ...
    def getHeight(self) -> int:
        ...
    def getSurface(self) -> Surface:
        ...
    def update(self, engine, surface, relativePosition:Vector2d):
        surface: VisualElement



