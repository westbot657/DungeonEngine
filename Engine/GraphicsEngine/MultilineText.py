# pylint: disable=[W,R,C,import-error,no-member]

try:
    from .GraphicElement import GraphicElement
    from .Vector2 import Vector2
except ImportError:
    from GraphicElement import GraphicElement
    from Vector2 import Vector2

import json, time

with open("./Engine/GraphicsEngine/defaults.json", "r+", encoding="utf-8") as f:
    text_config = json.load(f)["text"]

    DEFAULT_FONT = text_config["font"]
    DEFAULT_TEXTSIZE = text_config["size"]
    DEFAULT_COLOR = text_config["color"]
    DEFAULT_BACKGROUND = text_config["background"]
    DEFAULT_ANTIALIAS = text_config["antialias"]
    DEFAULT_LINE_SPACING = text_config["line spacing"]

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
        """


        self.position = position
        self.text = text
        self.writable = writable
        self.hoverable = self.writable
        self.clickable = self.writable
        self.draggable = False

        self.held = False
        self.hovered = False
        self.selected = False

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

        self._font = self.pygame.font.Font(self.font, self.text_size)
        self.cursor = self.pygame.Surface((2, 20), self.pygame.SRCALPHA, 32)
        self.cursor.fill(self.text_color)

        self.cursorPos = Vector2(0, 0)
        self.cursor_time = time.time()

        self.text_width = self._font.render("t", self.antialias, self.color, self.background).get_width()

        self.surface = self.pygame.Surface([*self.min_size], self.pygame.SRCALPHA, 32)
        self.surface.fill(self.background)

        self.lines = []
        self.surfaces = []

        self.highlighted = []

        self.updateText(text)


    def updateText(self, text:str|None=None, color:list|None=None, bg:list|None=None, antialias:bool|None=None, font:str|None=None, size:int|None=None, line_spacing:int|None=None, min_size:Vector2|None=None, max_size:Vector2|None=None):

        self.font = font or self.font
        self.text_size = size or self.text_size
        self.text = text if text is not None else self.text
        self.antialias = antialias if antialias is not None else self.antialias
        self.text_color = color or self.text_color
        self.background = bg or self.background
        self.line_spacing = line_spacing if line_spacing is not None else self.line_spacing
        self.min_size = min_size or self.min_size
        self.max_size = max_size or self.max_size


        if font:
            self._font = self.pygame.font.Font(self.font, self.text_size)
            self.text_width = self._font.render("t", self.antialias, self.color, self.background).get_width()

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

        self.cursorPos = Vector2.min(self.cursorPos, Vector2(len(self.lines[-1])*self.text_width, height-self.text_size))

        height -= self.line_spacing

        width = min(max(self.min_size.x, max_width), self.max_size.x)
        height = min(max(self.min_size.y, height), self.max_size.y)

        self.surface = self.pygame.Surface((width, height), self.pygame.SRCALPHA, 32)
        self.surface.fill(self.background)

        y = 0
        for surface in self.surfaces:
            self.surface.blit(surface, (0, y))
            y += self.line_spacing + surface.get_height()

    def onLeftClick(self, engine):
        relative_pos = engine.mouse.getPosition() - self.getPosition()



    def doTyping(self, engine):
        if self.selected:
            for t in engine.keyboard.typing:
                ...


    def update(self, engine):
        pos = self.getPosition()
        screen = self.getScreen()

        screen.blit(self.surface, [*pos])

        super().update(engine)

