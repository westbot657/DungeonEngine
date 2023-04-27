# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionalElement import FunctionalElement
except ImportError:
    from FunctionalElement import FunctionalElement

class Room(FunctionalElement):
    def __init__(self, abstract):
        self.abstract = abstract
        ...
