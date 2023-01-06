# pylint: disable=[W,R,C,import-error]

class Item:

    def __init__(self, name:str, max_count:int, count:int, data:dict|None=None):
        self.name = name
        self.max_count = max_count
        self.count = count
        self.data = data or {}

    def __repr__(self):
        return f"Item {self.name}: max_count:{self.max_count} count:{self.count} data:{self.data}"

