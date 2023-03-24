# pylint: disable=[W,R,C,import-error]

import math, time


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

class Time:

    def __init__(self, seconds:float):
        self.seconds = seconds
        self._start_time = time.time()
        self._paused = True
        self._pause_time = self._start_time

    def pause(self):
        self._pause_time = time.time()
        self._paused = True
        return self
        
    def resume(self):
        self._start_time += (time.time() - self._pause_time)
        self._pause_time = 0
        self._paused = False
        return self

    def reset(self):
        self._paused = True
        self._start_time = time.time()
        self._pause_time = self._start_time
        return self

    def start(self):
        self._pause_time = 0
        self._paused = False
        self._start_time = time.time()
        return self

    def getTimeElapsed(self) -> float:
        if self._paused:
            return self._pause_time - self._start_time
        return time.time() - self._start_time

    def getTimeRemaining(self) -> float:
        return self.seconds - self.getTimeElapsed()

    def __float__(self) -> float:
        return self.getTimeElapsed()

    def __int__(self) -> int:
        return int(self.__float__())


