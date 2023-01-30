# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .EngineErrors import MemoryError
except ImportError:
    from EngineDummy import Engine
    from EngineErrors import MemoryError


class FunctionMemory:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.symbol_table = {}
        self.context_data = {}
    
    def prepFunction(self):
        self.symbol_table.clear()
        self.context_data.clear()

    def checkPredicate(self, engine:Engine, predicate:dict):
        ...

    def store(self, name:str, value):
        self.symbol_table.update({name, value})
        
    def ref(self, name:str):
        if name in self.symbol_table:
            return self.symbol_table[name]
        raise MemoryError(f"Variable referenced before assignment: '{name}'")

    def clear(self):
        self.symbol_table.clear()

    def update(self, data:dict):
        self.symbol_table.update(data)
    


