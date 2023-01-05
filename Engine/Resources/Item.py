# pylint: disable=[W,R,C,import-error]

class Item:

    def __new__(cls, data:dict):
        self = super().__new__(cls)

        self.name = data.get("name", None)
        self.max_count = data.get("max_count", None)
        self.count = data.get("count", self.max_count)
        self.parent = data.get("parent", None)


        return self


