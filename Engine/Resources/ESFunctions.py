# pylint: disable=[W,R,C,import-error]

import math
import random

class MultistepFunction:
    
    def __init__(self, start, continuation):
        """
        `start` and `continuation` must be functions
        that return a tuple of (return_value:Any, continuation_environment:Any)
        the `continuation` function must have the first parameter
        take in the continuation_environment
        """
        
        self.start = start
        self.continuation = continuation


class ESBuiltin:
    _classes = {}

    @classmethod
    def register(cls, name:str):
        def decorator(clas):
            cls._classes[name] = clas
            return cls
        return decorator

class ESFunction:
    _functions = {}

    @classmethod
    def register(cls, name:str):
        def decorator(fun):
            cls._functions[name] = fun
            return cls
        return decorator

class ESClass:
    _classes = {}

    @classmethod
    def register(cls, name:str):
        def decorator(clas):
            cls._classes[name] = clas
            return cls
        return decorator


@ESBuiltin.register("math")
class Math:

    @classmethod
    def compare(cls, op, x, y):
        match op:
            case ">":
                return x > y
            case ">=":
                return x >= y
            case "<":
                return x < y
            case "<=":
                return x <= y
            case "==":
                return x == y
            case "!=":
                return x != y
            case "and":
                return x and y
            case "or":
                return x or y
    
    registry = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "compare": compare,
        "abs": abs,
        "sqrt": math.sqrt,
        "floor": math.floor,
        "ceil": math.ceil
    }
    
@ESBuiltin.register("random")
class Random:
    
    registry = {
        "choice": random.choice,
        "range": random.randint
    }


ESFunction.register("length")(len)


@ESFunction.register("output")
def output(es3, message):
    es3.engine.sendOutput()
