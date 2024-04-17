# pylint: disable=[W,R,C, import-error]

from UIElement import UIElement

import inspect

from enum import Enum


class SnapNode(UIElement):

    class Mode(Enum):
        ACCEPTS = 0b01 # nodes that you attach other nodes to
        CONNECTS = 0b10 # nodes that attach to nodes that accept
        BOTH = 0b11

    class Event(Enum):
        """
        A description of what each event wants:\n
        ---\n\n
        SnapToThisNode (value of 1):\n
        the node's position has been set, please update parent position to whatever offset from this node you need.\n
        RETURN: None\n
        ---\n\n
        ReturnParentPositionRelativeToNode (value of 2):\n
        please return the distance between this node's position and the parent position.\n
        RETURN: tuple[int|float, int|float]\n
        """
        SnapToThisNode = 0b01
        ReturnParentPositionRelativeToNode = 0b10

    nodes = {}

    def __init__(self, parent, x:int, y:int, mask:str, mode:Mode, radius=5):
        self.x = x
        self.y = y
        self.mask = mask
        self.mode = mode
        self.parent = parent
        
        if not hasattr(parent, "node_event"):
            raise Exception("parent must have the method: `node_event`, taking arguments: (SnapNode, SnapNode.Event)")

        args = inspect.getfullargspec(parent.node_event)
        if not (len(args.args) == 2 or len(args.args) == 3 and args.args[0] in ["self", "cls"]):
            raise Exception("parent's `node_event` method must take only 2 arguments (plus self/cls): (SnapNode, SnapNode.Event)")
        
        self.held = self.last_held = False
        self.radius = radius
        self.has_proximity = False

        if self.mask not in SnapNode.nodes:
            SnapNode.nodes.update({self.mask: []})

        SnapNode.nodes[self.mask].append(self)

        self._frame = 0

    @classmethod
    def reset(cls):
        for _, nodes in cls.nodes:
            for node in nodes:
                node._frame = 0

    def dist(self, other):
        return (((other.x-self.x)**2) + ((other.y-self.y)**2)) ** 0.5

    def get_nearby(self) -> list:
        nearby = []
        for node in SnapNode.nodes[self.mask]:
            if node._frame == self._frame:
                if (d := self.dist(node)) <= self.radius + node.radius:
                    nearby.append((d, node))

        nearby.sort(
            key=lambda a: a[0]
        )
        return nearby

    def _event(self, editor, X, Y):
        self.last_held = self.held
        self.held = editor.held == self.parent != None

        near = self.get_nearby()
        
        if near:
            near[0].has_proximity = True
        
    
    def _update(self, editor, X, Y):
        self._frame = editor._frame
        
        if self.has_proximity:
            # TODO: render something to represent being hovered
            ...
            self.has_proximity = False


