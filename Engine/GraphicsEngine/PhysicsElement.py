# pylint: disable=[W,R,C,import-error]

try:
    from .Util import Vector2d
except ImportError:
    from Util import Vector2d

"""
Base class for anything that moves
"""
class PhysicsElement:

    def __init__(self, position:Vector2d, velocity:Vector2d=None, acceleration:Vector2d=None):
        self.position = position
        self.velocity = velocity or Vector2d(0, 0)
        self.acceleration = acceleration or Vector2d(0, 0)

    def update(self, engine, surface, relativePosition:Vector2d):
        ...

