# pylint: disable=[W,R,C,import-error]


"""
Base class for anything that moves
"""
class PhysicsElement:

    def update(self, screen, relativePosition):
        ...

