# pylint: disable=[W,R,C,import-error]


class LoaderFunction:
    _functions = {}

    def __init__(self, symbol_table:dict|None=None):
        # use instances to store variables used in chained functions
        self.symbol_table = symbol_table





