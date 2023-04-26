# pylint: disable=[W,R,C,import-error]

try:
    from .EngineDummy import Engine
    from .Logger import Log
    from .EngineOperation import EngineOperation, _EngineOperation
except:
    from EngineDummy import Engine
    from Logger import Log
    from EngineOperation import EngineOperation, _EngineOperation


from enum import Enum, auto
from typing import Any, Generator

import re

class TextPattern:

    # TODO:
    # convert to generators:
    # handleInput()
    # check()
    #
    # treat eval_method as generator or function

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
    def handleInput(cls, function_memory, player, text:str):
        for pattern in cls._patterns:
            pattern: TextPattern

            ev = pattern.check(function_memory, player, text)
            matched = False
            v = None
            try:
                matched, v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    matched, v = ev.send(res)
            except StopIteration as e:
                #if isinstance(e.value, _EngineOperation): print("\n\n\n1: Engine Operation\n\n\n")
                if isinstance(e.value, (tuple, list)):
                    v = tuple(e.value)[1]
            ret = v
            # if matched: return True, v
            # return False, None


            #matched, ret = pattern.check(function_memory, player, text)
            if matched:
                if isinstance(ret, (EngineOperation, _EngineOperation)):
                    return ret
                elif isinstance(ret, Generator):
                    v = None
                    try:
                        v = ret.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield v
                            v = ret.send(res)
                    except StopIteration as e:
                        #if isinstance(e.value, _EngineOperation): print("\n\n\n2: Engine Operation\n\n\n")
                        v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                    return v
            
        return EngineOperation.Continue(ret)

    def check(self, function_memory, player, text:str) -> tuple[bool, Any]:
        if self.check_type == TextPattern.CheckType.MATCH:
            # Log["debug"]["text pattern"]("match-type")
            # Log["debug"]["text pattern"](f"regex: r'{self.regex}'")
            # Log["debug"]["text pattern"](f"text: '{text}'")
            if m := re.match(self.regex, text):

                ev = self.eval_method(function_memory, player, text, m.groupdict())

                if isinstance(ev, Generator):
                    v = None
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield True, v
                            v = ev.send(res)
                    except StopIteration as e:
                        v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                    return True, v
                else:
                    return True, ev

                #return True, self.eval_method(function_memory, player, text, m.groupdict())

        elif self.check_type == TextPattern.CheckType.SEARCH:
            # Log["debug"]["text pattern"]("search-type")
            # Log["debug"]["text pattern"](f"regex: r'{self.regex}'")
            # Log["debug"]["text pattern"](f"text: '{text}'")
            if m := re.search(self.regex, text):

                ev = self.eval_method(function_memory, player, text, m.groupdict())

                if isinstance(ev, Generator):
                    v = None
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield True, v
                            v = ev.send(res)
                    except StopIteration as e:
                        v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                    return True, v
                else:
                    return True, ev
                
                #return True, self.eval_method(function_memory, player, text, m.groupdict())
                
        elif self.check_type == TextPattern.CheckType.FULLMATCH:
            # Log["debug"]["text pattern"]("fullmatch-type")
            # Log["debug"]["text pattern"](f"regex: r'{self.regex}'")
            # Log["debug"]["text pattern"](f"text: '{text}'")
            if m := re.fullmatch(self.regex, text):

                ev = self.eval_method(function_memory, player, text, m.groupdict())

                if isinstance(ev, Generator):
                    v = None
                    try:
                        v = ev.send(None)
                        while isinstance(v, _EngineOperation):
                            res = yield True, v
                            v = ev.send(res)
                    except StopIteration as e:
                        #if isinstance(e.value, _EngineOperation): print("\n\n\nEngine Operation\n\n\n")
                        v = e.value or (v if not isinstance(v, _EngineOperation) else None)
                    return True, v
                else:
                    return True, ev

                #return True, self.eval_method(function_memory, player, text, m.groupdict())
            
        return False, None

    @staticmethod
    def interpretAmount(amount:str, max_available:int=-1) -> int:
        if amount is None: return 1
        
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



