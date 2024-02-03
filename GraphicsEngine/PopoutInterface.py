# pylint: disable=W,R,C


# this module is for sending commands between popout server/client
import json


class PopoutInterface:

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

    def target_component(self, comp:str):
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
            raise Exception("AMethod cannot start with \"__\"")

        self.current.update({str(self.sub_op): {"method": method_name}})
        self.sub_op += 1
        return self





    def end(self):
        if self.current:
            self.cmd_chain.update({self.op: self.current})
            self.op = 0
            self.sub_op = 0
            self.current = {}
        out = json.dumps(self.cmd_chain)
        self.cmd_chain = {}
        return out







