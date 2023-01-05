# pylint: disable=[W,R,C,import-error]

from .Armor import Armor
from .Identifier import Identifier

class AbstractArmor:

    def __init__(self, identifier:Identifier, data:dict):
        ...

    def __init_subclass__(cls, *args, **kwargs) -> None:
        print(f"test?  {args}  {kwargs}")


if __name__ == "__main__":
    class Test(AbstractArmor):
        def __init__(self, x, y):
            print(x, y)


    h = Test(2, 3)