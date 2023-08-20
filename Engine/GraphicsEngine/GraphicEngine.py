# pylint: disable=[W,R,C,import-error,no-member]

try:
    from .GraphicElement import GraphicElement
    from .Keyboard import KeyBoard
    from .Mouse import Mouse
    from .Vector2 import Vector2
    from .MultilineText import MultilineText
except ImportError:
    from GraphicElement import GraphicElement
    from Keyboard import KeyBoard
    from Mouse import Mouse
    from Vector2 import Vector2
    from MultilineText import MultilineText

from threading import Thread

import tkinter
import os
import pyautogui
import pygame

pygame.init()


RESOLUTION = (1920*.75, 1080*.75)

class GraphicEngine(GraphicElement):

    def __init__(self, window_icon=None, window_title=None):
        
        self.mouse = Mouse()
        self.keyboard = KeyBoard()
        self.children = []
        self.parent = self
        self.screen: pygame.Surface = None
        self.window_icon = window_icon
        self.window_title = window_title

        self.running = False

        self.pygame = pygame

    def bringToTop(self, child):
        self.children.remove(child)
        self.children.append(child)

    def getScreen(self) -> pygame.Surface:
        return self.screen

    def getRealPosition(self):
        return Vector2(0, 0)

    def getPosition(self):
        return Vector2(0, 0)

    def getTopParent(self):
        return self

    def setWindowPosition(self, x, y):
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"
        w, h = self.screen.get_size()
        self.pygame.display.set_mode((w, h-1))
        self.pygame.display.set_mode((w, h))

    def getMouseFullPosition(self):
        return [a for a in pyautogui.position()]

    def getWindowPosition(self):
        x, y = self.getMouseFullPosition()
        return [x - self.mouse.x, y - self.mouse.y]

    def update(self):

        self.keyboard.update(self)
        self.mouse.update(self)

        for child in self.children:
            child.update(self)

        self.mouse.post_update(self)
        
        self.keyboard.typing.clear()

    def collides(self, point:Vector2, region:list):
        return region[0] <= point.x <= region[0] + region[2] and region[1] <= point.y <= region[1] + region[3]

    def mouseCollides(self, region:list):
        return self.collides(self.mouse.position, region)

    def _mainloop(self):

        GraphicElement.init(self, pygame)
        MultilineText.init(pygame)

        pygame.display.init()
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE | pygame.SRCALPHA, 32)

        if self.window_icon:
            ico = pygame.image.load(self.window_icon)
            pygame.display.set_icon(ico)
        if self.window_title:
            pygame.display.set_caption(self.window_title)

        while self.running:
            self.screen.fill((0, 0, 0))

            mouse_scrolled = False

            for event in pygame.event.get():
                event: pygame.event.Event
                if event.type == pygame.KEYDOWN:
                    self.keyboard._setKeyDown(event.key)
                    self.keyboard._addUnicode(event.unicode)
                    #print(f"KEYDOWN: {event.key} ({event.unicode})")
                elif event.type == pygame.KEYUP:
                    self.keyboard._setKeyUp(event.key)
                    self.keyboard._removeUnicode(event.unicode)
                    #print(f"KEYUP: {event.key} ({event.unicode})")
                elif event.type == pygame.MOUSEWHEEL:
                    mouse_scrolled = True
                    if self.keyboard.getKeyDown(pygame.K_LSHIFT):
                        self.mouse.xscroll = event.y
                        self.mouse.yscroll = event.x
                    else:
                        self.mouse.xscroll = event.x
                        self.mouse.yscroll = event.y
                    #print(f"MOUSEWHEEL: {self.mouse.xscroll}, {self.mouse.yscroll}")
                elif event.type == pygame.QUIT:
                    pygame.display.quit()
                    self.running = False
                    return
            
            if not mouse_scrolled:
                self.mouse.xscroll, self.mouse.yscroll = 0, 0

            self.mouse._setButtons(*pygame.mouse.get_pressed())
            self.mouse.position.x, self.mouse.position.y = pygame.mouse.get_pos()
            self.update()

            pygame.display.flip()

    def start(self):
        t = Thread(target=self._mainloop)
        self.running = True
        t.start()

    def stop(self):
        self.running = False



if __name__ == "__main__":
    engine = GraphicEngine("./Engine/GraphicsEngine/resources/dungeon_builder_icon.png", "Dungeon Builder")
    engine.start()


    box = GraphicElement.Box(Vector2(10, 10), Vector2(50, 50), [255, 0, 0, 127])
    engine.addChild(box)


    text = GraphicElement.Text(Vector2(200, 20), "Hello", size=20).setDraggable()
    engine.addChild(text)

    text2 = GraphicElement.Text(Vector2(270, 20), "World!", size=20).setDraggable()
    engine.addChild(text2)
    

    def typing(engine, obj, screen):
        if obj.selected:
            for t in engine.keyboard.typing:

                if t == "\b":
                    if len(obj.text) >= 1:
                        obj.updateText(obj.text[0:-1])
                    else:
                        obj.updateText("")
                elif t in "\r\n":
                    obj.selected = False
                elif t in "\t":
                    obj.updateText(obj.text + "    ")
                else:
                    obj.updateText(obj.text + t)

                # print(obj.text)

    text.updater("typing")(typing)
    text2.updater("typing")(typing)


    img = GraphicElement.Image("./Engine/GraphicsEngine/resources/dungeon_builder_icon.png", Vector2(200, 200), 32, 4).setDraggable()
    engine.addChild(img)


    drag = GraphicElement.Box(Vector2(300, 300), Vector2(50, 50), [0, 255, 0, 127])
    corner1 = GraphicElement.Box(Vector2(295, 295), Vector2(6, 6), [255, 255, 0])
    corner2 = GraphicElement.Box(Vector2(351, 351), Vector2(6, 6), [255, 255, 0])
    drag.c1 = corner1
    drag.c2 = corner2
    @drag.updater("resizer")
    def resize(engine, obj, screen):
        obj.c1.update(engine)
        obj.c2.update(engine)
        if obj.held:
            obj.c1.position = obj.position - [3, 3]
            obj.c2.position = obj.position + obj.getSize() - [3, 3]
        else:
            minx = min(obj.c1.position.x + 3, obj.c2.position.x + 3)
            maxx = max(obj.c1.position.x + 3, obj.c2.position.x + 3)
            miny = min(obj.c1.position.y + 3, obj.c2.position.y + 3)
            maxy = max(obj.c1.position.y + 3, obj.c2.position.y + 3)
            obj.position = Vector2(minx, miny)
            size = Vector2(maxx - minx, maxy - miny)
            obj.updateBox(size)
    engine.addChild(drag.setDraggable())
    engine.addChild(corner1.setDraggable())
    engine.addChild(corner2.setDraggable())


    mtext = MultilineText(Vector2(20, 300), "Hello,\nthis is a\n     test!!!!!", True, text_size=20, background=[31, 31, 31])
    engine.addChild(mtext)

    # @mtext.updater("typing")
    # def typing2(engine, obj, screen):
    #     if obj.selected:
    #         for t in engine.keyboard.typing:

    #             if t == "\b":
    #                 if len(obj.text) >= 1:
    #                     obj.updateText(obj.text[0:-1])
    #                 else:
    #                     obj.updateText("")
    #             elif t in "\r\n":
    #                 obj.updateText(obj.text + "\n")
    #             elif t in "\t":
    #                 obj.updateText(obj.text + "    ")
    #             else:
    #                 obj.updateText(obj.text + t)

