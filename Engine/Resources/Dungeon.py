# pylint: disable=[W,R,C,import-error]

try:
    from .FunctionalElement import FunctionalElement
    from .FunctionMemory import FunctionMemory
except ImportError:
    from FunctionalElement import FunctionalElement
    from FunctionMemory import FunctionMemory

import json

class Dungeon(FunctionalElement):

    def __init__(self, abstract):
        self.abstract = abstract
        ...

    def loadSaveData(self, function_memory:FunctionMemory):
        ...

    def _input_handler(self, player_id, text:str):
        ...


