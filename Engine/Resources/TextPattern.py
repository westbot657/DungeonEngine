# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .Logger import Log
except:
    from EngineDummy import Engine
    from Logger import Log

from enum import Enum, auto
from typing import Any

import re

class TextPattern:

    class CheckType(Enum):
        MATCH = auto()
        SEARCH = auto()
        FULLMATCH = auto()

    _patterns = []
    def __init__(self, regex, check_type=CheckType.SEARCH):
        """
        regex: the regular expression player input is checked against.
        if the pattern is matched, the decorated function is called,
        passing the engine, player, raw text, and the regex groupdict()
        """
        self.check_type = check_type
        self.regex = regex
        TextPattern._patterns.append(self)
    
    def __call__(self, eval_method):
        self.eval_method = eval_method
    
    @classmethod
    def handleInput(cls, engine:Engine, player, text:str):
        for pattern in cls._patterns:
            matched, ret = pattern.check(engine, player, text)
            if matched:
                return ret

    def check(self, engine:Engine, player, text:str) -> tuple[bool, Any]:
        if self.check_type == TextPattern.CheckType.MATCH:
            # Log["debug"]["text pattern"]("match-type")
            # Log["debug"]["text pattern"](f"regex: r'{self.regex}'")
            # Log["debug"]["text pattern"](f"text: '{text}'")
            if m := re.match(self.regex, text):
                return True, self.eval_method(engine, player, text, m.groupdict())

        elif self.check_type == TextPattern.CheckType.SEARCH:
            # Log["debug"]["text pattern"]("search-type")
            # Log["debug"]["text pattern"](f"regex: r'{self.regex}'")
            # Log["debug"]["text pattern"](f"text: '{text}'")
            if m := re.search(self.regex, text):
                return True, self.eval_method(engine, player, text, m.groupdict())
                
        elif self.check_type == TextPattern.CheckType.FULLMATCH:
            # Log["debug"]["text pattern"]("fullmatch-type")
            # Log["debug"]["text pattern"](f"regex: r'{self.regex}'")
            # Log["debug"]["text pattern"](f"text: '{text}'")
            if m := re.fullmatch(self.regex, text):
                return True, self.eval_method(engine, player, text, m.groupdict())
            
        return False, None

    @staticmethod
    def interpretAmount(amount:str, max_available:int=-1) -> int:
        if amount.isnumeric():
            return int(amount)

        elif re.search(r"\b(all|every)\b", amount):
            return max_available

        elif re.search(r"\b(half|1/2)\b", amount):
            return int(max_available/2)

        elif re.search(r"\b(an?|the|some)\b", amount): # this has to go last, as it tries to find "a" as a valid match
            return 1

        else:
            return 1



