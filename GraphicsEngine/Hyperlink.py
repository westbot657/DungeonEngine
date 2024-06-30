# pylint: disable=[W,R,C,import-error]

from MultilineText import MultilineText
from Options import HYPERLINK_COLOR, TEXT_BG_COLOR, TEXT_SIZE

import webbrowser

class Hyperlink(MultilineText):
    def __init__(self, x:int, y:int, min_width:int=1, min_height:int=1, content:str="", link:str="", text_color:tuple|int=HYPERLINK_COLOR, text_bg_color:tuple|int=None, text_size=TEXT_SIZE):
        super().__init__(x, y, min_width, min_height, content, text_color, text_bg_color, text_size)
        
        self.hovered_link = MultilineText(0, 0, min_width, min_height, content, text_color, text_bg_color, text_size)
        self.hovered_link.font.underline = True
        self.hovered_link.refresh_surfaces()
        self.hovered = False
        self.link = link
        if link:
            self._alt_text = f"Click to open:\n{link}"

    def _event(self, editor, X, Y):
        editor.check_hover(editor, (X+self.x, Y+self.y, self.width, self.height), self)
        
        if self.hovered:
            if editor.left_mouse_down() and self.link:
                webbrowser.open(self.link)
        
        super()._event(editor, X, Y)
    
    def _update(self, editor, X, Y):
        if self.hovered:
            self.hovered_link._update(editor, X+self.x, Y+self.y)
        else:
            super()._update(editor, X, Y)
        