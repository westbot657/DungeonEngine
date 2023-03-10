# pylint: disable=[W,R,C,import-error]

try:
    from .Identifier import Identifier
    from .EngineDummy import Engine
except ImportError:
    from Identifier import Identifier
    from EngineDummy import Engine

from typing import Any

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
    def fullDisplay(cls, engine:Engine, data:dict|Any):
        if not isinstance(data, dict):
            return str(data)
        out = cls._fullDisplay(engine, data)
        return out

    @classmethod
    def quickDisplay(cls, engine:Engine, data:dict|Any):
        if not isinstance(data, dict):
            return str(data)
        out = cls._quickDisplay(engine, data)
        return out

    @classmethod
    def _fullDisplay(cls, engine:Engine, data:dict) -> str:
        if isinstance(data, dict):
            if (funcs := data.get("functions", None)) is not None:
                out = []
                for func in funcs:
                    out.append(cls._fullDisplay(engine, func))
                return "\n".join(out)
            if (func_name := data.get("function", None)) is not None:
                if func := cls.getFunction(func_name):
                    func: LoaderFunction
                    args = {}
                    for key, item in data.items():
                        if key in ["function", "predicate", "#store"]: continue
                        args.update({key: cls._fullDisplay(engine, item)})
                    return func.getFullDisplay(engine, args)
            out = {}
            for key, item in data:
                if isinstance(item, dict):
                    out.update({key: cls._fullDisplay(engine, item)})
                elif isinstance(item, list):
                    out.update({key: str([cls._fullDisplay(engine, i) for i in item])})
                else:
                    out.update({key: str(item)})
            return str(out)
        if isinstance(data, list):
            return str([cls._fullDisplay(engine, i) for i in data])

        return str(data)

    @classmethod
    def _quickDisplay(cls, engine:Engine, data:dict) -> str:
        if isinstance(data, dict):
            if (funcs := data.get("functions", None)) is not None:
                out = []
                for func in funcs:
                    out.append(cls._quickDisplay(engine, func))
                return "\n".join(out)
            if (func_name := data.get("function", None)) is not None:
                if func := cls.getFunction(func_name):
                    func: LoaderFunction
                    args = {}
                    for key, item in data.items():
                        if key in ["function", "predicate", "#store"]: continue
                        args.update({key: cls._quickDisplay(engine, item)})
                    return func.getQuickDisplay(engine, args)
            out = {}
            for key, item in data:
                if isinstance(item, dict):
                    out.update({key: cls._quickDisplay(engine, item)})
                elif isinstance(item, list):
                    out.update({key: str([cls._quickDisplay(engine, i) for i in item])})
                else:
                    out.update({key: str(item)})
            return str(out)
        if isinstance(data, list):
            return str([cls._quickDisplay(engine, i) for i in data])

        return str(data)


    def getFullDisplay(self, engine:Engine, data:dict) -> str:
        # overridden by functions
        return f"{self.id.full()} {data}"
    
    def getQuickDisplay(self, engine:Engine, data:dict) -> str:
        # overridden by functions
        return f"{self.id.full()} ..."

    @staticmethod
    def _check_dummy_return(*_, **__):
        pass # don't need to do anything in the dummy function

    @classmethod
    def check(cls, engine:Engine, args:dict):
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



