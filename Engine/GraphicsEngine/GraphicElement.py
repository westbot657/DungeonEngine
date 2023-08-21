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
    DEFAULT_COLOR = text_config["color"]
    DEFAULT_BACKGROUND = text_config["background"]
    DEFAULT_ANTIALIAS = text_config["antialias"]


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

        self.draggable = False
        self.clickable = False
        self.hoverable = False

        self.held = False
        self.hovered = False
        self.selected = False

        self._type: GraphicElement.Type = None

        self._updaters = {}

    def setDraggable(self):
        self.draggable = True
        self.clickable = True
        self.hoverable = True
        return self
    
    def setClickable(self):
        self.clickable = True
        self.hoverable = True
        return self
    
    def setHoverable(self):
        self.hoverable = True
        return self

    def bringToTop(self, child):
        self.children.remove(child)
        self.children.append(child)
        self.parent.bringToTop()

    def updater(self, _id):
        def wrapper(method):
            self._updaters.update({_id: method})
        return wrapper

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def removeChild(self, child):
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def getTopParent(self):
        return self.parent.getTopParent()

    def getScreen(self):
        return self.parent.getScreen()

    def getRealPosition(self) -> Vector2:
        parent_pos = self.parent.getRealPosition()
        return self.position + parent_pos

    def getPosition(self) -> Vector2:
        parent_pos = self.parent.getPosition()
        return self.position + parent_pos

    def setPosition(self, position:Vector2):
        self.position = position

    def getSize(self) -> Vector2:
        return Vector2(*self.surface.get_size())

    def onLeftClick(self, engine):
        pass

    def onRightClick(self, engine):
        pass
    
    def onLeftDown(self, engine):
        pass

    def update(self, engine):
        pos = self.getPosition()
        screen = self.getScreen()

        for updater in self._updaters.values():
            updater(engine, self, screen)

        if self.hoverable:
            size = self.getSize()
            
            if engine.mouseCollides([*pos, *size]):
                engine.mouse.hovering = self
                if self.clickable:
                    if engine.mouse.onLeftClick():
                        engine.mouse.setClicked(self)
                        if self.draggable:
                            engine.mouse.hold_offset = [*(engine.mouse.getPosition() - pos)]
                            engine.mouse.holding_obj = True
                            engine.mouse.held_obj = self
                        else:
                            self.onLeftClick(engine)
                    elif engine.mouse.left_button:
                        self.onLeftDown(engine)
                    if engine.mouse.onRightClick():
                        engine.mouse.setClicked(self)
                        self.onRightClick(engine)
            else:
                self.hovered = False

        if self._type == GraphicElement.Type.TEXT:
            screen.blit(self.surface, list(pos))

        elif self._type == GraphicElement.Type.IMAGE:
            self.getFrame()
            screen.blit(self.surface, list(pos))

        elif self._type == GraphicElement.Type.BOX:
            screen.blit(self.surface, list(pos))

        for child in self.children:
            child.update(engine)

    def updateText(self, text:str|None=None, color:list|None=None, bg:list|None=None, antialias:bool|None=None, font:str|None=None, size:int|None=None):
        if self._type != GraphicElement.Type.TEXT:
            raise Exception("Cannot update text for non-text element")
        
        self.font = font or self.font
        self.size = size or self.size
        self.text = text if text is not None else self.text
        self.antialias = antialias if antialias is not None else self.antialias
        self.color = color or self.color
        self.background = bg or self.background

        _font = self.pygame.font.Font(self.font, self.size)

        self.surface = _font.render(
            self.text,
            self.antialias,
            self.color,
            self.background
        )

    def updateBox(self, size:Vector2|None=None, color:list|None=None):
        if self._type != GraphicElement.Type.BOX:
            raise Exception("Cannot update size and color for non-box element")

        box = self.pygame.Surface(list(size or self.size), self.pygame.SRCALPHA, 32)
        box.fill((color or self.color)[0:3])
        
        self.surface = box

    @classmethod
    def Text(cls, position:Vector2, text:str, textColor:list=DEFAULT_COLOR, backgroundColor:list=DEFAULT_BACKGROUND, antialias:bool=DEFAULT_ANTIALIAS, font:str=DEFAULT_FONT, size:int=DEFAULT_TEXTSIZE):
        _font = cls.pygame.font.Font(font, size)
        obj = cls(_font.render(text, antialias, textColor, backgroundColor), position)
        obj.font = font
        obj.size = size
        obj.text = text
        obj.antialias = antialias
        obj.color = textColor
        obj.background = backgroundColor
        obj._type = GraphicElement.Type.TEXT
        obj.text_width, obj.text_height = _font.render("t", antialias, textColor, backgroundColor).get_size()
        return obj

    

    def getFrame(self):
        self._img: self.pygame.Surface
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

        self.surface = self.pygame.transform.scale(self._img.subsurface((0, h*self.current_frame, w, h)), [*self.scale * [w, h]])

    @classmethod
    def Image(cls, file_name:str, position:Vector2, frame_height:int, scale:int|Vector2=1):
        

        if isinstance(scale, (int, float)):
            scale = Vector2(scale, scale)

        if os.path.exists(f"./{file_name}.json"):
            with open(f"./{file_name}.json", "r+", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {
                "frames": [0],
                "fps": 0
            }
        
        img = cls.pygame.image.load(f"./{file_name}")

        obj = cls(img, position)
        obj._img = img
        obj.config = config
        obj.frame_time = time.time()
        obj.current_frame = 0
        obj.frame_height = frame_height
        obj._type = GraphicElement.Type.IMAGE
        obj.scale = scale

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

