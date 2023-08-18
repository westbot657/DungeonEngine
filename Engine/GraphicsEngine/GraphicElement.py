# pylint: disable=[W,R,C,import-error,no-member]

try:
    from .Vector2 import Vector2
except ImportError:
    from Vector2 import Vector2

from enum import Enum, auto

import json, os, time


with open("./Engine/GraphicsEngine/defaults.json", "r+", encoding="utf-8") as f:
    text_config = json.load(f)["text"]

    DEFAULT_FONT = text_config["font"]
    DEFAULT_TEXTSIZE = text_config["size"]
    DEFAULT_COLOR = []
    DEFAULT_BACKGROUND = []


class GraphicElement:

    class Type(Enum):
        IMAGE = auto()
        BOX = auto()
        TEXT = auto()

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

        self._type: GraphicElement.Type = None

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def removeChild(self, child):
        if child in self.children:
            child.parent = None
            self.children.pop(child)

    def update(self, engine):
        offset: Vector2 = self.parent.getOffset()
        screen = self.parent.getScreen()

        if self._type == GraphicElement.Type.TEXT:
            ...
        elif self._type == GraphicElement.Type.IMAGE:
            self.getFrame()

        elif self._type == GraphicElement.Type.BOX:
            ...


    @classmethod
    def Text(cls, position:Vector2, text:str, textColor:list=DEFAULT_COLOR, backgroundColor:list=DEFAULT_BACKGROUND, antialias:bool=False, font:str=DEFAULT_FONT, size:int=DEFAULT_TEXTSIZE):
        color = cls.pygame.Color(*textColor)
        bg = cls.pygame.Color(*backgroundColor)

        _font = cls.pygame.font.Font(font, size)
        
        obj = cls(_font.render(text, antialias, color, bg), position)

        obj.text = text
        obj.antialias = antialias
        obj.color = color
        obj.background = bg
        
        obj._type = GraphicElement.Type.TEXT

        return obj

    def getFrame(self):
        import pygame
        self._img: pygame.Surface
        w = self._img.get_width()
        h = self.frame_height
        ft = self.frame_time
        self.frame_time = time.time()
        dt = self.frame_time - ft
        fps = self.config["fps"]

        if fps > 0:
            f_advance = dt // fps
        
            self.current_frame += f_advance
            while self.current_frame >= len(self.config["frames"]):
                self.current_frame -= len(self.config["frames"])

        self.surface = self._img.subsurface((0, h*self.current_frame, w, h))


    @classmethod
    def Image(cls, file_name:str, position:Vector2, frame_height:int):
        import pygame

        if os.path.exists(f"./{file_name}.json"):
            with open(f"./{file_name}.json", "r+", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {
                "frames": [0],
                "fps": 0
            }
        
        img = pygame.image.load(f"./{file_name}")

        obj = cls(img, position)
        obj._img = img
        obj.config = config
        obj.frame_time = time.time()
        obj.current_frame = 0
        obj.frame_height = frame_height
        obj._type = GraphicElement.Type.IMAGE

        obj.getFrame()
        return obj

    @classmethod
    def Box(cls, position:Vector2, size:Vector2, color:list):
        col = cls.pygame.Color(*color)
    
        box = cls.pygame.Surface(list(size), cls.pygame.SRCALPHA, 32)
        box.fill(col)

        obj = cls(box, position)

        obj.color = col
        obj.size = size
        obj._type = GraphicElement.Type.BOX

        return obj

