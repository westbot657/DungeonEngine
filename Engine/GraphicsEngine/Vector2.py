# pylint: disable=[W,R,C,import-error]

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

    def __iter__(self):
        return iter([self.x, self.y])

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __dict__(self):
        return {
            "x": self.x,
            "y": self.y
        }
