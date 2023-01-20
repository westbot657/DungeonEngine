# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
except ImportError:
    from Identifier import Identifier

class LoaderFunction:
    _functions = {}
    id: Identifier|None = None

    @classmethod
    def getFunction(cls, identifier:Identifier|str):
        if isinstance(identifier, Identifier): identifier = identifier.full()

        if identifier in cls._functions:
            return cls._functions[identifier]
        print(f"No loader-function with the id: {identifier}")
        return None

    @classmethod
    def call(cls, *_, **__):
        return None

    @classmethod
    def check(cls, args:dict):
        return False
    
    def __init_subclass__(cls):
        id = cls.id
        if isinstance(id, Identifier):
            id: Identifier

            if cls.call is LoaderFunction.call:
                print(f"Failed to load function without call: {id.full()}")
                return
            if cls.check is LoaderFunction.check:
                print(f"Failed to load function without check: {id.full()}")

            LoaderFunction._functions.update({id.full(): cls})
        else:
            print(f"Failed to load function without id: {cls}")

    @classmethod
    def _call(cls, data:dict):
        # check args
        if cls.check(data):
            return cls.call(**data)
        else:
            print(f"Invalid arguments given to function: {cls.id.full()}")


if __name__ == "__main__":
    class test(LoaderFunction):
        id = Identifier("test", "something/", "idk")

        @staticmethod
        def check(args):
            match args:
                case {
                    "a": int()
                }: return True
                case _: return False

        @staticmethod
        def call(a):
            return 5 * a

    LoaderFunction._call({"min": 6, "max": 20})


