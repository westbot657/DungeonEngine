# pylint: disable=[W,R,C, import-error]
from UIElement import UIElement

class ShelfPanel(UIElement):
    def __init__(self, width, height, label, children):
        self.width = width
        self.height = height
        self.label = label # Used for panel search filtering
        self.children = children
        self.effective_height = height
    
    def _update(self, editor, X, Y):
        
        # update
        
        self.effective_height = self.height
        for child in self.children:
            if hasattr(child, "effective_height"):
                child._update(editor, X, Y+self.effective_height)
                self.effective_height += child.effective_height
            else:
                child._update(editor, X, Y)
            
            
    def _event(self, editor, X, Y):
        
        for child in self.children: # Can not reverse-iterate, as positions are constructed iteratively
            if hasattr(child, "effective_height"):
                child._event(editor, X, Y+self.effective_height)
                self.effective_height += child.effective_height
            else:
                child._event(editor, X, Y)

        # event

