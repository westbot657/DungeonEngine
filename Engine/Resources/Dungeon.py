# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionalElement import FunctionalElement
except ImportError:
    from FunctionalElement import FunctionalElement


class Dungeon(FunctionalElement):

    def __init__(self, abstract):
        self.abstract = abstract
        ...

    def _input_handler(self, player_id, text:str):
        ...


