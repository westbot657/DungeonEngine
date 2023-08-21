# pylint: disable=[W,R,C,import-error]

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (list, tuple)):
            return Vector2(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (list, tuple)):
            return Vector2(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (list, tuple)):
            return Vector2(self.x * other[0], self.y * other[1])

    def __iter__(self):
        return iter([self.x, self.y])

    def list(self):
        return [self.x, self.y]

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __dict__(self):
        return {
            "x": self.x,
            "y": self.y
        }
    
    @staticmethod
    def min(vec1, vec2):
        return Vector2(min(vec1.x, vec2.x), min(vec1.y, vec2.y))

    @staticmethod
    def max(vec1, vec2):
        return Vector2(max(vec1.x, vec2.x), max(vec1.y, vec2.y))

    def clamp(self, minx, miny, maxx, maxy):
        if minx is not ...:
            self.x = max(minx, self.x)
        if miny is not ...:
            self.y = max(miny, self.y)
        if maxx is not ...:
            self.x = min(maxx, self.x)
        if maxy is not ...:
            self.y = min(maxy, self.y)
