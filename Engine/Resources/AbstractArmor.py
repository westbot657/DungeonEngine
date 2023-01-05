# pylint: disable=[W,R,C,import-error]

try:
    from .Armor import Armor
    from .Identifier import Identifier
except ImportError:
    from Armor import Armor
    from Identifier import Identifier

class AbstractArmor:

    def __init__(self):
        ...


if __name__ == "__main__":
    class Test(AbstractArmor):
        def __init__(self, x, y):
            print(x, y)

    h = Test(2, 3)
    g = Test(4, 5)

    print(h.identifier)