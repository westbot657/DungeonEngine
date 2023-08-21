# pylint: disable=[W,R,C,import-error,no-member]

try:
    from .GraphicElement import GraphicElement
    from .Vector2 import Vector2
except ImportError:
    from GraphicElement import GraphicElement
    from Vector2 import Vector2

import json, time, pyperclip

with open("./Engine/GraphicsEngine/defaults.json", "r+", encoding="utf-8") as f:
    text_config = json.load(f)["text"]

    DEFAULT_FONT = text_config["font"]
    DEFAULT_TEXTSIZE = text_config["size"]
    DEFAULT_COLOR = text_config["color"]
    DEFAULT_BACKGROUND = text_config["background"]
    DEFAULT_ANTIALIAS = text_config["antialias"]
    DEFAULT_LINE_SPACING = text_config["line spacing"]
    SELECTION_COLOR = text_config["selection"]

def mround(number:float):
    if number % 1 < 0.5:
        return int(number)
    return int(number) + 1

class MultilineText(GraphicElement):
    pygame = None

    @classmethod
    def init(cls, pygame):
        cls.pygame = pygame

    def __init__(self, position:Vector2, text:str, writable:bool=False, **options):
        """multiline text object

        Args:
            position (Vector2): where the textbox is

            text (str): text for text box to start with
        
            writable (bool): whether the text box can be selected and written in
        options:
            text_size (int): size of text

            text_color (list): text color

            font (str): path to font file

            background (list|None): background color

            antialias (bool): antialias

            min_size (Vector2): minimum size of the text box
            max_size (Vector2): maximum size of the text box
            or
            fixed_size (Vector2): fixed size of the text box
        """
        self.position = position
        self.text = text
        self.writable = writable
        self.hoverable = self.writable
        self.clickable = self.writable
        self.draggable = False
        self.single_line = False
        self.held = False
        self.hovered = False
        self.selected = False
        self.scrolled = Vector2(1, 0)
        self._updaters = {}
        self.children = []
        self.parent = None
        self._type = None
        self.text_size = options.get("text_size", DEFAULT_TEXTSIZE)
        self.text_color = options.get("text_color", DEFAULT_COLOR)
        self.font = options.get("font", DEFAULT_FONT)
        self.background = options.get("background", DEFAULT_BACKGROUND)
        self.antialias = options.get("antialias", DEFAULT_ANTIALIAS)
        self.line_spacing = options.get("line_spacing", DEFAULT_LINE_SPACING)
        self.min_size = options.get("min_size", Vector2(1, 1))
        self.max_size = options.get("max_size", Vector2(1_000_000, 1_000_000))
        self.fixed_size = options.get("fixed_size", ...)
        if isinstance(self.fixed_size, Vector2):
            self.min_size = self.max_size = self.fixed_size
        self._font = self.pygame.font.Font(self.font, self.text_size)
        self.cursor = self.pygame.Surface((2, 20), self.pygame.SRCALPHA, 32)
        self.cursor.fill(self.text_color)
        self.cursorPos = 0
        self.cursorLocation = Vector2(0, 0)
        self.cursor_time = time.time()
        self.text_width, self.text_height = self._font.render("t", self.antialias, self.text_color, self.background).get_size()
        self.max_scroll = Vector2(0, 0)
        self.surface = self.pygame.Surface([*self.min_size], self.pygame.SRCALPHA, 32)
        self.surface.fill(self.background)
        self.lines = []
        self.surfaces = []
        self.selection = [None, None]
        self.highlights = []
        self._highlight_offset = []
        self.updateText(text)

    def updateText(self, text:str|None=None, color:list|None=None, bg:list|None=None, antialias:bool|None=None, font:str|None=None, size:int|None=None, line_spacing:int|None=None, min_size:Vector2|None=None, max_size:Vector2|None=None, fixed_size:Vector2|None=None):
        self.font = font or self.font
        self.text_size = size or self.text_size
        self.text = text if text is not None else self.text
        self.antialias = antialias if antialias is not None else self.antialias
        self.text_color = color or self.text_color
        self.background = bg or self.background
        self.line_spacing = line_spacing if line_spacing is not None else self.line_spacing
        self.min_size = min_size or self.min_size
        self.max_size = max_size or self.max_size
        self.fixed_size = fixed_size if fixed_size is not None else self.fixed_size
        if isinstance(self.fixed_size, Vector2):
            self.min_size = self.max_size = self.fixed_size
        if font:
            self._font = self.pygame.font.Font(self.font, self.text_size)
            self.text_width, self.text_height = self._font.render("t", self.antialias, self.text_color, self.background).get_size()
        self.surfaces.clear()
        lines = self.text.split("\n")
        max_width = 0
        height = 0
        for line in lines:
            surface = self._font.render(
                line,
                self.antialias,
                self.text_color,
                self.background
            )
            max_width = max(max_width, surface.get_width())
            height += surface.get_height() + self.line_spacing
            self.surfaces.append(surface)
        self.cursorPos = min(self.cursorPos, len(self.text))
        height -= self.line_spacing
        self.max_scroll.x = max(-1, max_width - self.max_size.x)
        self.max_scroll.y = max(0, height - self.max_size.y)
        sub = self.text[0:self.cursorPos]
        self.cursorLocation.y = sub.count("\n") * self.text_height
        self.cursorLocation.x = len(sub.split("\n")[-1]) * self.text_width
        width = min(max(self.min_size.x, max_width), self.max_size.x)
        height = min(max(self.min_size.y, height), self.max_size.y)
        self.surface = self.pygame.Surface((width, height), self.pygame.SRCALPHA, 32)
        self.surface.fill(self.background)
        y = 0
        for surface in self.surfaces:
            self.surface.blit(surface, [*self.scrolled + [0, y]])
            y += self.line_spacing + surface.get_height()

    def onLeftClick(self, engine):
        relative_pos = engine.mouse.getPosition() - self.getPosition() - self.scrolled
        self.cursor_time = time.time()
        col = mround((relative_pos.x / self.text_width))
        lines = self.text.split("\n")
        line = min(relative_pos.y // self.text_height, len(lines)-1)
        self.cursorPos = len("\n".join(lines[0:line])) + min(col, len(lines[line]))
        if line > 0: self.cursorPos += 1
        
        if self.pygame.K_LSHIFT in engine.keyboard.keys.keys() and (self.selection[0] is not None):
            self.selection[1] = self.cursorPos
        elif self.selection[0] is None:
            self.selection[0] = self.cursorPos
        else:
            self.selection = [self.cursorPos, None]

        self.updateText()

    def focusCursor(self):
        x = (self.getColumn(self.cursorPos) * self.text_width)
        y = (self.getLine(self.cursorPos) * self.text_height) + (self.text_height/2)
        
        width, height = self.max_size
        
        if x + self.scrolled.x < 0:
            diff = x + self.scrolled.x
            self.scrolled.x -= diff
        elif x + self.scrolled.x > width:
            diff = (x - width) + self.scrolled.x
            self.scrolled.x -= diff
        
        if y + self.scrolled.y < 0:
            diff = y + self.scrolled.y
            self.scrolled.y -= diff - (self.text_height*0.5)
        elif y + self.scrolled.y > height:
            diff = (y - height) + self.scrolled.y
            self.scrolled.y -= diff
        
        print(self.scrolled)

    def getLine(self, index):
        return len(self.text[0:index].split("\n"))-1
    
    def getColumn(self, index):
        return len(self.text[0:index].split("\n")[-1])

    def getSelection(self):
        if self.selection[0] is not None and self.selection[1] is not None:
            a = min(*self.selection)
            b = max(*self.selection)
            return self.text[a:b]
        else:
            line = self.getLine(self.cursorPos)
            lines = self.text.split("\n")
            return lines[line] + "\n"

    def setSelection(self, content:str=""):
        if self.selection[0] is not None and self.selection[1] is not None:
            a = min(*self.selection)
            b = max(*self.selection)
            self.text = self.text[0:a] + content + self.text[b:]
            self.cursorPos = min(*self.selection) + len(content)
        else:
            self.text = self.text[0:self.cursorPos] + content + self.text[self.cursorPos:]
            self.cursorPos += len(content)
        self.selection = [None, None]
        self.refresh_selection()

    def refresh_selection(self):
        self.highlights.clear()
        if self.selection[0] is None and self.selection[1] is None:
            return
        
        s_col = self.getColumn(self.selection[0])
        s_line = self.getLine(self.selection[0])
        e_col = self.getColumn(self.selection[1])
        e_line = self.getLine(self.selection[1])

        start_line = min(s_line, e_line)
        end_line = max(s_line, e_line)

        if s_line == e_line:
            start_col = min(s_col, e_col)
            end_col = max(s_col, e_col)
        elif s_line < e_line:
            start_col = s_col
            end_col = e_col
        elif s_line > e_line:
            start_col = e_col
            end_col = s_col

        lines = self.text.split("\n")

        if start_line == end_line:
            line = lines[start_line]
            pre = len(line[0:start_col]) * self.text_width
            self._highlight_offset = [pre, (start_line * self.text_height)]
            s = self.pygame.Surface(((end_col-start_col)*self.text_width, self.text_height), self.pygame.SRCALPHA, 32)
            s.fill(SELECTION_COLOR)
            self.highlights.append(s)
        
        else:
            line = lines[start_line]
            pre = len(line[0:start_col]) * self.text_width
            self._highlight_offset = [pre, (start_line * self.text_height)]
            s = self.pygame.Surface(((len(line[start_col:])+1)*self.text_width, self.text_height), self.pygame.SRCALPHA, 32)
            s.fill(SELECTION_COLOR)
            self.highlights.append(s)
            for l in range(start_line+1, end_line):
                line = lines[l]
                s = self.pygame.Surface(((len(line)+1)*self.text_width, self.text_height), self.pygame.SRCALPHA, 32)
                s.fill(SELECTION_COLOR)
                self.highlights.append(s)
            line = lines[end_line]
            s = self.pygame.Surface(((len(line[0:end_col]))* self.text_width, self.text_height), self.pygame.SRCALPHA, 32)
            s.fill(SELECTION_COLOR)
            self.highlights.append(s)

    def onLeftDown(self, engine):
        relative_pos = engine.mouse.getPosition() - self.getPosition() - self.scrolled
        self.cursor_time = time.time()
        col = mround((relative_pos.x / self.text_width))
        lines = self.text.split("\n")
        line = min(relative_pos.y // self.text_height, len(lines)-1)
        self.cursorPos = len("\n".join(lines[0:line])) + min(col, len(lines[line]))
        if line > 0: self.cursorPos += 1
        
        self.selection[1] = self.cursorPos
        self.refresh_selection()

    def doTyping(self, engine):
        if self.selected:
            self.scrolled += engine.mouse.getScroll() * [120, 60]
            self.scrolled.clamp(*self.max_scroll * [-1, -1], 1, 0)
            for t in engine.keyboard.typing:
                #print(f"key: {t}")
                if t == "$↑":
                    _old = self.cursorPos
                    lines = self.text[0:self.cursorPos].split("\n")
                    x = len(lines[-1])
                    if len(lines) == 1:
                        self.cursorPos = 0
                    else:
                        x2 = len(lines[-2])
                        if x2 < x:
                            self.cursorPos -= 1 + x
                        else:
                            self.cursorPos -= 1 + x2
                            
                    if self.pygame.K_LSHIFT in engine.keyboard.keys.keys() and (self.selection[0] is not None):
                        self.selection[1] = self.cursorPos
                        self.refresh_selection()
                    elif (self.selection[0] is None) and (self.pygame.K_LSHIFT in engine.keyboard.keys.keys()):
                        self.selection[0] = _old
                        self.selection[1] = self.cursorPos
                        self.refresh_selection()
                    elif (self.selection[0] is not None) and (self.selection[1] is not None) and (self.pygame.K_LSHIFT not in engine.keyboard.keys.keys()):
                        self.cursorPos = min(*self.selection)
                        self.selection = [None, None]
                        self.refresh_selection()
                elif t == "$↓":
                    _old = self.cursorPos
                    lines = self.text[0:self.cursorPos].split("\n")
                    after = self.text[self.cursorPos:].split("\n")
                    if len(after) == 1:
                        self.cursorPos = len(self.text)
                    else:
                        x = len(lines[-1])
                        _x = len(after[0])
                        x2 = len(after[1])
                        if x2 < x:
                            self.cursorPos += 1 + x2 + _x
                        else:
                            self.cursorPos += 1 + x + _x
                    if self.pygame.K_LSHIFT in engine.keyboard.keys.keys() and (self.selection[0] is not None):
                        self.selection[1] = self.cursorPos
                        self.refresh_selection()
                    elif (self.selection[0] is None) and (self.pygame.K_LSHIFT in engine.keyboard.keys.keys()):
                        self.selection[0] = _old
                        self.selection[1] = self.cursorPos
                        self.refresh_selection()
                    elif (self.selection[0] is not None) and (self.selection[1] is not None) and (self.pygame.K_LSHIFT not in engine.keyboard.keys.keys()):
                        self.cursorPos = max(*self.selection)
                        self.selection = [None, None]
                        self.refresh_selection()
                elif t == "$→":
                    _old = self.cursorPos
                    self.cursorPos = min(self.cursorPos + 1, len(self.text))
                    if self.pygame.K_LSHIFT in engine.keyboard.keys.keys() and (self.selection[0] is not None):
                        self.selection[1] = self.cursorPos
                        self.refresh_selection()
                    elif (self.selection[0] is None) and (self.pygame.K_LSHIFT in engine.keyboard.keys.keys()):
                        self.selection[0] = _old
                        self.selection[1] = self.cursorPos
                        self.refresh_selection()
                    elif (self.selection[0] is not None) and (self.selection[1] is not None) and (self.pygame.K_LSHIFT not in engine.keyboard.keys.keys()):
                        self.cursorPos = max(*self.selection)
                        self.selection = [None, None]
                        self.refresh_selection()

                elif t == "$←":
                    _old = self.cursorPos
                    self.cursorPos = max(0, self.cursorPos - 1)
                    if self.pygame.K_LSHIFT in engine.keyboard.keys.keys() and (self.selection[0] is not None):
                        self.selection[1] = self.cursorPos
                        self.refresh_selection()
                    elif (self.selection[0] is None) and (self.pygame.K_LSHIFT in engine.keyboard.keys.keys()):
                        self.selection[0] = _old
                        self.selection[1] = self.cursorPos
                        self.refresh_selection()
                    elif (self.selection[0] is not None) and (self.selection[1] is not None) and (self.pygame.K_LSHIFT not in engine.keyboard.keys.keys()):
                        self.cursorPos = min(*self.selection)
                        self.selection = [None, None]
                        self.refresh_selection()
                elif t == "\b":
                    if (self.selection[0] is not None) and (self.selection[1] is not None):
                        self.setSelection()
                    elif self.cursorPos > 0:
                        self.text = self.text[0:self.cursorPos-1] + self.text[self.cursorPos:]
                        self.cursorPos -= 1
                elif t in "\r\n":
                    
                    if self.single_line:
                        self.selected = False
                        engine.mouse.last_selected = None
                    else:
                        if (self.selection[0] is not None) and (self.selection[1] is not None):
                            self.setSelection()
                        else:
                            self.text = self.text[0:self.cursorPos] + "\n" + self.text[self.cursorPos:]
                            self.cursorPos += 1
                elif t == "\t":
                    pre_line = self.text[0:self.cursorPos].split("\n")[-1]
                    if pre_line.strip() == "":
                        p = 4 - (len(pre_line) % 4)
                        self.text = self.text[0:self.cursorPos] + (" "*p) + self.text[self.cursorPos:]
                        self.cursorPos += p
                    else:
                        self.text = self.text[0:self.cursorPos] + "    " + self.text[self.cursorPos:]
                        self.cursorPos += 4
                elif t == "\x03": # CTRL+C
                    pyperclip.copy(self.getSelection())
                elif t == "\x16": # CTRL+V
                    p = pyperclip.paste()
                    if (self.selection[0] is not None) and (self.selection[1] is not None):
                        self.setSelection(p)
                    else:
                        self.text = self.text[0:self.cursorPos] + p + self.text[self.cursorPos:]
                        self.cursorPos += len(p)
                else:
                    if (self.selection[0] is not None) and (self.selection[1] is not None):
                        self.setSelection(t)
                    else:
                        self.text = self.text[0:self.cursorPos] + t + self.text[self.cursorPos:]
                        self.cursorPos += 1
                self.focusCursor()
        self.updateText()

    def update(self, engine):
        pos = self.getPosition()
        screen = self.getScreen()
        
        if self.selection[0] is not None and self.selection[1] is not None and self.highlights:
            h = self.highlights[0]
            x, y = self._highlight_offset
            self.surface.blit(h, [*self.scrolled + pos+[x, y]])
            height = self.text_height
            for h in self.highlights[1:]:
                self.surface.blit(h, [*self.scrolled + pos+[0, y+height]])
                height += self.text_height
        
        if (time.time() - self.cursor_time) % 1 < 0.5 and self.selected:
            self.surface.blit(self.cursor, [*self.scrolled + [*self.cursorLocation - [1, -4]]])
        screen.blit(self.surface, [*pos])
        self.doTyping(engine)
        super().update(engine)
