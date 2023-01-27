# pylint: disable=[W,R,C,import-error]

class EngineError(Exception): pass

class InvalidObjectError(EngineError):
    def __init__(self, *args):
        super().__init__("InvalidObjectError:", *args)

class FunctionCallError(EngineError): # Error when function can't be called
    def __init__(self, *args):
        super().__init__("FunctionCallError:", *args)

class FunctionLoadError(EngineError): # Error when function can't load/can't be found
    def __init__(self, *args):
        super().__init__("FunctionLoadError:", *args)

class FunctionRunError(EngineError): # Error with code within a function
    def __init__(self, *args):
        super().__init__("FunctionRunError:", *args)

class MemoryError(EngineError): # Error with FunctionMemory
    def __init__(self, *args):
        super().__init__("MemoryLoadError:", *args)

class IdentifierError(EngineError):
    def __init__(self, *args):
        super().__init__("IdentifierError:", *args)


