# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .EngineDummy import Engine
except ImportError:
    from Identifier import Identifier
    from EngineDummy import Engine

class LoaderFunction:
    _functions = {}
    id: Identifier|None = None
    return_type: list|tuple|tuple = None

    @classmethod
    def getFunction(cls, identifier:Identifier|str):
        if isinstance(identifier, Identifier): identifier = identifier.full()

        if identifier in cls._functions:
            return cls._functions[identifier]
        print(f"No loader-function with the id: {identifier}")
        return None

    @classmethod
    def fullDisplay(cls, engine:Engine, data:dict):
        ...

    @classmethod
    def quickDisplay(cls, engine:Engine, data:dict):
        ...

    def _fullDisplay(self, engine:Engine, data:dict):
        ...
    
    def _quickDisplay(self, engine:Engine, data:dict):
        ...

    def getFullDisplay(self, engine:Engine, data:dict) -> str:
        # overridden by functions
        ...
    
    def getQuickDisplay(self, engine:Engine, data:dict) -> str:
        # overridden by functions
        ...

    @staticmethod
    def _check_dummy_return(*_, **__):
        pass # don't need to do anything in the dummy function

    @classmethod
    def check(cls, engine, args:dict):
        return cls._check_dummy_return
    
    def __init_subclass__(cls):
        id = cls.id
        if isinstance(id, Identifier):
            id: Identifier

            if cls.check is LoaderFunction.check:
                print(f"Failed to load function without check: {id.full()}")
                return

            LoaderFunction._functions.update({id.full(): cls})
        else:
            print(f"Failed to load function without id: {cls}")
        
        if not isinstance(cls.return_type, (list, tuple)):
            cls.return_type = [cls.return_type]

    @classmethod
    def _call(cls, engine, data:dict):
        # check args
        if call := cls.check(engine, data):
            return call(engine, **data)
        else:
            print(f"Invalid arguments given to function: {cls.id.full()}")



