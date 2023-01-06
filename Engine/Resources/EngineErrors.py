# pylint: disable=[W,R,C,import-error]

class InvalidObjectError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

