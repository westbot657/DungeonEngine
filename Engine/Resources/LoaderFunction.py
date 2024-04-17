# pylint: disable=[W,R,C,import-error]

from Identifier import Identifier
from EngineDummy import Engine
from Logger import Log
from FunctionMemory import FunctionMemory

from typing import Any

import json

class LoaderFunction:
    _functions = {}
    _pre_evaluators = [] # a list of identifiers
    id: Identifier|None = None
    return_type: list|tuple|tuple = None
    pre_evaluator: bool = False
    pre_evaluate_args: bool = True

    script_flags: dict = {}

    @classmethod
    def getRelatedFunctions(cls, value_type:str|Identifier) -> list:
        if isinstance(value_type, Identifier): value_type = value_type.full()
        related = []
        for name, value in cls._functions.items():
            name: str
            if name.startswith(value_type + "/"):
                related.append(value)
        return related
    
    @classmethod
    def getRelatedFunctionNames(cls, value_type:str|Identifier) -> list:
        if isinstance(value_type, Identifier): value_type = value_type.full()
        related = []
        for name in cls._functions:
            name: str
            if name.startswith(value_type + "/"):
                related.append(name)
        return related

    @classmethod
    def isPreEvaluator(cls, func:str|Identifier):
        if isinstance(func, Identifier): func = func.full()
        return func in cls._pre_evaluators

    @classmethod
    def getFunction(cls, identifier:Identifier|str):
        if isinstance(identifier, Identifier): identifier = identifier.full()

        if identifier in cls._functions:
            return cls._functions[identifier]
        Log["WARNING"]["loader function"](f"No loader-function with the id: {identifier}")
        return None

    @classmethod
    def fullDisplay(cls, function_memory:FunctionMemory, data:dict|Any):
        if not isinstance(data, dict):
            return str(data)
        out = cls._fullDisplay(function_memory, data)
        return out

    @classmethod
    def quickDisplay(cls, function_memory:FunctionMemory, data:dict|Any):
        if not isinstance(data, dict):
            return str(data)
        out = cls._quickDisplay(function_memory, data)
        return out

    @classmethod
    def _fullDisplay(cls, function_memory:FunctionMemory, data:dict) -> str:
        if isinstance(data, dict):
            if (funcs := data.get("functions", None)) is not None:
                out = []
                for func in funcs:
                    out.append(cls._fullDisplay(function_memory, func))
                return "\n".join(out)
            if (func_name := data.get("function", None)) is not None:
                if func := cls.getFunction(func_name):
                    func: LoaderFunction
                    args = {}
                    for key, item in data.items():
                        if key in ["function", "predicate", "#store"]: continue
                        args.update({key: cls._fullDisplay(function_memory, item)})
                    return func.getFullDisplay(function_memory, args)
            out = {}
            for key, item in data:
                if isinstance(item, dict):
                    out.update({key: cls._fullDisplay(function_memory, item)})
                elif isinstance(item, list):
                    out.update({key: str([cls._fullDisplay(function_memory, i) for i in item])})
                else:
                    out.update({key: str(item)})
            return str(out)
        if isinstance(data, list):
            return str([cls._fullDisplay(function_memory, i) for i in data])

        return str(data)

    @classmethod
    def _quickDisplay(cls, function_memory:FunctionMemory, data:dict) -> str:
        if isinstance(data, dict):
            if (funcs := data.get("functions", None)) is not None:
                out = []
                for func in funcs:
                    out.append(cls._quickDisplay(function_memory, func))
                return "\n".join(out)
            if (func_name := data.get("function", None)) is not None:
                if func := cls.getFunction(func_name):
                    func: LoaderFunction
                    args = {}
                    for key, item in data.items():
                        if key in ["function", "predicate", "#store"]: continue
                        args.update({key: cls._quickDisplay(function_memory, item)})
                    return func.getQuickDisplay(function_memory, args)
            out = {}
            for key, item in data:
                if isinstance(item, dict):
                    out.update({key: cls._quickDisplay(function_memory, item)})
                elif isinstance(item, list):
                    out.update({key: str([cls._quickDisplay(function_memory, i) for i in item])})
                else:
                    out.update({key: str(item)})
            return str(out)
        if isinstance(data, list):
            return str([cls._quickDisplay(function_memory, i) for i in data])

        return str(data)

    @classmethod
    def getFullDisplay(self, function_memory:FunctionMemory, data:dict) -> str:
        # overridden by functions
        return f"{self.id.full()} {data}"
    
    @classmethod
    def getQuickDisplay(self, function_memory:FunctionMemory, data:dict) -> str:
        # overridden by functions
        return f"{self.id.full()} ..."

    @staticmethod
    def _check_dummy_return(*_, **__):
        pass # don't need to do anything in the dummy function

    @classmethod
    def check(cls, function_memory, args:dict):
        return cls._check_dummy_return
    
    def __init_subclass__(cls):
        id = cls.id
        if isinstance(id, Identifier):
            id: Identifier

            if cls.check is LoaderFunction.check:
                Log["ERROR"]["loader function"](f"Failed to load function without check: {id.full()}")
                return

            LoaderFunction._functions.update({id.full(): cls})
            if cls.pre_evaluator:
                LoaderFunction._pre_evaluators.append(id.full())

        else:
            Log["ERROR"]["loader function"](f"Failed to load function without id: {cls}")
        
        if not isinstance(cls.return_type, (list, tuple)):
            cls.return_type = [cls.return_type]

    @classmethod
    def _call(cls, function_memory, data:dict):
        # check args
        try:
            _dat = json.dumps(data)#, indent=2)
        except TypeError as e:
            _dat = str(data)
        Log["debug"]["loader function"](f"calling '{cls.__name__}'")# with data:\n{_dat}\n")
        if call := cls.check(function_memory, data):
            return call(function_memory, **data)
        else:
            Log["ERROR"]["loader function"](f"Invalid arguments given to function: {cls.id.full()}: {data}")



