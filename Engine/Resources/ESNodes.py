# pylint: disable=[W,R,C]


try:
    from .EngineErrors import ScriptError, FinalScriptError, EOF
    from .Serializer import Serializer
    from .YieldTools import YieldTools
    # from .LoaderFunction import LoaderFunction
    from .ESFunctions import ESFunction, ESClass
except ImportError:
    from EngineErrors import ScriptError, FinalScriptError, EOF
    from Serializer import Serializer
    from YieldTools import YieldTools
    from ESFunctions import ESFunction, ESClass
    # from LoaderFunction import LoaderFunction
    

class Node:
    def compile(self):
        return {}

    def display(self, depth:int=0) -> str:
        return f"{" "*depth*2}{self}"


class Statements(Node):
    def __init__(self, nodes:list[Node]):
        self.nodes = nodes
    
    def compile(self):
        return {
            "#functions": [node.compile() for node in self.nodes]
        }

    def display(self, depth=0):
        out = [f"{" "*depth*2}Statements("]
        
        for node in self.nodes:
            out.append(node.display(depth+1))
        
        out.append(f"{" "*depth*2})")
        return "\n".join(out)


class Comp(Node):
    def __init__(self, left:Node, op:str, right:Node):
        self.left = left
        self.op = op
        self.right = right
    
    def compile(self):
        return {
            "#function": "math.compare",
            self.op: [
                self.left.compile(),
                self.right.compile()
            ]
        }

    def display(self, depth:int=0) -> str:
        return f"{" "*depth*2}Comp [ {self.op} ] (\n{self.left.display(depth+1)}\n{self.right.display(depth+1)}\n{" "*depth*2})"


class IfStatement(Node):
    def __init__(self, condition:Node, body:Node, else_node:Node=None):
        self.condition = condition
        self.body = body
        self.else_node = else_node
    
    def compile(self):
        return {
            "#check": self.condition.compile(),
            "true": self.body.compile(),
            "false": self.else_node.compile() if self.else_node else None
        }

    def display(self, depth:int=0):
        return f"{" "*depth*2}IfStatement(\n{" "*depth*2}  condition [\n{self.condition.display(depth+2)}\n{" "*depth*2}  ] true {{\n{self.body.display(depth+2)}\n{" "*depth*2}  }} false {{\n{self.else_node.display(depth+1) if self.else_node else f"{" "*depth*2}    [no else branch]"}\n{" "*depth*2}  }}\n{" "*depth*2})"


class ForLoopC(Node):
    def __init__(self, initializer, step, end_condition, body):
        self.initializer = initializer
        self.step = step
        self.end_condition = end_condition
        self.body = body
    
    def compile(self):
        return {
            "#for": "C-type",
            "init": self.initializer.compile(),
            "step": self.step.compile(),
            "stop": self.end_condition.compile(),
            "body": self.body.compile()
        }


class ForLoopPy(Node):
    def __init__(self, unpack, iterable, body):
        self.unpack = unpack
        self.iterable = iterable
        self.body = body
    
    def compile(self):
        return {
            "#for": "Py-type",
            "unpack": self.unpack.compile(),
            "iter": self.iterable.compile(),
            "body": self.body.compile()
        }


class WhileLoop(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def compile(self):
        return {
            "#while": self.condition.compile(),
            "body": self.body.compile()
        }


class MatchCase(Node):
    def __init__(self, match_value:Node, cases:list[Node], bodies:list[Node]):
        self.match_value = match_value
        self.cases = cases
        self.bodies = bodies
    
    def compile(self):
        pass

    def display(self, depth: int = 0) -> str:
        out = [f"{" "*depth*2}MatchCase ["]
        out.append(self.match_value.display(depth+1))
        out.append(f"{" "*depth*2}] {{")
        
        for case, body in zip(self.cases, self.bodies):
            out.append(f"{" "*depth*2}  case [")
            out.append(case.display(depth+2))
            out.append(f"{" "*depth*2}  ] {{")
            out.append(body.display(depth+2))
            out.append(f"{" "*depth*2}  }}")

        return "\n".join(out)

class ClassDef(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class BinaryOp(Node):
    def __init__(self, left:Node, op, right:Node):
        self.left = left
        self.op = op
        self.right = right
    
    def compile(self):
        return {
            "#function": "math.eval",
            self.op: [
                self.left.compile(), self.right.compile()
            ]
        }
    
    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}BinOp [ {self.op} ] (\n{self.left.display(depth+1)}\n{self.right.display(depth+1)}\n{" "*depth*2})"
    
class UnaryOp(Node):
    def __init__(self, op, right:Node):
        self.op = op
        self.right = right
    
    def compile(self):
        return {
            "#function": "math.eval",
            self.op: [
                0,
                self.right
            ]
        }

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}Unary [ {self.op} ] (\n{self.right.display(depth+1)}\n{" "*depth*2})"


class MacroDef(Node):
    def __init__(self, name, args:list[Node], body):
        self.name = name
        self.args = args
        self.body = body
    
    def compile(self, args):
        print(args, self.args, self.body)

    def display(self, depth:int=0):
        return f"{" "*depth*2}MacroDef [ {self.name.value} ] (\n{"\n".join(f"{" "*depth*2}  {a.value}" for a in self.args)}\n{" "*depth*2}) {{\n{self.body.display(depth+1)}\n{" "*depth*2}}}"


class MacroCall(Node):
    def __init__(self, token, args:list[Node], es3):
        self.token = token
        self.args = args
        self.es3 = es3
    
    def compile(self):
        print(f"fetch function-macro?")
        return self.es3.function_macros.get(self.token.value).compile(self.args)

    def display(self, depth: int = 0) -> str:
        out = [f"{" "*depth*2}fill: [ {self.token.value} ] ("]

        for arg in self.args:
            out.append(arg.display(depth+2))
        
        out.append(f"{" "*depth*2})")

        return "\n".join(out)

class MacroAssign(Node):
    def __init__(self, token, node:Node):
        self.token = token
        self.node = node
    
    def get(self):
        return self.node
    
    def compile(self):
        return self.node.compile()

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}{self.token.value} = (\n{self.node.display(depth+1)}\n{" "*depth*2})"

class MacroRef(Node):
    def __init__(self, token, es3):
        self.token = token
        self.es3 = es3
    
    def compile(self):
        print(f"fetch macro reference?")
        print(self.es3.macros, self.token.value)
        print(self.es3.macros.get(self.token.value).compile())
        return self.es3.macros.get(self.token.value).compile()

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}replace: {self.token.value}"

class Concat(Node):
    def __init__(self, args:list[Node], sep:Node|None):
        self.args = args
        self.sep = sep
    
    def compile(self):
        pass

class MacroStack(Node):
    def __init__(self, obj, tokens:list, last_token, es3):
        self.obj = obj
        self.tokens = tokens
        self.last_token = last_token
        self.es3 = es3
        self._compiler = None
    
    def default_compiler(self, tokens:list):
        raise FinalScriptError("Undefined procedural macro")
    
    def compile(self):
        pass # TODO: this compile method is probably one of the most complicated ones

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}MacroStack [\n{self.obj.display(depth+1)}\n{" "*depth*2}] <- [{", ".join(str(t) for t in self.tokens)}]"

class BreakNode(Node):
    def __init__(self, token):
        self.token = token
    
    def compile(self):
        return {"#break": 1}

class ReturnNode(Node):
    def __init__(self, token, expr:Node):
        self.token = token
        self.expr = expr
    
    def compile(self):
        return {"#return": self.expr.compile() if self.expr else None}

class PassNode(Node):
    def __init__(self, token):
        self.token = token
    
    def compile(self):
        return None

class ArgsDefNode(Node):
    def __init__(self, positional:list[Node], keyword:list[tuple[Node, Node]]):
        self.positional = positional
        self.keyword = keyword
    
    def compile(self):
        pass

class ArgsCallNode(Node):
    def __init__(self, args:list[Node], kwargs:dict[str, Node]):
        self.args = args
        self.kwargs = kwargs
    
    def compile(self):
        
        kwrds = {}
        
        for name, val in self.kwargs.items():
            kwrds.update({name: val.compile()})
        
        out = {
            "args": [a.compile() for a in self.args],
            "kwargs": kwrds
        }
        if not out["args"]:
            out.pop("args")
        if not out["kwargs"]:
            out.pop("kwargs")
        
        return out

    def display(self, depth: int = 0) -> str:
        out = [f"{" "*depth*2}Args: Positional ("]
        for arg in self.args:
            out.append(arg.display(depth+1))
        out.append(f"{" "*depth*2}) Keyword {{")
        for name, kwrd in self.kwargs.items():
            out.append(f"{" "*depth*2}{name}: [\n{kwrd.display(depth+1)}\n{" "*depth*2}  ]")
        out.append(f"{" "*depth*2}}}")
        return "\n".join(out)

class ReferenceNode(Node):
    def __init__(self, token, global_=False, es3=None, type_annotation=None):
        self.token = token
        self.global_ = global_
        self.es3 = es3
        self.type_annotation = type_annotation
    
    def compile(self):
        if self.global_:
            return {"#ref": f"#{self.token.value}"}
        return {"#ref": self.token.value}

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}ref: {"#" if self.global_ else ""}{self.token.value}"

class AccessNode(Node):
    def __init__(self, obj: Node, attr):
        self.obj = obj
        self.attr = attr

    def compile(self):
        return {"#access": self.attr.value, "from": self.obj.compile()}

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}Access [\n{self.obj.display(depth+1)}\n{" "*depth*2}] (\n{" "*depth*2}  attr: {self.attr.value}\n{" "*depth*2})"

class AssignNode(Node):
    def __init__(self, ref_node:Node, val:Node):
        self.ref_node = ref_node
        self.val = val
    
    def compile(self):
        if isinstance(self.ref_node, ReferenceNode):
            return {"#store": {f"{"#" if self.ref_node.global_ else ""}{self.ref_node.token.value}": self.val.compile()}}

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}Assign [\n{self.ref_node.display(depth+1)}\n{" "*depth*2}] (\n{self.val.display(depth+1)}\n{" "*depth*2})"

class GetItemNode(Node):
    def __init__(self, obj, key):
        self.obj = obj,
        self.key = key
    
    def compile(self):
        pass

class FunctionDefNode(Node):
    def __init__(self, name, args:ArgsDefNode, body:Node):
        self.name = name
        self.args = args
        self.body = body
    
    def compile(self):
        pass

class CallNode(Node):
    def __init__(self, obj:Node, args:Node, es3):
        self.obj = obj
        self.args = args
        self.es3 = es3
    
    def compile(self):
        out = {"#call": self.obj.compile()}
        out.update(self.args.compile())
        
        return out

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}Call [\n{self.obj.display(depth+1)}\n{" "*depth*2}] (\n{self.args.display(depth+1)}\n{" "*depth*2})"


class NotNode(Node):
    def __init__(self, node:Node):
        self.node = node
    
    def compile(self):
        return {"#not": self.node.compile()}

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}not(\n{self.node.display(depth+1)}\n{" "*depth*2})"

class ValueNode(Node):
    def __init__(self, token):
        self.token = token
    
    def compile(self):
        return self.token.value

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}Value( {self.token.type} ) [ {self.token.value!r} ]"

class NoneNode(Node):
    def __init__(self, token):
        self.token = token
    
    def compile(self):
        return None

    def display(self, depth:int=0):
        return f"{" "*depth*2}none"

class ListNode(Node):
    def __init__(self, values:list[Node]):
        self.values = values
    
    def compile(self):
        return [v.compile() for v in self.values]

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}List[\n{ "\n".join(f"{val.display(depth+1)}" for val in self.values) }\n{" "*depth*2}]"

class DictNode(Node):
    def __init__(self, keys:list[Node], values:list[Node]):
        self.keys = keys
        self.values = values
    
    def compile(self):
        out = {}
        for k, v in zip(self.keys, self.values):
            out.update({k.compile(): v.compile()})

        return out

class NewNode(Node):
    def __init__(self, obj, args):
        self.obj = obj
        self.args = args
    
    def compile(self):
        out = {
            "#new": self.obj.value
        }
        out.update(self.args.compile())
        return out

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}new: {self.obj.value} {{\n{self.args.display(depth+1)}\n{" "*depth*2}}}"

class MoveNode(Node):
    def __init__(self, obj: Node, dest):
        self.obj = obj
        self.dest = dest
    
    def compile(self):
        pass

    def display(self, depth: int = 0) -> str:
        return f"{" "*depth*2}move: [\n{self.obj.display(depth+1)}\n{" "*depth*2}] -> {self.dest.value}"

class UnpackNode(Node):
    def __init__(self, unpack:list[Node]):
        self.unpack = unpack
    
    def compile(self):
        pass

    def display(self, depth:int=0):
        out = [f"{" "*depth*2}Unpack("]
        
        for node in self.unpack:
            out.append(node.display(depth+1))
        
        out.append(f"{" "*depth*2})")
        return "\n".join(out)

