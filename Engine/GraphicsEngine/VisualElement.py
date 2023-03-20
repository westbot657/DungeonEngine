# pylint: disable=[W,R,C,import-error]

try:
    from .Util import Vector2d
except ImportError:
    from Util import Vector2d


"""
Base class for anything that renders on to the screen
"""
class VisualElement:

    def getWidth(self):
        ...
    def getHeight(self):
        ...
    
    def render(self, engine, surface, relativePosition:Vector2d):
        ...

