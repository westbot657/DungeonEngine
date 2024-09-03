# pylint: disable=W,R,C,import-error

from typing import Callable


class DataType:
    def __init__(self):
        self.attrs = {}

class CallableType(DataType):
    def __init__(self, retTypes):
        self.retTypes = retTypes

class NullType(DataType):
    _instance = None
    
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.attrs = {}

class StringType(DataType):
    _instance = None
    
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        self.attrs = {
            "split": CallableType(ListType(self)),
            "rsplit": CallableType(ListType(self)),
            "format": CallableType(self),
            "join": CallableType(self),
            "capitalize": CallableType(self),
            "upper": CallableType(self),
            "lower": CallableType(self),
            "length": CallableType(IntType()),
            "find": CallableType(IntType()),
            "rfind": CallableType(IntType()),
            "startswith": CallableType(BoolType()),
            "endswith": CallableType(BoolType()),
            "removeprefix": CallableType(self),
            "removesuffix": CallableType(self),
            "title": CallableType(self)
        }

class IntType(DataType):
    _instance = None
    
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        self.attrs = {}
        
class FloatType(DataType):
    _instance = None
    
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        self.attrs = {}

class BoolType(DataType):
    _instance = None
    
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        self.attrs = {}


class ListType(DataType):
    def __init__(self, valueTypes):
        self.valueTypes = valueTypes
        self.attrs = {
            "get": CallableType(valueTypes),
            "append": CallableType(NullType()),
            "insert": CallableType(NullType()),
            "index": CallableType([IntType(), NullType()]),
            "contains": CallableType(BoolType()),
            "clear": CallableType(NullType()),
            "length": CallableType(IntType()),
            "pop": CallableType(valueTypes),
            "remove": CallableType(NullType()),
            "copy": CallableType(lambda: ListType(valueTypes)), # this can't immediately call otherwise it will call recursively forever
            "sort": CallableType(NullType()),
            "reverse": CallableType(NullType())
        }

class MapType(DataType):
    def __init__(self, keyTypes, valueTypes):
        self.keyTypes = keyTypes
        self.valueTypes = valueTypes
        self.attrs = {
            "keys": CallableType(keyTypes),
            "values": CallableType(valueTypes),
            "items": CallableType(lambda: ListType([keyTypes, valueTypes])),
            "containsKey": CallableType(BoolType()),
            "containsValue": CallableType(BoolType()),
            "get": CallableType(valueTypes),
            "update": CallableType(NullType()),
            "pop": CallableType(valueTypes),
            "copy": CallableType(lambda: MapType(keyTypes, valueTypes))
        }

class MacroStackType(DataType):
    def __init__(self, compiler:Callable):
        self.compiler = compiler
    
    def compile(self, tokens):
        return self.compiler(tokens)

class PlayerType(DataType):
    
    @staticmethod
    def tag_compiler(tokens):
        ...
    
    def __init__(self):
        self.attrs = {
            "tag": MacroStackType(self.tag_compiler),
            "give_money": CallableType(NullType())
        }

class DungeonType(DataType):
    def __init__(self):
        ...


class Globals:
    def __init__(self):
        self.attrs = {
            "wait": CallableType(NullType()),
            "output": CallableType(NullType()),
            "format": CallableType(StringType()),
            "random": ...
        }


class TypeHelper:
    
    @classmethod
    def typesHaveAttr(cls, types:DataType|list[DataType], attr:str):
        if isinstance(types, list): # ALL types must have `attr` for this to return true
            return all(
                (attr in list(t.attrs.keys())) for t in types # change this to get types from CallableType
            )
        else:
            return attr in list(types.attrs.keys())

