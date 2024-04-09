# pylint: disable=W,R,C, import-error

from UIElement import UIElement
from Options import TEXT_BG2_COLOR, FONT, TEXT_SIZE
from MultilineText import MultilineText

import time
import pygame

class Toasts(UIElement):
    
    class Toast:
        def __init__(self, toasts, text, border_color, max_width):
            lines = text.split("\n")
            new_lines = []
            
            for line in lines:
                while len(line)*toasts._char_size[0] > max_width:
                    length = max_width//toasts._char_size[0]
                    pre = line[0:length]
                    line = line[length:]
                    new_lines.append(pre)
                if line:
                    new_lines.append(line)
            
            self.text_dsiplay = MultilineText(0, 0, 1, 1, "\n".join(new_lines))
            self.bg = pygame.Surface((max_width, self.text_dsiplay._text_height))
            self.bg.fill(border_color)
            self.bg.fill(border_color, (1, 1, max_width-2, self.text_dsiplay._text_height-2))
    
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.appear_queue = []
        self.appearing = None
        self.toasts = []
        self.disappearing = []
        
        f = pygame.font.Font(FONT, TEXT_SIZE)
        self._char_size = f.render(" ", True, (0, 0, 0)).get_size()
        


    def toast(self, text:str, display_time:float=2, border_color=TEXT_BG2_COLOR):
        self.appear_queue.append([display_time, Toasts.Toast(self, text, border_color, self.width)])
    
    
    def _event(self, editor, X, Y):
        ...
    
    def _update(self, editor, X, Y):
        ...





