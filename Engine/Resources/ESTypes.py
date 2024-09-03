# pylint: disable=W,R,C,import-error

from typing import Callable

class CompileError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
    def __repr__(self):
        return f"CompileError: {"".join(self.args)}"

class DataType:
    def __init__(self):
        self.attrs = {}
    
    def getAttrs(self) -> dict:
        return self.attrs
    
    def called(self):
        raise CompileError("object cannot be called")

class CallableType(DataType):
    def __init__(self, retTypes):
        self.retTypes = retTypes
    
    def getAttrs(self):
        attrs = {}
        for tp in self.retTypes:
            tp: DataType
            tp_attrs = tp.getAttrs()
            for k, v in tp_attrs.items():
                if k in attrs:
                    _v = attrs[k]
                    if not isinstance(_v, list):
                        _v = [_v]
                    _v.append(v)
                    attrs.update({k: _v})
                else:
                    attrs.update({k: v})
        return attrs

    def called(self):
        return self.getAttrs()

class UnknownType(DataType):
    _instance = None
    
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        self.attrs = self

    def __getitem__(self, idx):
        return self
    
    def getAttrs(self) -> dict:
        return self

    def update(self, *_):
        pass
    
    def get(self, *_):
        return self

    def keys(self):
        return []

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
    
    def compile(self, es3, ref, tokens):
        return self.compiler(es3, ref, tokens)

class RandomClassType(DataType):
    _instance = None
    
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        self.attrs = {
            "choice": CallableType(UnknownType()),
            "range": CallableType(IntType())
        }

class CurrencyType(DataType):
    def __init__(self):
        self.attrs = {
            "gold": IntType(),
            "silver": IntType(),
            "copper": IntType(),
            "to_string": CallableType(StringType())
        }

class PlayerType(DataType):
    
    @staticmethod
    def tag_compiler(es3, compiled_reference, tokens:list):
        if len(tokens) >= 3:
            t1 = tokens.pop(0)
            t2 = tokens.pop(0)
            if t1.type == "WORD" and t2 == ("LITERAL", "="):
                value = es3.expression(tokens)
                return {
                    "#set_player_tag": t1.value,
                    "of_player": compiled_reference,
                    "with_value": value.compile()
                }
            else:
                raise CompileError(f"tag macro expected pattern: WORD '=' expression. received pattern: ({t1}) ({t2}) ...")
            
        elif len(tokens) == 1:
            t = tokens[0]
            if t.type != "WORD":
                raise CompileError(f"tag macro expected a WORD token. received token type: {t.type}")
            return {
                "#get_player_tag": t.value,
                "from": compiled_reference
            }
        else:
            raise CompileError(f"tag macro only takes 1 or 3+ tokens. received {len(tokens)} tokens")
    
    def __init__(self):
        self.attrs = {
            "tag": MacroStackType(self.tag_compiler),
            "give_money": CallableType(NullType())
        }

class DungeonType(DataType):
    def __init__(self):
        self.attrs = {
            "player_ids": ListType(IntType())
        }


class Globals:
    attrs = {
        "wait": CallableType(NullType()),
        "output": CallableType(NullType()),
        "format": CallableType(StringType()),
        "random": RandomClassType()
    }


class TypeHelper:
    
    @classmethod
    def typesHaveAttr(cls, types:DataType|list[DataType], attr:str):
        if isinstance(types, UnknownType):
            return False
        if isinstance(types, list): # ALL types must have `attr` for this to return true
            return all(
                (attr in list(t.getAttrs().keys())) for t in types
            )
        return attr in list(types.getAttrs().keys())

    @classmethod
    def getAttrType(cls, base_type:DataType, attr:str):
        if isinstance(base_type, list):
            return cls.getAttrType(base_type[0], attr)
        if attr in base_type.getAttrs().keys():
            tp = base_type.getAttrs().get(attr)
            if isinstance(tp, Callable): # process lambda
                tp = tp()
            return tp
