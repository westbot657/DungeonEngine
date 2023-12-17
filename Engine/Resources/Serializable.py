# pylint: disable=[W,R,C]



class Serializable:
    """
    Decorator for all classes that need to be
    (de)serializable for socket server communication
    
    all decorated classes MUST implement:
    `serialize() -> dict`
    
    `(classmethod/staticmethod) deserialize(instance, serialized:dict) -> None` # `instance` is a blank instance of YOUR class

    """
    
    _serializable = {}
    

    def __init__(self, serialization_id):
        self.serialization_id = serialization_id
        
    def __call__(self, serializable_class):
        if not hasattr(serializable_class, "serialize"):
            raise NotImplementedError(f"serialize() method not implemented by {serializable_class}")
        
        if not hasattr(serializable_class, "deserialize"):
            raise NotImplementedError(f"deserialize() method not implemented by {serializable_class}")
        
        else:
            Serializable._serializable.update({self.serialization_id: serializable_class})
        
        return serializable_class

    @classmethod
    def isSerealizable(cls, obj):
        return obj.__class__ in tuple(cls._serializable.values())
    
    @classmethod
    def getId(cls, obj):
        for k, v in cls._serializable.items():
            if obj.__class__ == v:
                return k
        raise ValueError(f"Cannot find serialization id for '{obj}'")


