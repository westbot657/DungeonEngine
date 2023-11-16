# pylint: disable=[W,R,C,no-member]

import opendal, orjson, json


class Loader:
    op = opendal.Operator("fs", root="./")
    
    @classmethod
    def load(cls, filename):
        # with open(filename, "r+", encoding="utf-8") as f:
        #     d = json.load(f)
        # return d
        return orjson.loads(cls.op.read(filename))

    @classmethod
    def read(cls, filename):
        # with open(filename, "r+", encoding="utf-8") as f:
        #     d = f.read()
        # return d
        return cls.op.read(filename).decode()


