# pylint: disable=[W,R,C, import-error]

from Util import PopoutElement
from UIElement import UIElement
from FunctionalElements import Button
from MultilineTextBox import MultilineTextBox

@PopoutElement()
class Popup(UIElement):
    _popup = None
    tick = 0
    
    def __init__(self, width:int, height:int, children=...):
        self.width = width
        self.height = height
        self.children = [] if children is ... else children
        self.mask = Button(0, 20, 1, 1, "", (0, 0, 0, 127), hover_color=(0, 0, 0, 127))
        self.mask.on_left_click = self._mask_on_click
        self.bg = Button(0, 0, self.width, self.height, bg_color=(24, 24, 24), hover_color=(24, 24, 24))
        self._on_close = self._default_on_close
        self.x = 0
        self.y = 0

    def _default_on_close(self):
        return

    def on_close(self, function):
        self._on_close = function
        return function
    
    def add_children(self, *children):
        self.children += [c for c in children]
        return self

    def popup(self):
        MultilineTextBox.set_focus(None)

        if isinstance(Popup._popup, Popup):
            Popup._popup._on_close()
        
        self.tick = 10
        Popup._popup = self
    
    def close(self):
        Popup._popup = None
        self._on_close()
        
    def _mask_on_click(self, editor):
        self.close()
        
    def _update_layout(self, editor):
        self.x = (editor.width-self.width)/2
        self.y = (editor.height-self.height)/2
        self.bg.width = self.width
        self.bg.height = self.height
        self.mask.width = editor.width
        self.mask.height = editor.height-40
    
    def _update(self, editor, X, Y):

        if self.tick > 0: return
        
        self.mask._update(editor, X, Y)
        self.bg._update(editor, X+self.x, Y+self.y)
        
        for child in self.children:
            child._update(editor, X+self.x, Y+self.y)
    
    def _event(self, editor, X, Y):

        if self.tick > 0:
            self.tick -= 1
            return

        for child in self.children[::-1]:
            child._event(editor, X+self.x, Y+self.y)
        
        self.bg._event(editor, X+self.x, Y+self.y)
        self.mask._event(editor, X, Y)
