# pylint: disable=W,R,C

from UIElement import UIElement
from RenderPrimitives import Color, Animation, Image
from Options import TEXT_COLOR, TEXT_BG_COLOR, \
    TEXT_SIZE, FONT, CURSOR_BLINK_TIME, PATH, TAB_SIZE

import pygame
import pyperclip

class TextBox(UIElement):
    
    __slots__ = [
        "x", "y", "min_width", "text_color", "text_bg_color",
        "text_size", "font", "surface", "focused", "hovered",
        "_letters", "cursor_location", "_cursor_surface",
        "_cursor_tick", "_blink", "_cursor_visible",
        "_text_selection_end", "_text_selection_start",
        "_highlight", "highlight"
    ]
    
    def __init__(self, x:int, y:int, min_width:int=1, content:str="", text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|tuple|int=TEXT_BG_COLOR, text_size:int=TEXT_SIZE):
        self.x = x
        self.y = y
        assert min_width >= 1, "Min width must be 1 or more"
        self.min_width = min_width
        #self.content = content
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.text_size = text_size
        self.font = pygame.font.Font(FONT, text_size)
        self.surface = self.font.render(content, True, tuple(self.text_color))
        self.focused = False
        self.hovered = False
        self._letters = [l for l in content]
        self.cursor_location = 0
        self._cursor_surface = pygame.Surface((1, text_size))
        self._cursor_tick = 0
        self._blink = CURSOR_BLINK_TIME
        self._cursor_visible = False
        self._text_selection_end = None
        self._text_selection_start = None
        self._highlight = pygame.image.load(f"{PATH}/highlight.png")#pygame.Surface((1, self.text_size), pygame.SRCALPHA, 32) # pylint: disable=no-member
        #self._highlight.fill(TEXT_HIGHLIGHT)
        self.highlight = self._highlight.copy()

    def get_selection(self):
        if self._text_selection_start and self._text_selection_end:
            a = min(self._text_selection_start, self._text_selection_end)
            b = max(self._text_selection_start, self._text_selection_end)
            return self.get_content()[a:b]
        return None

    def set_selection(self, text:str):
        if self._text_selection_start and self._text_selection_end:
            a = min(self._text_selection_start, self._text_selection_end)
            b = max(self._text_selection_start, self._text_selection_end)
            content = self.get_content()
            pre = content[0:a]
            post = content[b-1:]
            self.set_content(pre + text + post)
            self._text_selection_start = self._text_selection_end = None

    def get_content(self):
        return "".join(self._letters)

    def set_content(self, content:str=""):
        self._letters = [l for l in content]
        #self.surface = self.font.render(content, True, self.text_color)
        self.cursor_location = min(self.cursor_location, len(self._letters))

    def refresh_highlight(self):
        if self._text_selection_start and self._text_selection_end:
            a = min(self._text_selection_start, self._text_selection_end)
            b = max(self._text_selection_start, self._text_selection_end)
            letter = self.font.render("T", True, (0, 0, 0))
            w = letter.get_width()
            width = (b - a) * w
            self.highlight = pygame.transform.scale(self._highlight, (width, self.text_size))

    def _event(self, editor, X, Y):
        w, h = self.surface.get_size()
        _x, _y = editor.mouse_pos

        #if max(editor.X, X + self.x) <= _x <= min(X + self.x + w, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + h, editor.Height):
        if editor.collides((_x, _y), (X+self.x, Y+self.y, w, h)):
            if editor._hovering is not None:
                editor._hovering = self
                self.hovered = editor._hovered = True
        else:
            self.hovered = False

        if editor.left_mouse_down():
            if self.hovered:
                letter = self.font.render("T", True, (0, 0, 0))
                w = letter.get_width()# - 1
                dx = _x - (X + self.x)

                self.cursor_location = min(int(round(dx/w)), len(self._letters))
                
                if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                    self._text_selection_end = self.cursor_location
                else:
                    self._text_selection_start = self.cursor_location
                    self._text_selection_end = None

                self.focused = True
                self._cursor_visible = True
                self._cursor_tick = 0
                
            else:
                self.focused = False
                self._cursor_visible = False

        if self.focused:
            for key in editor.new_keys:
                if pygame.K_LCTRL in editor.keys and key == pygame.K_c:
                    if self._text_selection_start and self._text_selection_end:
                        pyperclip.copy(self.get_selection())
                elif pygame.K_LCTRL in editor.keys and key == pygame.K_x:
                    if self._text_selection_start and self._text_selection_end:
                        pyperclip.copy(self.get_selection())
                        self.set_selection("")
                elif pygame.K_LCTRL in editor.keys and key == pygame.K_v:
                    if self._text_selection_start and self._text_selection_end:
                        self.set_selection(pyperclip.paste())
                    else:
                        self._text_selection_start = self._text_selection_end = self.cursor_location.copy()
                        self.set_selection(pyperclip.paste())
                elif key in [
                        pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL,
                        pygame.K_CAPSLOCK, pygame.K_LALT,
                        pygame.K_RALT
                    ]: ...
                elif key in (pygame.K_TAB, "\t"):
                    tabs_to_add = TAB_SIZE - (self.cursor_location % TAB_SIZE)
                    self.set_selection("")
                    for i in range(tabs_to_add):
                        self._letters.insert(self.cursor_location, " ")
                        self.cursor_location += 1
                elif key == pygame.K_UP:
                    self.cursor_location = 0
                    if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                        self._text_selection_end = self.cursor_location
                        self.refresh_highlight()
                    elif not self._text_selection_start:
                        self._text_selection_start = self.cursor_location
                    else:
                        self._text_selection_start = self._text_selection_end = None
                elif key == pygame.K_LEFT:
                    self.cursor_location = max(self.cursor_location - 1, 0)
                    if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                        self._text_selection_end = self.cursor_location
                        self.refresh_highlight()
                    elif not self._text_selection_start:
                        self._text_selection_start = self.cursor_location
                    else:
                        self._text_selection_start = self._text_selection_end = None
                elif key == pygame.K_RIGHT:
                    self.cursor_location = min(self.cursor_location + 1, len(self._letters))
                    if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                        self._text_selection_end = self.cursor_location
                        self.refresh_highlight()
                    elif not self._text_selection_start:
                        self._text_selection_start = self.cursor_location
                    else:
                        self._text_selection_start = self._text_selection_end = None
                elif key == pygame.K_DOWN:
                    self.cursor_location = len(self._letters)
                    if pygame.K_LSHIFT in editor.keys and self._text_selection_start:
                        self._text_selection_end = self.cursor_location
                        self.refresh_highlight()
                    elif not self._text_selection_start:
                        self._text_selection_start = self.cursor_location
                    else:
                        self._text_selection_start = self._text_selection_end = None
                elif key in ["\b", pygame.K_BACKSPACE]:
                    if self._text_selection_start and self._text_selection_end:
                        self.set_selection("")
                        self._text_selection_start = self._text_selection_end = None
                    elif 0 < self.cursor_location <= len(self._letters):
                        self.cursor_location -= 1
                        self._letters.pop(self.cursor_location)
                elif key in (pygame.K_DELETE, pygame.KSCAN_DELETE):
                    if self._text_selection_start and self._text_selection_end:
                        self.set_selection("")
                        self._text_selection_start = self._text_selection_end = None
                    elif 0 <= self.cursor_location < len(self._letters):
                        self._letters.pop(self.cursor_location)
                elif key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, "\n", "\r"):
                    self.focused = False
                    self._cursor_visible = False
                    self.on_enter(self.get_content())
                    break
                else:
                    self._letters.insert(self.cursor_location, key)
                    self.cursor_location += 1
                #print(self.get_content())

            self._cursor_tick += 1
            if self._cursor_tick >= self._blink:
                self._cursor_tick = 0
                self._cursor_visible = not self._cursor_visible

            self.surface = self.font.render(self.get_content(), True, tuple(self.text_color))

    def _update(self, editor, X, Y):
        _x, _y = self.surface.get_size()
        if self.text_bg_color:
            if isinstance(self.text_bg_color, (Image, Animation)):
                self.text_bg_color.resize(_x+2, _y+2)._update(editor, X+self.x-1, Y+self.y-1)
            else:
                editor.screen.fill(self.text_bg_color, (X+self.x-1, Y+self.y-1, _x+2, _y+2))
        editor.screen.blit(self.surface, (X+self.x, Y+self.y))

        if self._cursor_visible:
            h = self.font.render(self.get_content()[0:self.cursor_location], True, (0, 0, 0)) # This is not shown on screen, only used to get width
            editor.screen.blit(self._cursor_surface, (X+self.x+h.get_width(), Y+self.y+2))

    def on_enter(self, text:str): ... # pylint: disable=unused-argument
