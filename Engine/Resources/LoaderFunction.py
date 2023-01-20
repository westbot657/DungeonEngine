# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
except ImportError:
    from Identifier import Identifier



class LoaderFunction:
    _functions = {}
    id = None
    args = {}

    @classmethod
    def call(cls, *_, **__):
        return None

    @classmethod
    def check(cls, args:dict):
        return None
    
    def __init_subclass__(cls):
        id = cls.id
        if isinstance(id, Identifier):
            id: Identifier

            if cls.args is None:
                print(f"Failed to load function without args: {id.full()}")
                return
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
        match data:
            case {
                    "min": int(),
                    "max": int()
                }:
                    print("case 1")
            case _:
                print("no match")
        return cls.call(...)


if __name__ == "__main__":
    class test(LoaderFunction):
        id = Identifier("test", "something/", "idk")
        args = {
            "args": {
                "a": int
            }
        }

        @staticmethod
        def call(a):
            return 5 * a

    LoaderFunction._call({"min": 6, "max": 20})


