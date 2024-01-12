# pylint: disable=W,R,C

from UIElement import UIElement
from RenderPrimitives import Color
from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_SIZE, FONT

import pygame
import re

class MultilineText(UIElement):
    
    __slots__ = [
        "x", "y", "min_width", "min_height", "content",
        "colored_content", "text_color", "text_bg_color",
        "font", "surfaces", "_text_width", "_text_height",
        "surface"
    ]
    
    def __init__(self, x:int, y:int, min_width:int=1, min_height:int=1, content:str="", text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|tuple|int=TEXT_BG_COLOR, text_size=TEXT_SIZE):
        assert min_width >= 1, "Min width must be 1 or more"
        assert min_height >= 1, "Min height must be 1 or more"
        self.x = x
        self.y = y
        self.min_width = min_width
        self.min_height = min_height
        self.content = content
        self.colored_content = content
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.font = pygame.font.Font(FONT, text_size)
        self.surfaces = []
        self.surface = None

        self._text_width = self.min_width
        self._text_height = self.min_height

        self.refresh_surfaces()
        # for line in content.split("\n"):
        #     s = self.font.render(line, True, tuple(self.text_color))
            
        #     self.surfaces.append(s)

    def get_lines(self):
        return self.content.split("\n")

    def _refresh_surfaces(self):
        # self.surfaces.clear()
        self._text_width = 0
        self._text_height = 0
        sl = []
        for line in self.get_lines():
            s = self.font.render(line or " ", True, (0, 0, 0))
            a, b = s.get_size()
            s = pygame.Surface([a+5, b], pygame.SRCALPHA) # pylint: disable=no-member
            # s.fill(tuple(self.text_bg_color))
            sl.append(s)
            self._text_width = max(self._text_width, s.get_width(), self.min_width)
            self._text_height += s.get_height()
        self._text_height = max(self._text_height, self.min_height)
        
        # self.surface = pygame.Surface((self._text_width, self._text_height), pygame.SRCALPHA, 32)
        
        self.surfaces = sl

    def set_colored_content(self, text:str):
        self.content = re.sub(r"\033\[(\d+;?)*m", "", text)
        self.colored_content = text
        self.refresh_surfaces()

    def color_text(self, text:str) -> str:
        return self.colored_content #re.sub(r"(#.*)", "\033[38;2;106;153;85m\\1\033[0m", text)

    def format_text(self, text:str, default_color:Color|list|tuple) -> list[tuple[Color|list|tuple, str]]:

        col = default_color

        raw = re.split("(\033\\[(?:\\d+;?)+m|\n)", self.color_text(text))
        data = []
        curr_line = []

        for r in raw:
            # print(f"{r!r}")
            if m := re.match(r"\033\[38;2;(?P<R>\d+);(?P<G>\d+);(?P<B>\d+)m", r):
                # print("is color")
                d = m.groupdict()
                col = (int(d["R"]), int(d["G"]), int(d["B"]))
            elif r == "\033[0m":
                # print("is color reset")
                col = default_color
            elif r == "\n":
                data.append(curr_line)
                curr_line = []
            else:
                curr_line.append((col, r))
        
        if curr_line:
            data.append(curr_line)
                

        return data #[[(default_color, l)] for l in text.split("\n")]

    def refresh_surfaces(self):
        self._refresh_surfaces()
        data = self.format_text(self.content, self.text_color)

        surf = pygame.Surface((self._text_width, self._text_height), pygame.SRCALPHA, 32) # pylint: disable=no-member
        # print(s.get_size())
        h = 0
        for line, surface in zip(data, self.surfaces):
            x = 1
            for col, segment in line:

                s = self.font.render(segment, True, tuple(col))
                surface.blit(s, (x, 0))
                x += s.get_width()
                
            surf.blit(surface, (0, h))
            h += surface.get_height()
        
        self.surface = surf

    def set_content(self, content:str=""):
        self.content = content

        self.refresh_surfaces()
        # self.surfaces.clear()
        # for line in content.split("\n"):
        #     s = self.font.render(line, True, tuple(self.text_color))
        #     self.surfaces.append(s)

    def _event(self, *_):
        pass

    def _update(self, editor, X, Y):
        w = self.min_width
        h = 0
        for s in self.surfaces:
            s:pygame.Surface
            w = max(w, s.get_width())
            h += s.get_height()
        h = max(self.min_height, h)

        if self.text_bg_color:
            editor.screen.fill(tuple(self.text_bg_color), (X+self.x-1, Y+self.y-1, w+2, h+2))

        if self.surface:
            editor.screen.blit(self.surface, (X+self.x, Y+self.y))
        # h = 0
        # for s in self.surfaces:
        #     editor.screen.blit(s, (X+self.x, Y+self.y+h))
        #     h += s.get_height()
