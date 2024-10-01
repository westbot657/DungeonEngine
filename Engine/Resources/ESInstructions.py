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

class Register:
    _id = 0
    def __init__(self, id):
        self.id = id
    
    def __repr__(self):
        return f"R:{self.id}"
    
    @classmethod
    def new(cls):
        r = cls(cls._id)
        cls._id += 1
        return r

class MemoryObject:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"M:{self.name}"

class Instruction:
    def __init__(self):
        self.line_number = -1

    def assemble(self, line_number):
        raise Exception(f"assemble() not implemented for {self}")

class GetInputI(Instruction):
    def __init__(self, store_to, prompt, user):
        self.store_to = store_to
        self.prompt = prompt
        self.user = user
    
    def assemble(self, line_number):
        return f"INPUT {self.store_to} {self.user} {self.prompt!r}"

class BinOpI(Instruction):
    def __init__(self, store_to, left, op, right):
        self.store_to = store_to
        self.op = op
        self.left = left
        self.right = right
        self.line_number = -1

    def assemble(self, line_number):
        self.line_number = line_number
        return f"OP {self.store_to} {self.left} {self.op} {self.right}"

class StoreI(Instruction):
    def __init__(self, store_to, value):
        self.store_to = store_to
        self.value = value
        self.line_number = -1

    def assemble(self, line_number):
        self.line_number = line_number
        return f"STORE {self.store_to} {self.value}"

# class PushStackI(Instruction):
#     def __init__(self):
#         self.line_number = -1

#     def assemble(self, line_number):
#         self.line_number = line_number
#         return "PUSHSTACK"

# class PopStackI(Instruction):
#     def __init__(self):
#         self.line_number = -1

#     def assemble(self, line_number):
#         self.line_number = line_number
#         return "POPSTACK"

class OutputI(Instruction):
    def __init__(self, out):
        self.out = out
        self.line_number = -1

    def assemble(self, line_number):
        self.line_number = line_number
        return f"OUT {self.out}"

class PrepArgsI(Instruction):
    def __init__(self):
        self.line_number = -1

    def assemble(self, line_number):
        self.line_number = line_number
        return "PREPARGS"

class SetArgI(Instruction):
    def __init__(self, arg_name, value):
        self.line_number = -1
        self.arg_name = arg_name
        self.value = value
    
    def assemble(self, line_number):
        self.line_number = line_number
        return f"SETARG {self.arg_name} {self.value}"

class CallI(Instruction):
    def __init__(self, call_to):
        self.line_number = -1
        self.call_to = call_to
    
    def assemble(self, line_number):
        self.line_number = line_number
        return f"CALL {self.call_to}"

class GotoI(Instruction):
    def __init__(self, target:Instruction):
        self.target = target
        while isinstance(self.target, GotoI):
            self.target = self.target.target
        self.line_number = -1

    def assemble(self, line_number):
        self.line_number = line_number
        if (self.target.line_number != -1):
            return f"GOTO {self.target.line_number}"
        return self

class LoadI(Instruction):
    def __init__(self, load_val, load_to):
        self.load_val = load_val
        self.load_to = load_to
        self.line_number = -1

    def assemble(self, line_number):
        self.line_number = line_number
        return f"LOAD {self.load_to} {self.load_val}"

class NewI(Instruction):
    def __init__(self, store_to, object_type):
        self.store_to = store_to
        self.object_type = object_type
        self.line_number = -1
    
    def assemble(self, line_number):
        self.line_number = line_number
        return f"NEW {self.store_to} {self.object_type}"

class WaitI(Instruction):
    def __init__(self, duration):
        self.duration = duration
        self.line_number = -1
    
    def assemble(self, line_number):
        self.line_number = line_number
        return f"WAIT {self.duration}"

class MoveI(Instruction):
    def __init__(self, entity, destination):
        self.entity = entity
        self.destination = destination
        self.line_number = -1
    
    def assemble(self, line_number):
        self.line_number = line_number
        return f"MOVE {self.entity} {self.destination}"

class ReferenceI(Instruction):
    def __init__(self, var_name, parent):
        self.line_number = -1
        self.var_name = var_name
        self.parent = parent
    
    def assemble(self, line_number):
        self.line_number = line_number
        return f"REF {self.parent} {self.var_name}"
