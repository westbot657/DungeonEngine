# pylint: disable=W,R,C,import-error

try:
    from .EngineErrors import ScriptError, FinalScriptError, EOF
    from .Serializer import Serializer
except ImportError:
    from EngineErrors import ScriptError, FinalScriptError, EOF
    from Serializer import Serializer
    

from typing import Any

import re

test_script = """
#!emberhollow/rooms/boats/spawn_boat
#!enter-script

num_players = length(#dungeon.player_ids)

#dungeon.player_ids.append(#player.uid)

#player.tag: listening = true

$listening = #player.tag: listening

output("say `skip` to skeip dialog")

captain = random.choice([
    "...",
    "..."
])

starting_money = new: <engine:currency> {
    gold: random.range(9, 11),
    silver: random.range(5, 7),
    copper: random.range(2, 9)
}

if ($listening) {
    output("...")
    wait(2)
}

$out($message, $wait_time) {
    if ($listening) {
        output(
            format($message, captain=captain)
        )
        wait($wait_time)
    }
}

$outm($message, $wait_time) {
    if ($listening) {
        output(
            format($message, captain=captain, money=starting_money.total)
        )
        wait($wait_time)
    }
}

// ...

match random.choice([1, 2, 3, 4]) {
    case 1 {
        // ...
        $outm("{captain} hands you a bag of coins.\n(+{money})")
    }
}

#player.give_money(starting_money)


#player.goto(<emberhollow:rooms/docks/roads/road_4>)


"""

"""
[
    CONTEXT: '#!emberhollow/rooms/boats/spawn_boat'            (Line 2, Column 1 to 37),
    NEWLINE
    CONTEXT: '#!enter-script'                                  (Line 3, Column 1 to 15)
    NEWLINE
    WORD:    'num_players'                                     (Line 5, Column 1 to 12),
    LITERAL: '='                                               (Line 5, Column 13 to 14),
    WORD:    'length'                                          (Line 5, Column 15 to 21),
    LITERAL: '('                                               (Line 5, Column 21 to 22),
    LITERAL: '#'                                               (Line 5, Column 22 to 23),
    WORD:    'dungeon'                                         (Line 5, Column 23 to 30),
    LITERAL: '.'                                               (Line 5, Column 30 to 31),
    WORD:    'player_ids'                                      (Line 5, Column 31 to 41),
    LITERAL: ')'                                               (Line 5, Column 41 to 42),
    NEWLINE
    LITERAL: '#'                                               (Line 7, Column 1 to 2),
    WORD:    'dungeon'                                         (Line 7, Column 2 to 9),
    LITERAL: '.'                                               (Line 7, Column 9 to 10),
    WORD:    'player_ids'                                      (Line 7, Column 10 to 20),
    LITERAL: '.'                                               (Line 7, Column 20 to 21),
    WORD:    'append'                                          (Line 7, Column 21 to 27),
    LITERAL: '('                                               (Line 7, Column 27 to 28),
    LITERAL: '#'                                               (Line 7, Column 28 to 29),
    WORD:    'player'                                          (Line 7, Column 29 to 35),
    LITERAL: '.'                                               (Line 7, Column 35 to 36),
    WORD:    'uid'                                             (Line 7, Column 36 to 39),
    LITERAL: ')'                                               (Line 7, Column 39 to 40),
    NEWLINE
    LITERAL: '#'                                               (Line 9, Column 1 to 2),
    WORD:    'player'                                          (Line 9, Column 2 to 8),
    LITERAL: '.'                                               (Line 9, Column 8 to 9),
    WORD:    'tag'                                             (Line 9, Column 9 to 12),
    LITERAL: ':'                                               (Line 9, Column 12 to 13),
    WORD:    'listening'                                       (Line 9, Column 14 to 23),
    LITERAL: '='                                               (Line 9, Column 24 to 25),
    WORD:    'true'                                            (Line 9, Column 26 to 30),
    NEWLINE
    MACRO:   '$listening'                                      (Line 11, Column 1 to 11),
    LITERAL: '='                                               (Line 11, Column 12 to 13),
    LITERAL: '#'                                               (Line 11, Column 14 to 15),
    WORD:    'player'                                          (Line 11, Column 15 to 21),
    LITERAL: '.'                                               (Line 11, Column 21 to 22),
    WORD:    'tag'                                             (Line 11, Column 22 to 25),
    LITERAL: ':'                                               (Line 11, Column 25 to 26),
    WORD:    'listening'                                       (Line 11, Column 27 to 36),
    NEWLINE
    WORD:    'output'                                          (Line 13, Column 1 to 7),
    LITERAL: '('                                               (Line 13, Column 7 to 8),
    STRING:  'say `skip` to skeip dialog'                      (Line 13, Column 8 to 36),
    LITERAL: ')'                                               (Line 13, Column 36 to 37),
    NEWLINE
    WORD:    'captain'                                         (Line 15, Column 1 to 8),
    LITERAL: '='                                               (Line 15, Column 9 to 10),
    WORD:    'random'                                          (Line 15, Column 11 to 17),
    LITERAL: '.'                                               (Line 15, Column 17 to 18),
    WORD:    'choice'                                          (Line 15, Column 18 to 24),
    LITERAL: '('                                               (Line 15, Column 24 to 25),
    LITERAL: '['                                               (Line 15, Column 25 to 26),
    NEWLINE
    STRING:  '...'                                             (Line 16, Column 5 to 10),
    LITERAL: ','                                               (Line 16, Column 10 to 11),
    NEWLINE
    STRING:  '...'                                             (Line 17, Column 5 to 10),
    NEWLINE
    LITERAL: ']'                                               (Line 18, Column 1 to 2),
    LITERAL: ')'                                               (Line 18, Column 2 to 3),
    NEWLINE
    WORD:    'starting_money'                                  (Line 20, Column 1 to 15),
    LITERAL: '='                                               (Line 20, Column 16 to 17),
    WORD:    'new'                                             (Line 20, Column 18 to 21),
    LITERAL: ':'                                               (Line 20, Column 21 to 22),
    OBJECT: '<engine:currency>'                                (Line 20, Column 23 to 40),
    LITERAL: '{'                                               (Line 20, Column 41 to 42),
    NEWLINE
    WORD:    'gold'                                            (Line 21, Column 5 to 9),
    LITERAL: ':'                                               (Line 21, Column 9 to 10),
    WORD:    'random'                                          (Line 21, Column 11 to 17),
    LITERAL: '.'                                               (Line 21, Column 17 to 18),
    WORD:    'range'                                           (Line 21, Column 18 to 23),
    LITERAL: '('                                               (Line 21, Column 23 to 24),
    NUMBER:  '9'                                               (Line 21, Column 24 to 25),
    LITERAL: ','                                               (Line 21, Column 25 to 26),
    NUMBER:  '11'                                              (Line 21, Column 27 to 29),
    LITERAL: ')'                                               (Line 21, Column 29 to 30),
    LITERAL: ','                                               (Line 21, Column 30 to 31),
    NEWLINE
    WORD:    'silver'                                          (Line 22, Column 5 to 11),
    LITERAL: ':'                                               (Line 22, Column 11 to 12),
    WORD:    'random'                                          (Line 22, Column 13 to 19),
    LITERAL: '.'                                               (Line 22, Column 19 to 20),
    WORD:    'range'                                           (Line 22, Column 20 to 25),
    LITERAL: '('                                               (Line 22, Column 25 to 26),
    NUMBER:  '5'                                               (Line 22, Column 26 to 27),
    LITERAL: ','                                               (Line 22, Column 27 to 28),
    NUMBER:  '7'                                               (Line 22, Column 29 to 30),
    LITERAL: ')'                                               (Line 22, Column 30 to 31),
    LITERAL: ','                                               (Line 22, Column 31 to 32),
    NEWLINE
    WORD:    'copper'                                          (Line 23, Column 5 to 11),
    LITERAL: ':'                                               (Line 23, Column 11 to 12),
    WORD:    'random'                                          (Line 23, Column 13 to 19),
    LITERAL: '.'                                               (Line 23, Column 19 to 20),
    WORD:    'range'                                           (Line 23, Column 20 to 25),
    LITERAL: '('                                               (Line 23, Column 25 to 26),
    NUMBER:  '2'                                               (Line 23, Column 26 to 27),
    LITERAL: ','                                               (Line 23, Column 27 to 28),
    NUMBER:  '9'                                               (Line 23, Column 29 to 30),
    LITERAL: ')'                                               (Line 23, Column 30 to 31),
    NEWLINE
    LITERAL: '}'                                               (Line 24, Column 1 to 2),
    NEWLINE
    WORD:    'if'                                              (Line 26, Column 1 to 3),
    LITERAL: '('                                               (Line 26, Column 4 to 5),
    MACRO:   '$listening'                                      (Line 26, Column 5 to 15),
    LITERAL: ')'                                               (Line 26, Column 15 to 16),
    LITERAL: '{'                                               (Line 26, Column 17 to 18),
    NEWLINE
    WORD:    'output'                                          (Line 27, Column 5 to 11),
    LITERAL: '('                                               (Line 27, Column 11 to 12),
    STRING:  '...'                                             (Line 27, Column 12 to 17),
    LITERAL: ')'                                               (Line 27, Column 17 to 18),
    NEWLINE
    WORD:    'wait'                                            (Line 28, Column 5 to 9),
    LITERAL: '('                                               (Line 28, Column 9 to 10),
    NUMBER:  '2'                                               (Line 28, Column 10 to 11),
    LITERAL: ')'                                               (Line 28, Column 11 to 12),
    NEWLINE
    LITERAL: '}'                                               (Line 29, Column 1 to 2),
    NEWLINE
    MACRO:   '$out'                                            (Line 31, Column 1 to 5),
    LITERAL: '('                                               (Line 31, Column 5 to 6),
    MACRO:   '$message'                                        (Line 31, Column 6 to 14),
    LITERAL: ','                                               (Line 31, Column 14 to 15),
    MACRO:   '$wait_time'                                      (Line 31, Column 16 to 26),
    LITERAL: ')'                                               (Line 31, Column 26 to 27),
    LITERAL: '{'                                               (Line 31, Column 28 to 29),
    NEWLINE
    WORD:    'if'                                              (Line 32, Column 5 to 7),
    LITERAL: '('                                               (Line 32, Column 8 to 9),
    MACRO:   '$listening'                                      (Line 32, Column 9 to 19),
    LITERAL: ')'                                               (Line 32, Column 19 to 20),
    LITERAL: '{'                                               (Line 32, Column 21 to 22),
    NEWLINE
    WORD:    'output'                                          (Line 33, Column 9 to 15),
    LITERAL: '('                                               (Line 33, Column 15 to 16),
    NEWLINE
    WORD:    'format'                                          (Line 34, Column 13 to 19),
    LITERAL: '('                                               (Line 34, Column 19 to 20),
    MACRO:   '$message'                                        (Line 34, Column 20 to 28),
    LITERAL: ','                                               (Line 34, Column 28 to 29),
    WORD:    'captain'                                         (Line 34, Column 30 to 37),
    LITERAL: '='                                               (Line 34, Column 37 to 38),
    WORD:    'captain'                                         (Line 34, Column 38 to 45),
    LITERAL: ')'                                               (Line 34, Column 45 to 46),
    NEWLINE
    LITERAL: ')'                                               (Line 35, Column 9 to 10),
    NEWLINE
    WORD:    'wait'                                            (Line 36, Column 9 to 13), 
    LITERAL: '('                                               (Line 36, Column 13 to 14),
    MACRO:   '$wait_time'                                      (Line 36, Column 14 to 24),
    LITERAL: ')'                                               (Line 36, Column 24 to 25),
    NEWLINE
    LITERAL: '}'                                               (Line 37, Column 5 to 6),
    NEWLINE
    LITERAL: '}'                                               (Line 38, Column 1 to 2),
    NEWLINE
    MACRO:   '$outm'                                           (Line 40, Column 1 to 6),
    LITERAL: '('                                               (Line 40, Column 6 to 7),
    MACRO:   '$message'                                        (Line 40, Column 7 to 15),
    LITERAL: ','                                               (Line 40, Column 15 to 16),
    MACRO:   '$wait_time'                                      (Line 40, Column 17 to 27),
    LITERAL: ')'                                               (Line 40, Column 27 to 28),
    LITERAL: '{'                                               (Line 40, Column 29 to 30),
    NEWLINE
    WORD:    'if'                                              (Line 41, Column 5 to 7),
    LITERAL: '('                                               (Line 41, Column 8 to 9),
    MACRO:   '$listening'                                      (Line 41, Column 9 to 19),
    LITERAL: ')'                                               (Line 41, Column 19 to 20),
    LITERAL: '{'                                               (Line 41, Column 21 to 22),
    NEWLINE
    WORD:    'output'                                          (Line 42, Column 9 to 15),
    LITERAL: '('                                               (Line 42, Column 15 to 16),
    NEWLINE
    WORD:    'format'                                          (Line 43, Column 13 to 19),
    LITERAL: '('                                               (Line 43, Column 19 to 20),
    MACRO:   '$message'                                        (Line 43, Column 20 to 28),
    LITERAL: ','                                               (Line 43, Column 28 to 29),
    WORD:    'captain'                                         (Line 43, Column 30 to 37),
    LITERAL: '='                                               (Line 43, Column 37 to 38),
    WORD:    'captain'                                         (Line 43, Column 38 to 45),
    LITERAL: ','                                               (Line 43, Column 45 to 46),
    WORD:    'money'                                           (Line 43, Column 47 to 52),
    LITERAL: '='                                               (Line 43, Column 52 to 53),
    WORD:    'starting_money'                                  (Line 43, Column 53 to 67),
    LITERAL: '.'                                               (Line 43, Column 67 to 68),
    WORD:    'total'                                           (Line 43, Column 68 to 73),
    LITERAL: ')'                                               (Line 43, Column 73 to 74),
    NEWLINE
    LITERAL: ')'                                               (Line 44, Column 9 to 10),
    NEWLINE
    WORD:    'wait'                                            (Line 45, Column 9 to 13),
    LITERAL: '('                                               (Line 45, Column 13 to 14),
    MACRO:   '$wait_time'                                      (Line 45, Column 14 to 24),
    LITERAL: ')'                                               (Line 45, Column 24 to 25),
    NEWLINE
    LITERAL: '}'                                               (Line 46, Column 5 to 6),
    NEWLINE
    LITERAL: '}'                                               (Line 47, Column 1 to 2),
    NEWLINE
    WORD:    'match'                                           (Line 51, Column 1 to 6),
    WORD:    'random'                                          (Line 51, Column 7 to 13),
    LITERAL: '.'                                               (Line 51, Column 13 to 14),
    WORD:    'choice'                                          (Line 51, Column 14 to 20),
    LITERAL: '('                                               (Line 51, Column 20 to 21),
    LITERAL: '['                                               (Line 51, Column 21 to 22),
    NUMBER:  '1'                                               (Line 51, Column 22 to 23),
    LITERAL: ','                                               (Line 51, Column 23 to 24),
    NUMBER:  '2'                                               (Line 51, Column 25 to 26),
    LITERAL: ','                                               (Line 51, Column 26 to 27),
    NUMBER:  '3'                                               (Line 51, Column 28 to 29),
    LITERAL: ','                                               (Line 51, Column 29 to 30),
    NUMBER:  '4'                                               (Line 51, Column 31 to 32),
    LITERAL: ']'                                               (Line 51, Column 32 to 33),
    LITERAL: ')'                                               (Line 51, Column 33 to 34),
    LITERAL: '{'                                               (Line 51, Column 35 to 36),
    NEWLINE
    WORD:    'case'                                            (Line 52, Column 5 to 9),
    NUMBER:  '1'                                               (Line 52, Column 10 to 11),
    LITERAL: '{'                                               (Line 52, Column 12 to 13),
    NEWLINE
    MACRO:   '$outm'                                           (Line 54, Column 9 to 14),
    LITERAL: '('                                               (Line 54, Column 14 to 15),
    STRING:  '{captain} hands you a bag of coins.\n(+{money})' (Line 54, Column 15 to Line 55, Column 12),
    NEWLINE
    LITERAL: ')'                                               (Line 55, Column 12 to 13),
    NEWLINE
    LITERAL: '}'                                               (Line 56, Column 5 to 6),
    NEWLINE
    LITERAL: '}'                                               (Line 57, Column 1 to 2),
    NEWLINE
    LITERAL: '#'                                               (Line 59, Column 1 to 2),
    WORD:    'player'                                          (Line 59, Column 2 to 8),
    LITERAL: '.'                                               (Line 59, Column 8 to 9),
    WORD:    'give_money'                                      (Line 59, Column 9 to 19),
    LITERAL: '('                                               (Line 59, Column 19 to 20),
    WORD:    'starting_money'                                  (Line 59, Column 20 to 34),
    LITERAL: ')'                                               (Line 59, Column 34 to 35),
    NEWLINE
    LITERAL: '#'                                               (Line 62, Column 1 to 2),
    WORD:    'player'                                          (Line 62, Column 2 to 8),
    LITERAL: '.'                                               (Line 62, Column 8 to 9),
    WORD:    'goto'                                            (Line 62, Column 9 to 13),
    LITERAL: '('                                               (Line 62, Column 13 to 14),
    OBJECT: '<emberhollow:rooms/docks/roads/road_4>'           (Line 62, Column 14 to 52),
    LITERAL: ')'                                               (Line 62, Column 52 to 53)
    NEWLINE
    EOF
]
"""


class Node:
    def compile(self):
        return {}


class Expression(Node):
    def __init__(self, node:Node):
        self.node = node
    
    def compile(self):
        return self.node.compile()

class Statement(Node):
    def __init__(self, node:Node):
        self.node = node
    
    def compile(self):
        return self.node.compile()

class Statements(Node):
    def __init__(self, nodes:list[Node]):
        self.nodes = nodes
    
    def compile(self):
        return {
            "#functions": [node.compile() for node in self.nodes]
        }

class Comp(Node):
    def __init__(self, left:Node, op:str, right:Node):
        self.left = left
        self.op = op
        self.right = right
    
    def compile(self):
        return {
            "#function": "math.compare",
            "left": self.left.compile(),
            "op": self.op,
            "right": self.right.compile()
        }

class IfStatement(Node):
    def __init__(self, condition:Node, body:Node, else_node:Node=None):
        self.condition = condition
        self.body = body
        self.else_node = else_node
    
    def compile(self):
        return {
            "#check": self.condition.compile(),
            "true": self.body.compile(),
            "false": self.else_node.compile()
        }

class ForLoop(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class Scope(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class WhileLoop(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class ElseBranch(Node):
    def __init__(self, body:Node):
        self.body = body
    
    def compile(self):
        return self.body.compile()

class MatchCase(Node):
    def __init__(self, match_value:Node, cases:list[Expression], bodies:list[Scope]):
        self.match_value = match_value
        self.cases = cases
        self.bodies = bodies
    
    
    def compile(self):
        pass

class ClassDef(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class FunctionDef(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class BinaryOp(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MacroDef(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MacroCall(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MacroAssign(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class MacroRef(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class Table(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass

class Concat(Node):
    def __init__(self):
        pass
    
    def compile(self):
        pass


class EngineScript:
    _scripts = {}
    
    _patterns = {
        r"\/\/.*": "ignore",
        r"(?<!\/)\/\*(\*[^/]|[^*])+\*\/": "ignore",
        "\\#\\![^\n;]*;?": "CONTEXT",
        r"(\"(\\.|[^\"\\])*\"|\'(\\.|[^\'\\])*\')": "STRING",
        r"@[^ ]*": "TAG",
        r"\$[a-zA-Z_][a-zA-Z0-9_]*": "MACRO",
        r"\b(true|false)\b": "BOOLEAN",
        r"\<[^<> ]+\>": "OBJECT",
        r"(<=|>=|<|>|==|!=)": "COMP",
        r"(\.\.|::)": "CONCAT",
        r"\b(if|elif|else|while|for|in|and|not|or|true|false|none|match|case|class|def)\b": "KEYWORD",
        r"[a-zA-Z_][a-zA-Z0-9_]*": "WORD",
        r"(\d+(\.\d+)?|\.\d+)": "NUMBER",
        r"\*\*": "POW",
        r"[=\-+*/()&\[\]{},#%:|^\.;~`]": "LITERAL",
        r"\n+": "NEWLINE",
        r"[\t ]+": "ignore"
    }

    class Token:
        def __init__(self, es, value:str):
            self.es = es
            self.value = value
            
            for pattern, token_type in EngineScript._patterns.items():
                if re.fullmatch(pattern, self.value):
                    self.type = token_type

            self.line_start = es.line
            self.col_start = es.col

            es.lexpos += len(self.value)
            if x := self.value.count("\n"):
                es.line += x
                es.col = 0
            es.col += len(self.value.split("\n")[-1])
            
            self.line_end = es.line
            self.col_end = es.col

            if self.type == "NUMBER":
                self.value = float(self.value) if "." in self.value else int(self.value)
            elif self.type == "STRING":

                if not self.value.startswith(("\"", "'")):
                    self.value = self.value[2:-1]
                else:
                    self.value = self.value[1:-1]

                matches = list(re.finditer(r"\\.", self.value))
                matches.reverse()

                replacements = {
                    "\\n": "\n",
                    "\\\"": "\"",
                    "\\\'": "\'",
                    "\\\\": "\\"
                }
                for match in matches:
                    match:re.Match
                    self.value = self.value[0:match.start()] + replacements.get(match.group(), match.group()) + self.value[match.end():]

        def __eq__(self, other):
            if isinstance(other, EngineScript.Token):
                return self.type == other.type and self.value == other.value
            elif isinstance(other, tuple):
                return (self.type == other[0]) and ((self.value in other[1]) if isinstance(other[1], (tuple, list)) else (self.value == other[1]))

        def __str__(self):
            if self.line_start == self.line_end:
                return f"'{self.value}' (Line {self.line_start+1}, Column {self.col_start+1} to {self.col_end+1})"
            else:
                return f"'{self.value}' (Line {self.line_start+1}, Column {self.col_start+1} to Line {self.line_end+1}, Column {self.col_end+1})"

        def __repr__(self):
            return f"{self.type}: {self!s}"
    
        def unexpected(self):

            if self.line_start == self.line_end:
                err_disp = self.es.script.split("\n")[self.line_start]
                err_disp += f"\n{' '*self.col_start}{'^'*(min(self.col_end-self.col_start, len(err_disp)-self.col_start))}"
            else:
                err_disp = ""

            return ScriptError(f"Unexpected token at Line {self.line_start+1}, Column {self.col_start+1}: {self.value!r}:\n\n{err_disp}")

        def expected(self, actual, do_quotes=True):
            if self.line_start == self.line_end:
                err_disp = self.es.script.split("\n")[self.line_start]
                err_disp += f"\n{' '*self.col_start}{'^'*(min(self.col_end-self.col_start, len(err_disp)-self.col_start))}"
            else:
                err_disp = ""
            q = "'" if do_quotes else ""
            return FinalScriptError(f"Expected {q}{actual}{q} at Line {self.line_start+1}, Column {self.col_start+1}, got {self.value!r} instead.\n\n{err_disp}")

        def get_location(self):
            return f"Line {self.line_start+1}, Column {self.col_start+1}"

    class Macro:
        __slots__ = ["name", "token"]
        def __init__(self, name, token=None):
            self.name = name
            self.token = token
    
    
    class MacroFunction:
        __slots__ = [
            "es", "name", "args", "code"
        ]
        def __init__(self, es, name, args, code):
            self.es: EngineScript = es
            self.name = name
            self.args = args
            self.code = code
        
        def compile(self, arg_values, macro_token):
            macro_token: EngineScript.Token
            if len(arg_values) > len(self.args):
                raise FinalScriptError(f"Too many args passed into macro at {macro_token.get_location()}")
            elif len(arg_values) < len(self.args):
                raise FinalScriptError(f"Too few args passed into macro at {macro_token.get_location()}")
            
            macros = {}
            
            for k, v in zip(self.args, arg_values):
                macros.update({k: v})
                
            return self.deep_replace(self.code, macros, macro_token)


        def deep_replace(self, obj:Any, repls:dict, macro_call_token):
            if isinstance(obj, EngineScript.Macro):
                if obj.name in repls:
                    return repls[obj.name]
                elif obj.name in self.es.macros:
                    return self.es.macros[obj.name]
                raise FinalScriptError(f"Undefined macro: '{obj.name}' in macro function")
            elif isinstance(obj, dict):
                out = {}
                for k, v in obj.items():
                    if isinstance(k, EngineScript.Macro):
                        if k.name in repls:
                            r = repls[k.name]
                            if isinstance(r, dict) and ((v2 := r.get("#ref", None)) is not None):
                                out.update({v2: self.deep_replace(v, repls, macro_call_token)})
                            else:
                                raise FinalScriptError(f"Macro at {k.token.get_location()} does not describe a variable, so cannot be assigned a value. Called at {macro_call_token.get_location()}")
                    else:
                        out.update({k: self.deep_replace(v, repls, macro_call_token)})
                return out
            elif isinstance(obj, list):
                return [self.deep_replace(v, repls, macro_call_token) for v in obj]
            else:
                return obj


    def serialize(self):
        return {
            "script_file": Serializer.serialize(""),
            "script_name": Serializer.serialize(""),
            "script": Serializer.serialize(self.script),
            "line": Serializer.serialize(self.line),
            "col": Serializer.serialize(self.col),
            "lexpos": Serializer.serialize(self.lexpos),
            "compiled_script": Serializer.serialize(self.compiled_script),
            "_tokens": Serializer.serialize([]),
            "do_analysis": Serializer.serialize(False),
            "macros": Serializer.serialize(self.macros),
            "macro_functions": Serializer.serialize(self.macro_functions),
        }
    
    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    @classmethod
    def inline_script(cls,
    script:str):
        s = super().__new__(cls)
        s.init("", "<inline>")
        s.script = script
        return s

    def __new__(cls, script_file, do_analysis=False):
        script_name = f"{script_file.replace("\\", "/").replace(".ds", "").replace(".dungeon_script", "")}.ds"
        
        if script_name in cls._scripts:
            return cls._scripts[script_name]

        else:
            script = super().__new__(cls)
            cls._scripts.update({script_name: script})
            script.init(script_file, script_name, do_analysis)
            return script
    
    def init(self, script_file:str, script_name:str, do_analysis:bool=False):
        self.script_file = script_file
        self.script_name = script_name
        self.macro_functions: dict[str, EngineScript.MacroFunction] = {}
        self.macros: dict[str, Any] = {}
        self.script = ""
        self.line = 0
        self.col = 0
        self.lexpos = 0
        self.compiled_script = {}
        self.do_analysis = do_analysis
        self._tokens = []
        self.variable_table = {}

    def compile(self):
        self.macro_functions.clear()
        self.macros.clear()
        
        self.parse()
    
    def parse(self):
        
        self.line = 0
        self.col = 0
        
        tokens = [EngineScript.Token(self, t.group()) for t in re.finditer("(?:"+"|".join(self._patterns.keys())+")", self.script)]

        tokens = [t for t in tokens if t.type not in ["ignore", "context_hint"]]

        # print(tokens)

        self.build(tokens)
    
    def cleanup(self, ast):
        # print(f"CLEANUP: {ast}")
        if isinstance(ast, dict):
            if "functions" in ast and ast["functions"] == []:
                ast.pop("functions")
            if "true" in ast and ast["true"] == {"functions": []}:
                ast.update({"true": {}})
            if "false" in ast and ast["false"] == {"functions": []}:
                ast.update({"false": {}})
            out = {}
            for k, v in ast.items():
                x = self.cleanup(v)
                out.update({k: x})
            return out
        elif isinstance(ast, list):
            lst = []
            for l in ast:
                x = self.cleanup(l)
                if not any(x == h for h in (None, {})):
                    lst.append(x)
            return lst
        return ast
    
    def build(self, tokens):
        t = bool(tokens)
        if tokens:
            try:
                ast = self.statements(tokens)
                self.compiled_script = self.cleanup(ast.compile())
            except EOF:
                self.compiled_script = {}
        if t and self.compiled_script == {}:
            print(f"Warning:\n    File '{self.script_file}' contained code that compiled to nothing.")

    def statements(self, tokens):
        stmts = []
        while tokens:
            try:
                stmt = self.statement(tokens)
                stmts.append(stmt)
            except EOF as e:
                pass
        return Statements(stmts)

    def statement(self, tokens):
        return {}

"""
statements : statement*

statement : BREAK
          | RETURN expression?
          | PASS
          | function_def
          | class_def
          | if_statement
          | match_case
          | while_loop
          | for_loop
          | expression

expression : comp

if_statement : IF '(' expression ')' scope (elif_branch|else_branch)?

while_loop : WHILE '(' expression ')' scope

for_loop : FOR '(' word_list IN expreesion ')' scope

scope : '{' statements '}'

elif_branch : ELSEIF '(' expression ')' scope (elif_branch|else_branch)?

else_branch : ELSE scope

comp : NOT comp
     | arith (LT|LE|GT|GE|EE|NE) arith
     | comp (AND|OR) comp
     | arith

macro : MACRO '(' macro_args ')' '=' macro_scope
      | MACRO '(' comma_expressions ')'
      | MACRO '=' expression
      | MACRO

macro_args : (MACRO ','?)+

macro_scope : '{' macro_statements '}'

arith : mul (('+'|'-') mul)*

mul : pow (('*'|'/'|'%') pow)*

pow : concat ('^' concat)*

concat : var (CONCAT var)? (CONCATSEP var)?

atom : var '=' expression
     | var
     | '-' atom
     | '(' expression ')'
     | (NUMBER|BOOL|STRING|OBJECT|table|WORD|scope|macro|function_call)

var : WORD (('.' WORD)* ('[' expression ']')*)

table : '[' comma_expressions ']'
      | '{' table_contents '}'

function_call : var parameters scope?
              | 'new' ':' OBJECT scope

table_contents : (expression ':' expression ','?)*

parameters : '(' param_elements* ')'

param_elements : (expression ',')* (WORD '=' expression ','?)*

function_def : 'def' WORD '(' ( (WORD ','?)* (WORD '=' expression ','?)* )? ')' scope

class_def : 'class' OBJECT scope

"""




if __name__ == "__main__":
    es = EngineScript.inline_script(test_script)
    
    es.compile()
