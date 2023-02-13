# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
except ImportError:
    from EngineDummy import Engine


class DynamicValue:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.cached_value = None
    def getNew(self, engine:Engine):
        """
        returns the result of passing this value's raw_data to `DungeonLoader.evaluateFunction()`
        """
        self.cached_value = engine.loader.evaluateFunction(engine, self.raw_data, None)
        return self.cached_value
    def getCached(self, engine:Engine):
        """
        returns the same value as the most recent call to `getNew()`.
        If no prior call to `getNew()` has been made, returns None
        """
        return self.cached_value
    def getCachedNew(self, engine:Engine):
        """
        returns the cached value.
        if the cached value is None, makes a call to `getNew()` first.
        """
        if self.cached_value is None:
            return self.getNew(engine)
        return self.cached_value