# pylint: disable=W,R,C


class Data:
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        if isinstance(self.data, bool):
            return f"B:{1 if self.data else 0}"
        elif isinstance(self.data, (int, float)):
            return f"N:{self.data}"
        elif isinstance(self.data, str):
            return f"S:{self.data!r}"
        

class Instruction:
    def __init__(self):
        ...

    def assemble(self):
        raise Exception(f"assemble() not implemented for {self}")

class GetInputI(Instruction):
    def __init__(self, store_to, prompt, user):
        self.store_to = store_to
        self.prompt = prompt
        self.user = user
    
    def assemble(self):
        return f"INPUT {self.store_to} {self.user} {self.prompt!r}"

class BinOpI(Instruction):
    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right

    def assemble(self):
        return f"OP {self.op} {self.left} {self.right}"

class StoreI(Instruction):
    def __init__(self, store_to, value):
        self.store_to = store_to
        self.value = value
    
    def assemble(self):
        return f"STORE {self.store_to} {self.value}"

class PushStackI(Instruction):
    def __init__(self):
        pass

    def assemble(self):
        return "PUSHSTACK"

class PopStackI(Instruction):
    def __init__(self): pass
    
    def assemble(self):
        return "POPSTACK"

class OutputI(Instruction):
    def __init__(self, out):
        self.out = out
    
    def assemble(self):
        return f"OUT {self.out}"

class PrepArgsI(Instruction):
    def __init__(self): pass
    
    def assemble(self):
        return "PREPARGS"

class LoadI(Instruction):
    def __init__(self, load_val, load_to):
        self.load_val = load_val
        self.load_to = load_to
    
    def assemble(self):
        return f"LOAD {self.load_to} {self.load_val}"


