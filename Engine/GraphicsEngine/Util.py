# pylint: disable=[W,R,C,import-error]

import math


class Vector2d:
    __slots__ = ["x", "y"]

    def __init__(self, x:int|float, y:int|float):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x * other.x, self.y * other.y)
        if isinstance(other, (float|int)):
            return Vector2d(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x / other.x, self.y / other.y)
        if isinstance(other, (float|int)):
            return Vector2d(self.x / other, self.y / other)

    def __floordiv__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x // other.x, self.y // other.y)
        if isinstance(other, (float|int)):
            return Vector2d(self.x // other, self.y // other)

    def __pow__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x ** other.x, self.y ** other.y)
        if isinstance(other, (float|int)):
            return Vector2d(self.x ** other, self.y ** other)

    def copy(self):
        return Vector2d(self.x, self.y)
    
    def getLength(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2))

    def getAngle(self):
        """
        returns the angle in degrees (counterclockwise positive)
        """
        ...

    def rotate(self, angle):
        """
        rotates the vector by the given angle
        """
        ...
    
    def extend(self, length):
        """
        extends the vector by `length` in the direction it points
        """
        ...








