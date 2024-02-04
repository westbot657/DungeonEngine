# pylint: disable=W,R,C


# this module is for sending commands between popout server/client
import json

from enum import Enum, auto
from mergedeep import merge


class PopoutInterface:

    class Event(Enum):
        WINDOW_CLOSED = "WINDOW_CLOSED"

        

    def __init__(self):
        self.cmd_chain: dict = {}
        self.current: dict = self.cmd_chain
        self.op = 0
        self.sub_op = 0

    def cmd(self):
        if self.current:
            self.cmd_chain.update({self.op: self.current})
            self.op += 1
            self.sub_op = 0
            self.current = {}

        return self

    def component(self, comp:str):
        self.current.update({"target": comp})
        self.sub_op = 0

        return self

    def attr(self, attr_name:str):
        if attr_name.startswith("__"):
            raise Exception("Attr cannot start with \"__\"")

        self.current.update({str(self.sub_op): {"attr": attr_name}})
        self.sub_op += 1
        return self

    def method(self, method_name:str):
        if method_name.startswith("__"):
            raise Exception("Method cannot start with \"__\"")

        self.current.update({str(self.sub_op): {"method": method_name}})
        self.sub_op += 1
        return self

    def param(self, val):
        self.current.update({str(self.sub_op): {"param": val}})
        self.sub_op += 1
        return self

    def ref_param(self, ref:str):
        self.current.update({str(self.sub_op): {"ref-param": ref}})
        self.sub_op += 1
        return self

    def kwarg(self, name, val):
        self.current.update({str(self.sub_op): {"kwarg": {name: val}}})
        self.sub_op += 1
        return self
    
    def ref_kwarg(self, name, ref):
        self.current.update({str(self.sub_op): {"ref-kwarg": {name: ref}}})
        self.sub_op += 1
        return self

    def return_result(self):
        self.current.update({str(self.sub_op): "return"})
        self.sub_op += 1
        return self

    def event(self, event_type:Event, linked_object:str|None=None):
        if self.current:
            self.cmd_chain.update({self.op: self.current})
            self.op += 1
            self.sub_op = 0
            self.current = {}
        
        self.current.update({"event": event_type.value})
        if linked_object:
            self.current.update({"link-to": linked_object})
        return self

    def end(self) -> str:
        if self.current:
            self.cmd_chain.update({str(self.op): self.current})
        self.op = 0
        self.sub_op = 0
        self.current = {}
        out = json.dumps(self.cmd_chain)
        self.cmd_chain = {}
        return out

    @classmethod
    def execute(cls, cmd_chain:dict, components:dict, editor):
        
        for op, cmd in cmd_chain.items():
            ...

    def clone(self):
        chain = merge({}, self.cmd_chain)

        interface = PopoutInterface()
        interface.cmd_chain = chain
        interface.op = self.op
        interface.sub_op = self.sub_op

        return interface





