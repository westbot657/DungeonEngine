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
        self.current: dict = {}
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

    def call(self):
        self.current.update({str(self.sub_op): "call"})
        self.sub_op += 1
        return self

    def return_result(self):
        self.current.update({str(self.sub_op): "return"})
        self.sub_op += 1
        return self

    def event(self, event_type:Event):#, linked_object:str|None=None):
        if self.current:
            self.cmd_chain.update({self.op: self.current})
            self.op += 1
            self.sub_op = 0
            self.current = {}
        
        self.current.update({"event": event_type.value})
        # if linked_object:
        #     self.current.update({"link-to": linked_object})
        return self

    def end(self) -> str:
        if self.current:
            self.cmd_chain.update({str(self.op): self.current})
        self.op = 0
        self.sub_op = 0
        self.current = {}
        out = json.dumps({"interface-cmd": self.cmd_chain})
        self.cmd_chain = {}
        return out

    def clone(self):
        chain = merge({}, self.cmd_chain)

        interface = PopoutInterface()
        interface.cmd_chain = chain
        interface.op = self.op
        interface.sub_op = self.sub_op

        return interface

    @classmethod
    def execute(cls, cmd_chain:dict, components:dict, popout) -> list:
        """Takes a command chain and executes it.
        Returns a list of values to be returned to the main process
        """
        rets = []
        curr = None

        func = None
        args = []
        kwargs = {}
        event = None
        for op, command in cmd_chain.items():
            for key, cmd in command.items():
                if key == "target":
                    curr = components.get(cmd)
                elif key == "event":
                    event = cmd
                    # func = None
                    args = []
                    kwargs = {}
                else:
                    if isinstance(cmd, str):
                        if cmd == "return":
                            rets.append(curr)
                        if cmd == "call":
                            if event:
                                
                                def listener():
                                    popout.send(json.dumps({f"event-return-{event}": func(*args, **kwargs)})) # pylint: disable=not-callable
                                
                                components["editor"].add_event_listener(event,
                                    listener
                                )
                                event = None
                            else:
                                curr = func(*args, **kwargs) # pylint: disable=not-callable
                            func = None
                            args = []
                            kwargs = {}
                    else:
                        for k, v in cmd.items():
                            match k:
                                case "attr":
                                    if v.startswith("__"):
                                        raise ValueError("Attr cannot start with '__'")
                                    if hasattr(curr, v):
                                        curr = getattr(curr, v)
                                    else:
                                        raise ValueError(f"No attribute '{v}'")
                                case "method":
                                    if v.startswith("__"):
                                        raise ValueError("Attr cannot start with '__'")
                                    if hasattr(curr, v):
                                        curr = func = getattr(curr, v)
                                        args = []
                                        kwargs = {}
                                    else:
                                        raise ValueError(f"No attribute '{v}'")
                                case "param":
                                    if not func:
                                        raise ValueError("Param calls must happen after a method call")
                                    args.append(v)
                                case "ref-param":
                                    if not func:
                                        raise ValueError("Ref-param calls must happen after a method call")
                                    dat = v.split(".")
                                    c = dat[0]
                                    while dat:
                                        _c = dat.pop(0)
                                        if c.startswith("__"):
                                            raise ValueError("Attr/Method cannot start with '__'")
                                        if hasattr(c, _c):
                                            c = getattr(c, _c)
                                        else:
                                            raise ValueError(f"No attribute '{_c}'")
                                    args.append(c)
                                case "kwarg":
                                    if not func:
                                        raise ValueError("Param calls must happen after a method call")
                                    kwargs.update(v)
                                case "ref-kwarg":
                                    if not func:
                                        raise ValueError("Ref-param calls must happen after a method call")
                                    dat = v.values()[0].split(".")
                                    c = dat[0]
                                    while dat:
                                        _c = dat.pop(0)
                                        if c.startswith("__"):
                                            raise ValueError("Attr/Method cannot start with '__'")
                                        if hasattr(c, _c):
                                            c = getattr(c, _c)
                                        else:
                                            raise ValueError(f"No attribute '{_c}'")
                                    args.append({v.keys()[0]: c})
                            






