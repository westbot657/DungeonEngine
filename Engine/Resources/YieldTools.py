# pylint: disable=W,R,C
from typing import Any

class YieldTools:
    
    class YieldSender:
        def __init__(self, source, target:str, data:Any):
            self.source = source
            self.target = target
            self.data = data
    
    class YieldResult:
        def __init__(self, target, value):
            self.target = target
            self.value = value

    def __init__(self, uid:str):
        self.uid = uid
        self._result = None

    def result(self):
        if self._result:
            return self._result.value
        return None

    def send(self, other_uid:str, data:Any):
        res = yield YieldTools.YieldSender(self, other_uid, data)
        if isinstance(res, YieldTools.YieldResult):
            self._result = res
        else:
            self._result = None

    def call(self, func, *args, **kwargs):
        ev = func(*args, **kwargs)
        v = None
        try:
            v = ev.send(None) # start the iterator
            while True:
                res = yield v # pass v down, and store any result
                v = ev.send(res) # pass result back up
        except StopIteration as e:
            if isinstance(e.value, YieldTools.YieldResult):
                v = e.value
            elif not isinstance(v, YieldTools.YieldResult):
                v = None
        
    def handle(self, ev):
        v = None
        try:
            v = ev.send(None) # start the iterator
            while True:
                res = yield v # pass v down, and store any result
                v = ev.send(res) # pass result back up
        except StopIteration as e:
            if isinstance(e.value, YieldTools.YieldResult):
                v = e.value
            elif not isinstance(v, YieldTools.YieldResult):
                v = None

"""
How this should look:


y = YieldTools("some_function")

...
yield from y.send("engine", {"function": "get_input", "prompt": "type_something"})
inp = y.result()

yield from y.call(some_other_func, *args, **kwargs)
ret = y.result()


"""



