# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .FunctionMemory import FunctionMemory
    from .EngineOperation import _EngineOperation
    from .FunctionalElement import FunctionalElement
except ImportError:
    from EngineDummy import Engine
    from FunctionMemory import FunctionMemory
    from EngineOperation import _EngineOperation
    from FunctionalElement import FunctionalElement


class DynamicValue(FunctionalElement):

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.cached_value = None

    def getLocalVariables(self):
        return {
            ".value": self.cached_value
        }

    def updateLocalVariables(self, locals: dict):
        ...
    
    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.addContextData({
            "#dynamic_value": self
        })
        function_memory.update(self.getLocalVariables())
    
    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

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
            self.getNew(function_memory)
            
        return self.cached_value

    def quickDisplay(self, function_memory:FunctionMemory):
        if not isinstance(self.raw_data, dict):
            return str(self.raw_data)
        return function_memory.engine.loader.loader_function.quickDisplay(function_memory, self.raw_data)
        

    def fullDisplay(self, function_memory:FunctionMemory):
        if not isinstance(self.raw_data, dict):
            return str(self.raw_data)
        return function_memory.engine.loader.loader_function.fullDisplay(function_memory, self.raw_data)

