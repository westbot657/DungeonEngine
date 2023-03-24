# pylint: disable=[W,R,C,import-error]

try:
    from .Hitbox import Hitbox
    from .Util import Vector2d, Time
except ImportError:
    from Hitbox import Hitbox
    from Util import Vector2d, Time

from pygame import Surface


"""
Base class for anything that moves
"""
class PhysicsElement: # yay! calculus probably! (this is sarcasm)

    def __init__(self, parent, hitbox, position:Vector2d, velocity:Vector2d=None, accelerations:dict[str, dict[str, int|float|Vector2d]]={}):
        self.parent = parent
        self.hitbox = hitbox
        self.position = position
        self.velocity = velocity or Vector2d(0, 0)
        self.acceleration = Vector2d(0, 0)

        self.accelerations:dict[str, dict[str, int|float|Vector2d]] = accelerations

        self.position_locked = False
        self.elasticity = 0.0

    def addAcceleration(self, identifier:str, acceleration:Vector2d, duration:float):
        """
        identifier: a name for the accelerator, so that it may be removed at a later point
        acceleration: the vector to accelerate at
        duration: time in seconds to accelerate for
        """
        self.accelerations.update({
            identifier: {
                "acceleration": acceleration,
                "duration": duration
            }
        })

    def removeAcceleration(self, identifier:str):
        if identifier in self.accelerations:
            self.accelerations.pop(identifier)

    def getAcceleration(self):
        return self.acceleration

    def lockPosition(self):
        self.position_locked = True

    def unlockPosition(self):
        self.position_locked = False

    def setPosition(self, position:Vector2d):
        self.position = position

    def move(self, offset:Vector2d):
        self.position += offset

    def update(self, engine, surface, relativePosition:Vector2d):
        if self.position_locked:
            return

        # movement and collision
        







