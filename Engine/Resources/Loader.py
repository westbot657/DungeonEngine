# pylint: disable=[W,R,C,no-member]

import opendal, orjson


class Loader:
    op = opendal.Operator("fs", root="./")
    
    @classmethod
    def load(cls, filename):
        return orjson.loads(cls.op.read(filename))

    @classmethod
    def read(cls, filename):
        return cls.op.read(filename).decode()


