# pylint: disable=W,R,C, import-error

from UIElement import UIElement
from Options import TEXT_BG3_COLOR, FONT, TEXT_SIZE, TEXT_BG_COLOR
from MultilineText import MultilineText

import pygame
import math
import time

class Toasts(UIElement):
    
    class Toast(UIElement):
        def __init__(self, toasts, text, border_color, max_width):
            self.keep_showing = False
            lines = text.split("\n")
            new_lines = []
            
            for line in lines:
                while len(line)*toasts._char_size[0] > max_width-15:
                    length = max_width//toasts._char_size[0]
                    pre = line[0:length]
                    line = line[length:]
                    new_lines.append(pre)
                if line:
                    new_lines.append(line)
            
            print(f"formatted lines to {new_lines}")
            
            self.text_dsiplay = MultilineText(5, 5, 1, 1, "\n".join(new_lines))
            self.bg = pygame.Surface((max_width, self.text_dsiplay._text_height+10))
            self.bg.fill(border_color)
            self.bg.fill(TEXT_BG_COLOR, (1, 1, max_width-2, self.text_dsiplay._text_height+8))
            self.height = self.text_dsiplay._text_height+18
        
        def _event(self, editor, X, Y):
            pass
        
        def _update(self, editor, X, Y):
            editor.screen.blit(self.bg, (X, Y))
            self.text_dsiplay._update(editor, X, Y)
    
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.appear_queue: list[list[float, Toasts.Toast]] = []
        self.appearing: list[float, float, list[float, Toasts.Toast], int] = None
        self.toasts: list[list[float, Toasts.Toast]] = []
        self.disappearing: list[list[float, Toasts.Toast]] = []
        
        f = pygame.font.Font(FONT, TEXT_SIZE)
        self._char_size = f.render(" ", True, (0, 0, 0)).get_size()
        


    def toast(self, text:str, display_time:float=2, border_color=TEXT_BG3_COLOR) -> Toast:
        toast = Toasts.Toast(self, text, border_color, self.width)
        self.appear_queue.append([display_time, toast])
        return toast
    
    
    def _event(self, editor, X, Y):
        
        tm = time.time()
        if self.appearing is not None:
            if self.appearing[0]+self.appearing[1] <= tm:
                self.toasts.insert(0, [tm + self.appearing[2][0], self.appearing[2][1]])
                if len(self.toasts) > 3:
                    self.disappearing.insert(0, [tm, self.toasts.pop(-1)[1]])
                self.appearing = None
        else:
            if self.appear_queue:
                a: list[int, Toasts.Toast] = self.appear_queue.pop(0)
                t: int = a[1].height/100 # this is where time of slide-in is set, divisor controls pixels per second
                self.appearing = [tm, t, a, a[1].height]
        
        for toast in self.toasts.copy():
            if toast[0] <= tm and toast[1].keep_showing == False:
                self.toasts.remove(toast)
                self.disappearing.insert(0, [tm, toast[1]])
        
        for toast in self.disappearing.copy():
            if toast[0]+1 <= tm:
                self.disappearing.remove(toast)




    def _update(self, editor, X, Y):
        y_offset = 0
        tm = time.time()
        if (toast := self.appearing) is not None:
            # y_offset = toast[3]
            y_offset = (tm-toast[0])/toast[1] * toast[3]
            toast[2][1]._update(editor, X+self.x, Y+self.y-y_offset)

        for toast in self.toasts:
            y_offset += toast[1].height
            toast[1]._update(editor, X+self.x, Y+self.y-y_offset)
        
        for toast in self.disappearing:
            y_offset += toast[1].height
            x_offset = (tm-toast[0]) * self.width
            toast[1]._update(editor, X+self.x+x_offset, Y+self.y-y_offset)
