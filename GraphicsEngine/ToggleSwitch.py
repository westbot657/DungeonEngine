# pylint: disable=W,R,C,import-error


from UIElement import UIElement
from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR

from enum import Enum, auto

class ToggleSwitch(UIElement):
    
    class Style(Enum):
        ROUND = auto()
        SQUARE = auto()
    
    
    def __init__(self, x, y, width, height, state=False, bg_color=TEXT_BG2_COLOR, on_color=TEXT_BG2_COLOR, off_color=TEXT_BG_COLOR, toggle_color=TEXT_BG3_COLOR, style:Style=Style.ROUND):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = state
        self.bg_color = bg_color
        self.on_color = on_color
        self.off_color = off_color
        self.toggle_color = toggle_color
        self.style = style
