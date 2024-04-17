# pylint: disable=[W,R,C, import-error]

from .Serializable import Serializable

from typing import Any

import re

class Serializer:
    
    _serialized = [] # this is a list of object ids (from id()) to avoid double-serialization of an object
    _deserialized = {} # mapping of:   serialized obj id: deserialized obj
        
    @classmethod
    def serialize(cls, obj:Any) -> dict:
        
        if isinstance(obj, (int, float, str, bool, bytes)):
            return {"literal": obj}
        elif isinstance(obj, dict):
            serialized = []
            for k, v in obj.items():
                serialized.append((cls.serialize(k), cls.serialize(v)))
            return {"dict": serialized}
        elif isinstance(obj, list):
            return {"list": [cls.serialize(x) for x in obj]}
        elif isinstance(obj, tuple):
            return {"tuple": [cls.serialize(x) for x in obj]}
        elif Serializable.isSerealizable(obj):
            if id(obj) in cls._serialized:
                return {"serial-reference": id(obj)}
            else:
                cls._serialized.append(id(obj))
                return {f"serial-{Serializable.getId(obj)}-{id(obj)}": obj.serialize()}
        else:
            raise ValueError(f"Cannot serialize '{obj}'. Not marked as Serializable")
        
    @classmethod
    def deserialize(cls, obj:dict) -> Any:
        for k, v in obj.items(): # 'obj' should only ever have 1 key/value pair
            if k == "literal":
                return v
            elif k == "dict":
                deserialized = {}
                for key, val in v:
                    deserialized.update({cls.deserialize(key): cls.deserialize(val)})
                return deserialized
            elif k == "list":
                return [cls.deserialize(x) for x in v]
            elif k == "tuple":
                return tuple(cls.deserialize(x) for x in v)
            elif m := re.match(r"serial\-(?P<class_type>[^\-]+)\-(?P<object_id>.+)", k):
                d = m.groupdict()
                class_type = d["class_type"]
                object_id = int(d["object_id"])
                _class = Serializable._serializable[class_type]
                instance = object.__new__(_class)
                cls._deserialized.update({object_id: instance})
                _class.deserialize(instance, v)
            elif k == "serial-reference":
                return cls._deserialized[v]

    @classmethod
    def smartSerialize(cls, instance:object, *attrs) -> dict:
        out = {}
        for attr in attrs:
            out.update({attr: cls.serialize(getattr(instance, attr))})
        return out
    
    @classmethod
    def smartDeserialize(cls, instance:object, data:dict) -> None:
        for k, v in data.items():
            setattr(instance, k, cls.deserialize(v))

    @classmethod
    def clear_serialized_cache(cls):
        cls._serialized.clear()
        
    @classmethod
    def clear_deserialized_cache(cls):
        cls._deserialized.clear()
            
