# pylint: disable=[W,R,C,import-error]

try:
    from .Vector2 import Vector2
except ImportError:
    from Vector2 import Vector2

import json

with open("./Engine/GraphicsEngine/defaults.json", "r+", encoding="utf-8") as f:
    text_config = json.load(f)["text"]

    DEFAULT_FONT = text_config["font"]
    DEFAULT_TEXTSIZE = text_config["size"]
    DEFAULT_COLOR = []


class GraphicElement:

    pygame = None

    @classmethod
    def init(cls, engine, pygame):

        cls.pygame = pygame

        cls.engine = engine
        pygame.font.init()
        

    def __init__(self, surface, position:Vector2):
        self.surface = surface
        self.position = position
        self.parent = None
        self.children = []

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def removeChild(self, child):
        if child in self.children:
            child.parent = None
            self.children.pop(child)

    def update(self):
        ...


    @classmethod
    def Text(cls, text, textColor=DEFAULT_COLOR, font=DEFAULT_FONT, size=DEFAULT_TEXTSIZE):
        color = cls.pygame.Color(*textColor)
        


    @classmethod
    def Image(cls)





