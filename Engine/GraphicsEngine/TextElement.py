# pylint: disable=[W,R,C,import-error]

try:
    from .VisualElement import VisualElement
    from .Util import Vector2d
except ImportError:
    from VisualElement import VisualElement
    from Util import Vector2d

from pygame import Surface, font as pygameFont, Color

pygameFont.init()

class TextElement(VisualElement):

    def __init__(self, parent, text:str, font:str, text_size:int, text_color:Color=None, background:Color=None):
        super().__init__(parent)
        self.text = text
        self._fontname = font or pygameFont.get_default_font()
        self._text_size = text_size
        self._font = pygameFont.Font(self._fontname, self._text_size)
        self._text_color = text_color
        self._background = background
        self._surface = self._font.render(text, True, text_color, background)

    def setText(self, text:str):
        self.text = text
        self._surface = self._font.render(self.text, True, self._text_color, self._background)

    def setTextColor(self, color:Color):
        self._text_color = color
        self._surface = self._font.render(self.text, True, self._text_color, self._background)

    def setBackgroundColor(self, color:Color):
        self._background = color
        self._surface = self._font.render(self.text, True, self._text_color, self._background)

    def setTextSize(self, size:int):
        self._text_size = size
        self._font = pygameFont.Font(self._fontname, self._text_size)
        self._surface = self._font.render(self.text, True, self._text_color, self._background)

    def setFont(self, font_name:str):
        self._fontname = font_name
        self._font = pygameFont.Font(self._fontname, self._text_size)
        self._surface = self._font.render(self.text, True, self._text_color, self._background)


    def getText(self) -> str:
        return self.text

    def getTextColor(self) -> Color:
        return self._text_color

    def getTextSize(self) -> int:
        return self._text_size
    
    def getBackgroundColor(self) -> Color:
        return self._background

    def getFont(self) -> str:
        return self._fontname


    def getWidth(self) -> int:
        return super().getWidth()
    
    def getHeight(self) -> int:
        return super().getHeight()
    
    def getSurface(self) -> Surface:
        return super().getSurface()

    def update(self, engine, surface, relativePosition: Vector2d):
        return super().update(engine, surface, relativePosition)

