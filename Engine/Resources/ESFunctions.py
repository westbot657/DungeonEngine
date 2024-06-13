# pylint: disable=W,R,C,import-error,no-member


import time
import re
import math
import random

from typing import Any

try:
    from .EngineErrors import FinalScriptError, ScriptError, EOF
except ImportError as e:
    from EngineErrors import FinalScriptError, ScriptError, EOF
    

class ESFunction:
    funcs = {}
    
    _instance = None
    
    def __new__(cls, metadata=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._instance.metadata = metadata
        return cls._instance

    def __call__(self, callable):
        callable.metadata = self.metadata # pylint: disable=access-member-before-definition
        self.metadata = None
        ESFunction.funcs.update({callable.__name__: callable})
        return callable

class ESClass:
    classes = {}
    
    def __init_subclass__(cls) -> None:
        cls._functions = ESFunction.funcs
        ESFunction.funcs = {}
        ESClass.classes.update({cls.__name__: cls})




class ESPlayer(ESClass):
    def __init__(self, player):
        self.player = player
        
        self.attrs = {
            "tag": self.tag
        }

    @staticmethod
    def _tag_parser(tokens:list, es3) -> dict:
        
        if tokens and tokens[0].type in ["WORD", "KEYWORD", "COMMAND"]:
            name = tokens[0].pop().value
        
            if tokens and tokens[0] == ("LITERAL", "="):
                eq = tokens.pop(0)
                if tokens:
                    expr = es3.expression(tokens)
                    
                    return {"tag-assign": [name.value, expr]}
                else:
                    raise FinalScriptError(f"expected expression after '=' @ {eq.get_location()}")
            
            elif tokens:
                raise tokens[0].expected("'=' or end of expression", False)
            else:
                return {"tag-ref": name.value}
        
        elif tokens:
            raise FinalScriptError(f"Expected tag label @ {tokens[0].get_location()}")
        else:
            raise FinalScriptError("Expected tag label @ {tlast_location}")

    @ESFunction({"macro-parser": _tag_parser})
    def tag(self, data:dict):
        ...

class ESDungeon(ESClass):
    def __init__(self, dungeon):
        self.dungeon = dungeon
    
    


# print(ESClass.classes)

# for name, cls in ESClass.classes.items():
#     print(name)
#     for n, f in cls._functions.items():
#         print(f"{n}: {f}  {f.metadata}")







