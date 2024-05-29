# pylint: disable=[W,R,C, import-error]

from UIElement import UIElement
from Util import PopoutElement
from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_SIZE
from FunctionalElements import Button
from Geometry import Box

@PopoutElement()
class ContextTree(UIElement):
    global_tree = None
    groups = {}
    
    class Line: pass

    class MousePos:
        x = 0
        y = 0
        width = 0
        height = 0
    
    __slots__ = [
        "visible", "width", "option_height", "text_color", "bg_color",
        "line_color", "text_size", "hover_color", "click_color", "tree",
        "parent", "group"
    ]
    
    @classmethod
    def new(cls, x, y, width, height, label, *args, **kwargs) -> Button:
        """See ContextTree.__init__() for args/kwargs"""
        _m = cls(*args, **kwargs)
        m = Button(x, y, width, height, label, hover_color=(50, 50, 50), click_color=(50, 50, 50))
        m.on_left_click = _m
        _m.parent = m
        # m.children.append(_m)
        return m
    
    def __init__(self, tree_fields, width, option_height, text_color=TEXT_COLOR, bg_color=TEXT_BG_COLOR, line_color=(70, 70, 70), text_size=TEXT_SIZE, hover_color=TEXT_BG_COLOR, click_color=TEXT_BG_COLOR, group=None):
        self.visible = False
        self.width = width
        self.height = 0
        self.option_height = option_height
        self.text_color = text_color
        self.bg_color = bg_color
        self.line_color = line_color
        self.text_size = text_size
        self.hover_color = hover_color
        self.click_color = click_color
        self.tree = {}
        self.parent = None
        self.group = group

        h = 0

        for obj in tree_fields:
            if isinstance(obj, ContextTree.Line):
                self.tree.update({h: Box(0, h, self.width, 1, self.line_color)})
                h += 1/2

            elif isinstance(obj, dict):
                for key, val in obj.items():
                    if val is None:
                        continue

                    b = Button(0, 0, self.width, self.option_height, key, self.bg_color, self.text_color, self.text_size, self.hover_color, self.click_color)
                    b.on_left_click = val
                    if isinstance(val, UIElement):
                        b.children.append(val)
                        if isinstance(val, ContextTree):
                            val.parent = b

                    self.tree.update({h: b})
                    h += self.option_height
                    
        self.height = h

    def set_visibility(self, val:bool):
        self.visible = val
        if val:
            # print("group:", self.group)
            if self.group:
                if (tree := ContextTree.groups.get(self.group, None)):
                    if tree is not self:
                        tree.set_visibility(False)
                ContextTree.groups.update({self.group: self})

        else:
            for t in self.tree.values():
                if isinstance(t, Button):
                    for c in t.children:
                        if isinstance(c, ContextTree):
                            c.set_visibility(False)

    def toggle_visibility(self):
        self.set_visibility(not self.visible)
    
    def close(self):
        self.set_visibility(False)
    
    def open(self):
        self.set_visibility(True)

    def openAtMouse(self, editor):
        if not (self.parent is ContextTree.MousePos or self.parent is None):
            self.set_visibility(not self.visible)
            return
        ContextTree.MousePos.x, ContextTree.MousePos.y = editor.mouse_pos
        self.parent = ContextTree.MousePos
        self.set_visibility(not self.visible)

    def __call__(self, *_, **__):
        self.toggle_visibility()
    
    def _update(self, editor, X, Y):
        if self.visible:
            
            if self.tree:
                dx = 0 if X + self.parent.width + self.width < editor.width else -[v for v in self.tree.values()][0].width
                dw = min(0, X+self.parent.x+dx-1)
                dh = min(0, Y+self.parent.height+self.parent.y-1)
                
                editor.screen.fill((0, 120, 212), (X+self.parent.x+dx-dw-1, Y+self.parent.height+self.parent.y-1, self.width+2+dw, self.height+2+dw))
            
            for h, t in self.tree.items():
                _x = 0 if X + self.parent.width + self.width < editor.width else -t.width
                t._update(editor, X + _x+self.parent.x, Y + h+self.parent.height+self.parent.y)
    
    def _event(self, editor, X, Y):
        if self.visible:
            for h, t in self.tree.items():
                _x = 0 if X + self.parent.width + self.width < editor.width else -t.width
                t._event(editor, X + _x+self.parent.x, Y + h+self.parent.height+self.parent.y)
                if t.hovered:
                    editor._hovering_ctx_tree = True
    
    @classmethod
    def closeAll(cls):
        for group, tree in cls.groups.items():
            tree.set_visibility(False)

    @classmethod
    def event(cls, editor, X, Y):
        for group, tree in cls.groups.items():
            tree._event(editor, X, Y)
    
    @classmethod
    def update(cls, editor, X, Y):
        for group, tree in cls.groups.items():
            tree._update(editor, X, Y)
