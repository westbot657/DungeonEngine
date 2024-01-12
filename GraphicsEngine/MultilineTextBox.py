# pylint: disable=W,R,C,no-member

from UIElement import UIElement
from RenderPrimitives import Color, Image, Animation
from Options import TEXT_COLOR, TEXT_BG_COLOR, TEXT_SIZE, \
    FONT, CURSOR_BLINK_TIME, PATH, CURSOR_COLOR
from Util import Cursor, Selection, expand_text_lists

import pygame
import re
import time
import pyperclip

class MultilineTextBox(UIElement):

    _focused = None

    def __init__(self, x:int, y:int, min_width:int=1, min_height:int=1, content:str="", text_color:Color|tuple|int=TEXT_COLOR, text_bg_color:Color|Image|tuple|int=TEXT_BG_COLOR, text_size:int=TEXT_SIZE, cursor_color:Color|tuple|int=CURSOR_COLOR, single_line:bool=False):
        self.x = x
        self.y = y
        self.min_width = min_width
        self.min_height = min_height
        self._text_width = 0
        self._text_height = 0
        self.single_line = single_line
        self._lines = [[*line] for line in content.split("\n")]
        self.text_color = Color.color(text_color)
        self.text_bg_color = Color.color(text_bg_color)
        self.text_size = text_size
        self.font = pygame.font.Font(FONT, text_size)
        self.cursor_location = Cursor(0, 0)
        self._blink = CURSOR_BLINK_TIME
        self._cursor_tick = 0
        self._cursor_visible = False
        self._cursor_color = Color.color(cursor_color)
        self._cursor_surface = pygame.Surface((1, text_size+2))
        self._cursor_surface.fill(tuple(self._cursor_color))
        self.surfaces = []
        self.focused = False
        self.hovered = False
        self._text_selection_start = None
        self._text_selection_end = None
        self._highlight_offset = [0, 0]
        self._highlight = pygame.image.load(f"{PATH}/highlight.png")#pygame.Surface((1, 1), pygame.SRCALPHA, 24) # pylint: disable=no-member
        self.highlights = []
        self._save = self._default_save_event
        self._on_enter = self._default_on_enter_event
        
        self.char_whitelist: list[str] = None
        self.char_blacklist: list[str] = None

        self.set_content(content)

        self._history: list = []
        self._future: list = []

        self._history_triggers = " \n:.,/;'\"[]{}-=_+<>?|\\~`!@#$%^&*()"

        self._width, self._height = self.font.render("_", True, (0, 0, 0)).get_size()

    def save_history(self):
        content = self.get_content()
        if self._history:
            if self._history[0] != content:
                self._history.insert(0, content)
                self._future.clear()
        else:
            self._history.insert(0, content)
            self._future.clear()

    def undo(self):
        if len(self._history) > 1:
            self.set_content(p := self._history.pop(0))
            self._future.insert(0, p)
        elif len(self._history) == 1:
            self.set_content(self._history[0])

    def redo(self):
        if self._future:
            self.set_content(p := self._future.pop(0))
            self._history.insert(0, p)

    def on_save(self, function):
        """Decorator for a function
        
        This function is called whenever the text box detects the CTRL+S keybind
        
        passes:
            text_box (MultilineTextBox): The box that CTRL+S came from
            content (str): the entire text content of the text box
            selection (Selection | None): a Selection object containing the text box's selected text, and it's start and end text indices
            cursorPos (Cursor): the text box's current cursor position
        """
        self._save = function
        return function

    def on_enter(self, function):
        self._on_enter = function
        return function

    def _default_save_event(self, _, content:str, selection:Selection|None, cursorPos:Cursor):
        pass

    def _default_on_enter_event(self, _):
        pass

    def refresh_highlight(self):
        self.highlights.clear()
        if (s := self._text_selection_start) and (e := self._text_selection_end):
            ll = min(s.line, e.line)
            gl = max(s.line, e.line)
            if gl == ll:
                lc = min(s.col, e.col)
                gc = max(s.col, e.col)
            elif s.line < e.line:
                lc = s.col
                gc = e.col
            else:
                lc = e.col
                gc = s.col
            

            letter = self.font.render("_", True, (0, 0, 0)) # This is not shown on screen, only used to get width
            w = letter.get_width()# - 1
            h = letter.get_height()

            if ll == gl:
                line = self.get_lines()[ll]
                pre = len(line[0:lc]) * w
                self._highlight_offset = [pre, (ll * h)]
                self.highlights.append(pygame.transform.scale(self._highlight, ((gc-lc)*w, h)))

            else:
                lines = self.get_lines()
                line = lines[ll]
                pre = len(line[0:lc]) * w
                self._highlight_offset = [pre, (ll * h) + 2]
                self.highlights.append(pygame.transform.scale(self._highlight, ((len(line[lc:])+1)*w, h)))
                for l in range(ll+1, gl):
                    line = lines[l]
                    self.highlights.append(pygame.transform.scale(self._highlight, ((len(line)+1)*w, h)))
                
                line = lines[gl]
                self.highlights.append(pygame.transform.scale(self._highlight, (len(line[0:gc])*w, h)))

    def get_selection(self):
        if (s := self._text_selection_start) and (e := self._text_selection_end):
            ll = min(s.line, e.line)
            gl = max(s.line, e.line)
            if s.line == e.line:
                lc = min(s.col, e.col)
                gc = max(s.col, e.col)
            elif s.line > e.line:
                lc = e.col
                gc = s.col
            else:
                lc = s.col
                gc = e.col

            lc = min(s.col, e.col)
            gc = max(s.col, e.col)

            lines = self.get_lines()[ll:gl+1]
            # print(lines[-1], len(lines[-1]))
            lines[-1] = lines[-1][0:gc]
            lines[0] = lines[0][lc:]
            return "\n".join(lines)
        return None

    def set_selection(self, text:str):
        if (s := self._text_selection_start) is not None and (e := self._text_selection_end) is not None:
            ll = min(s.line, e.line)
            gl = max(s.line, e.line)
            lc = min(s.col, e.col)
            gc = max(s.col, e.col)
            
            mp = min(s, e).copy()

            lines = self.get_lines()
            pre = lines[0:ll+1]
            pre[-1] = pre[-1][0:lc]

            post = lines[gl:]
            post[0] = post[0][gc:]
            self.set_content("\n".join(pre) + text + "\n".join(post))
            self.cursor_location = mp
            self._text_selection_start = self._text_selection_end = None

    def get_index(self, cursor:Cursor):
        return sum(len(l) for l in self._lines[0:cursor.line]) + len(self._lines[cursor.line][0:cursor.col])

    def get_content(self):
        return "\n".join(["".join(line) for line in self._lines])

    def get_lines(self):
        return ["".join(line) for line in self._lines]

    def set_content(self, content:str):
        self._lines = [[*line] for line in content.split("\n")]
        self.cursor_location.line = min(self.cursor_location.line, len(self._lines)-1)
        if self._lines:
            self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line])-1)
        self.refresh_surfaces()

    def _refresh_surfaces(self):
        self.surfaces.clear()
        self._text_width = 0
        self._text_height = 0
        for line in self.get_lines():
            s = self.font.render(line or " ", True, (0, 0, 0))
            a, b = s.get_size()
            s = pygame.Surface((a+2, b), pygame.SRCALPHA)
            # s.fill(tuple(self.text_bg_color))
            self.surfaces.append(s)
            self._text_width = max(self._text_width, s.get_width())
            self._text_height += s.get_height()

    def color_text(self, text:str) -> str:
        return text #re.sub(r"(#.*)", "\033[38;2;106;153;85m\\1\033[0m", text)

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
        data = self.format_text("\n".join(self.get_lines()), self.text_color)

        for line, surface in zip(data, self.surfaces):
            x = 1
            for col, segment in line:

                s = self.font.render(segment, True, tuple(col))
                surface.blit(s, (x, 0))
                x += s.get_width()

    def format_content(self, content):
        return content

    def _update(self, editor, X, Y):
        h = 0

        if self.text_bg_color:
            if isinstance(self.text_bg_color, (Image, Animation)):
                self.text_bg_color.x = self.x - 1
                self.text_bg_color.y = self.y - 1
                self.text_bg_color.width = max(self._text_width, self.min_width) + 2
                self.text_bg_color.height = max(self._text_height, self.min_height) + 2
                self.text_bg_color._update(editor, X, Y)
            else:
                editor.screen.fill(tuple(self.text_bg_color), (X+self.x-1, Y+self.y-1, max(self._text_width, self.min_width)+2, max(self._text_height, self.min_height)+2))

        l = 0
        for s in self.surfaces:
            s:pygame.Surface
            editor.screen.blit(s, (X+self.x, Y+self.y+h))
            if l == self.cursor_location.line and self._cursor_visible:
                _h = self.font.render(self.get_lines()[self.cursor_location.line][0:self.cursor_location.col], True, (0, 0, 0)) # This is not shown on screen, only used to get width
                editor.screen.blit(self._cursor_surface, (X+self.x+_h.get_width(), Y+self.y+h+2))
            h += self._height#s.get_height()
            l += 1

        if self._text_selection_start and self._text_selection_end and self.highlights:
            # letter = self.font.render("_", True, (0, 0, 0)) # This is not shown on screen, only used to get width
            #w = letter.get_width()# - 1
            _h = self._height # letter.get_height()
            h = self.highlights[0]
            _x, _y = self._highlight_offset
            #print(f"highlight at: {X+self.x+_x}, {Y+self.y+_y}  mouse: {editor.mouse_pos} {h.get_size()}")
            editor.screen.blit(h, (X+self.x+_x, Y+self.y+_y))
            height = _h
            for h in self.highlights[1:]:
                editor.screen.blit(h, (X+self.x, Y+self.y+_y+height))
                height += _h

    def refresh_lines(self):
        self._lines = expand_text_lists(self._lines)

    @classmethod
    def set_focus(cls, box):
        if cls._focused:
            cls._focused.focused = False
            cls._focused._cursor_visible = False
        
        cls._focused = box

    def _event(self, editor, X, Y):
        w, h = max(self.min_width, self._text_width), max(self.min_height, self._text_height)
        _x, _y = editor.mouse_pos
        # print(X+self.x, Y+self.y, w, h, _x, _y)
        #if max(editor.X, X + self.x) <= _x <= min(X + self.x + w, editor.Width) and max(editor.Y, Y + self.y) <= _y <= min(Y + self.y + h, editor.Height):
        if editor.collides((_x, _y), (X+self.x, Y+self.y, w, h)):
            if editor._hovering is None:
                self.hovered = editor._hovered = True
                editor._hovering = self
        else:
            self.hovered = False

        if editor.left_mouse_down():
            if self.hovered:
                #if self.focused:
                letter = self.font.render("_", True, (0, 0, 0)) # This is not shown on screen, only used to get width
                w = letter.get_width()# - 1
                h = letter.get_height()
                dx = _x - (X + self.x)
                dy = _y - (Y + self.y)
                _old = self.cursor_location.copy()
                self.cursor_location.line = min(int(dy//h), len(self._lines)-1)
                self.cursor_location.col = max(min(int(round(dx/w)), len(self._lines[self.cursor_location.line])), 0)

                if pygame.K_LSHIFT in editor.keys:
                    if not self._text_selection_start:
                        self._text_selection_start = _old
                    self._text_selection_end = self.cursor_location.copy()
                else:
                    self._text_selection_start = self._text_selection_end = None

                MultilineTextBox.set_focus(self)
                self.focused = True
                self._cursor_visible = True
                self._cursor_tick = time.time()
                
            else:
                self.focused = False
                self._cursor_visible = False

        elif editor.mouse[0] and self.hovered:
            letter = self.font.render("_", True, (0, 0, 0))
            w = letter.get_width()# - 1
            h = letter.get_height()
            dx = _x - (X + self.x)
            dy = _y - (Y + self.y)
            _old = self.cursor_location.copy()
            self.cursor_location.line = min(int(dy//h), len(self._lines)-1)
            self.cursor_location.col = max(min(int(round(dx/w)), len(self._lines[self.cursor_location.line])), 0)

            if not self._text_selection_start:
                self._text_selection_start = _old
            self._text_selection_end = self.cursor_location.copy()
            self.refresh_highlight()

        if self.focused:
            for key in editor.typing:
                
                # print(f"{key!r}")
                if key == "$↑":
                    _old = self.cursor_location.copy()
                    if self.cursor_location.line == 0:
                        self.cursor_location.col = 0
                    else:
                        self.cursor_location.line -= 1
                        self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line]))
                    if pygame.K_LSHIFT in editor.keys:
                        if not self._text_selection_start:
                            self._text_selection_start = _old
                        self._text_selection_end = self.cursor_location.copy()
                        self.refresh_highlight()
                    elif self._text_selection_start and self._text_selection_end:
                        self.cursor_location = min(self._text_selection_start, self._text_selection_end)
                        if self.cursor_location.line > 0:
                            self.cursor_location.line -= 1
                            self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line]))
                        self._text_selection_start = self._text_selection_end = None
                elif key == "$↓":
                    _old = self.cursor_location.copy()
                    if self.cursor_location.line == len(self._lines)-1:
                        self.cursor_location.col = len(self._lines[self.cursor_location.line])
                    else:
                        self.cursor_location.line += 1
                        self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line]))
                    if pygame.K_LSHIFT in editor.keys:
                        if not self._text_selection_start:
                            self._text_selection_start = _old
                        self._text_selection_end = self.cursor_location.copy()
                        self.refresh_highlight()
                    elif self._text_selection_start and self._text_selection_end:
                        self.cursor_location = max(self._text_selection_start, self._text_selection_end)
                        if self.cursor_location.line < len(self._lines)-1:
                            self.cursor_location.line += 1
                            self.cursor_location.col = min(self.cursor_location.col, len(self._lines[self.cursor_location.line]))
                        self._text_selection_start = self._text_selection_end = None
                elif key == "$→":
                    _old = self.cursor_location.copy()
                    if self.cursor_location.col == len(self._lines[self.cursor_location.line]):
                        if self.cursor_location.line < len(self._lines)-1:
                            self.cursor_location.line += 1
                            self.cursor_location.col = 0
                    else:
                        self.cursor_location.col += 1
                    if pygame.K_LSHIFT in editor.keys:
                        if not self._text_selection_start:
                            self._text_selection_start = _old
                        self._text_selection_end = self.cursor_location.copy()
                        self.refresh_highlight()
                    elif self._text_selection_start and self._text_selection_end:
                        self.cursor_location = max(self._text_selection_start, self._text_selection_end)
                        self._text_selection_start = self._text_selection_end = None
                elif key == "$←":
                    _old = self.cursor_location.copy()
                    if self.cursor_location.col == 0:
                        if self.cursor_location.line > 0:
                            self.cursor_location.line -= 1
                            self.cursor_location.col = len(self._lines[self.cursor_location.line])
                    else:
                        self.cursor_location.col -= 1
                    if pygame.K_LSHIFT in editor.keys:
                        if not self._text_selection_start:
                            self._text_selection_start = _old
                        self._text_selection_end = self.cursor_location.copy()
                        self.refresh_highlight()
                    elif self._text_selection_start and self._text_selection_end:
                        self.cursor_location = min(self._text_selection_start, self._text_selection_end)
                        self._text_selection_start = self._text_selection_end = None
                elif key in "\n\r":
                    if self.single_line:
                        self._on_enter(self)
                        continue
                    if self.get_selection():
                        self.set_selection("")
                    txt = self._lines[self.cursor_location.line][self.cursor_location.col:]
                    self._lines[self.cursor_location.line] = self._lines[self.cursor_location.line][0:self.cursor_location.col]
                    self.cursor_location.line += 1
                    self.cursor_location.col = 0
                    self._lines.insert(self.cursor_location.line, txt)
                    self.save_history()
                    self._on_enter(self)
                elif key == "\t":
                    pre = "".join(self._lines[self.cursor_location.line][0:self.cursor_location.col])
                    if pre.strip() == "":
                        add = " " * (4 - (len(pre) % 4))
                    else:
                        add = "    "
                    self._lines[self.cursor_location.line].insert(self.cursor_location.col, add)
                    self.refresh_lines()
                    self.cursor_location.col += len(add)
                elif key == "\b":
                    if self.get_selection():
                        self.set_selection("")
                    else:
                        if self.cursor_location.col > 0:
                            c = self._lines[self.cursor_location.line][self.cursor_location.col-1]
                            txt = self._lines[self.cursor_location.line][0:self.cursor_location.col-1] + \
                                self._lines[self.cursor_location.line][self.cursor_location.col:]
                            self._lines[self.cursor_location.line] = txt
                            self.cursor_location.col -= 1
                            if c in self._history_triggers:
                                self.save_history()
                        elif self.cursor_location.line > 0:
                            self.cursor_location.col = len(self._lines[self.cursor_location.line-1])
                            self._lines[self.cursor_location.line-1] += self._lines.pop(self.cursor_location.line)
                            self.cursor_location.line -= 1
                            self.save_history()
                    
                elif key == "\x7f": # delete
                    if self.get_selection():
                        self.set_selection("")
                    else:
                        if self.cursor_location.col < len(self._lines[self.cursor_location.line]):
                            c = self._lines[self.cursor_location.line][self.cursor_location.col]
                            txt = self._lines[self.cursor_location.line][0:self.cursor_location.col] + \
                                self._lines[self.cursor_location.line][self.cursor_location.col+1:]
                            self._lines[self.cursor_location.line] = txt
                            # self.cursor_location.col -= 1
                            if c in self._history_triggers:
                                self.save_history()
                        elif self.cursor_location.line < len(self._lines)-1:
                            # self.cursor_location.col = len(self._lines[self.cursor_location.line-1])
                            self._lines[self.cursor_location.line] += self._lines.pop(self.cursor_location.line+1)
                            # self.cursor_location.line -= 1
                            self.save_history()
                elif key == "\x1a": # CTRL+Z
                    if pygame.K_LSHIFT in editor.keys:
                        self.redo()
                    else:
                        if not self._future:
                            self.save_history()
                        self.undo()
                elif key == "\x18": # CTRL+X
                    if (self._text_selection_start is not None) and (self._text_selection_end is not None):
                        pyperclip.copy(self.get_selection())
                        self.set_selection("")
                        self.save_history()
                elif key == "\x03": # CTRL+C
                    if (self._text_selection_start is not None) and (self._text_selection_end is not None):
                        pyperclip.copy(self.get_selection())
                elif key == "\x16": # CTRL+V
                    if self.get_selection():
                        self.set_selection("")
                    _l = pyperclip.paste()
                    if self.single_line:
                        noline = re.sub("\n+", " ", _l)
                        self._lines[self.cursor_location.line].insert(self.cursor_location.col, noline)
                        self.refresh_lines()
                        self.cursor_location.col += len(noline)
                        self.save_history()
                        continue
                    l = _l.split("\n")
                    l0 = l[0]
                    self._lines[self.cursor_location.line].insert(self.cursor_location.col, l0)
                    
                    for _line in l[1:-1]:
                        self.cursor_location.line += 1
                        self._lines.insert(self.cursor_location.line, [c for c in re.split(r"", _line) if c])
                    
                    if len(l) > 1:
                        self.cursor_location.line += 1
                        if len(self._lines) <= self.cursor_location.line:
                            self._lines.append([c for c in re.split(r"", l[-1]) if c])
                        else:
                            self._lines.insert(self.cursor_location.line, [])
                            self._lines[self.cursor_location.line].insert(0, l[-1])
                    self.refresh_lines()
                    self.cursor_location.col += len(l[-1])
                    self.save_history()
                elif key == "\x01": # CTRL+A
                    self._text_selection_start = Cursor(0, 0)
                    self._text_selection_end = Cursor(len(self._lines)-1, len(self._lines[-1]))
                    self.refresh_highlight()
                elif key == "\x13": # CTRL+S
                    content = self.get_content()
                    cursor = self.cursor_location.copy()
                    selection = None
                    if self._text_selection_start and self._text_selection_end:
                        selection = Selection(
                            self.get_selection(),
                            self.get_index(self._text_selection_start),
                            self.get_index(self._text_selection_end)
                        )
                    self._save(self, content, selection, cursor)
                    self.save_history()
                else:
                    # self.char_blacklist: list
                    if ((self.char_whitelist is not None) and (key not in self.char_whitelist)) or ((self.char_blacklist is not None) and (key in self.char_blacklist)): # pylint: disable=unsupported-membership-test
                        continue
                    if self.get_selection():
                        self.set_selection("")
                    self._lines[self.cursor_location.line].insert(self.cursor_location.col, key)
                    self.cursor_location.col += 1
                    if key in self._history_triggers:
                        self.save_history()
            if self._text_selection_start == self._text_selection_end and self._text_selection_start != None:
                self._text_selection_start = self._text_selection_end = None

            if (time.time() - self._cursor_tick) % 1 < 0.5:
                self._cursor_visible = True
            else:
                self._cursor_visible = False

            # self._cursor_tick += 1
            # if time.time() % 1 == 0:
            #     self._cursor_tick = 0
            #     self._cursor_visible = not self._cursor_visible


            # self.surface = self.font.render(self.get_content(), True, self.text_color)
            self.refresh_surfaces()
