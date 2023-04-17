# pylint: disable=[W,R,C,import-error]

try:
    from .Location import Location
    from .Identifier import Identifier
    from .EngineErrors import IdentifierError
except ImportError:
    from Location import Location
    from Identifier import Identifier
    from EngineErrors import IdentifierError


class AbstractInteractable:
    _interaction_types = {}
    
    def __init__(self, data:dict):
        self._raw_data = data


    

