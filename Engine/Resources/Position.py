# pylint: disable=[W,R,C,import-error]




class Position:

    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    
    def _get_save(self, function_memory):
        return [self.x, self.y]