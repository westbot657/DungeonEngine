# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .FunctionMemory import FunctionMemory
except ImportError:
    from EngineDummy import Engine
    from FunctionMemory import FunctionMemory


class DynamicValue:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.cached_value = None
    def getNew(self, function_memory:FunctionMemory):
        """
        returns the result of passing this value's raw_data to `DungeonLoader.evaluateFunction()`
        """
        if isinstance(self.raw_data, dict):
            self.cached_value = function_memory.evaluateFunction(self.raw_data)
        else:
            self.cached_value = self.raw_data
            
        return self.cached_value
    def getCached(self, function_memory:FunctionMemory):
        """
        returns the same value as the most recent call to `getNew()`.
        If no prior call to `getNew()` has been made, returns None
        """
        return self.cached_value
    def getCachedOrNew(self, function_memory:FunctionMemory):
        """
        returns the cached value.
        if the cached value is None, makes a call to `getNew()` first.
        """
        if self.cached_value is None:
            return self.getNew(function_memory)
        return self.cached_value

    def quickDisplay(self, engine:Engine):
        if not isinstance(self.raw_data, dict):
            return str(self.raw_data)
        return engine.loader.loader_function.quickDisplay(engine, self.raw_data)
        

    def fullDisplay(self, engine:Engine):
        if not isinstance(self.raw_data, dict):
            return str(self.raw_data)
        return engine.loader.loader_function.fullDisplay(engine, self.raw_data)

