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

import pyperclip
import os, sys
import pyautogui
import pygame
import time
import random
import re
from subprocess import Popen

pygame.init()


RESOLUTION = [1920*.75, 1080*.75]

class GraphicEngine(GraphicElement):

    keys = {
        pygame.K_UP: "$↑",
        pygame.K_RIGHT: "$→",
        pygame.K_DOWN: "$↓",
        pygame.K_LEFT: "$←"
    }

    def __init__(self, window_icon=None, window_title=None):
        
        self.mouse = Mouse()
        self.keyboard = KeyBoard()
        self.children = []
        self.parent = self
        self.screen: pygame.Surface = None
        self.window_icon = window_icon
        self.window_title = window_title

        self.running = False
        
        GraphicElement.init(self, pygame)
        MultilineText.init(pygame)

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
        global RESOLUTION

        pygame.display.init()
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE | pygame.SRCALPHA, 32)
        #self.screen = pygame.Surface(RESOLUTION, pygame.SRCALPHA, 32)

        if self.window_icon:
            ico = pygame.image.load(self.window_icon)
            pygame.display.set_icon(ico)
        if self.window_title:
            pygame.display.set_caption(self.window_title)

        while self.running:
            self.screen.fill((0, 0, 0))
            # self._screen.fill((0, 0, 0))
            mouse_scrolled = False

            for event in pygame.event.get():
                event: pygame.event.Event
                if event.type == pygame.KEYDOWN:
                    self.keyboard._setKeyDown(event.key)
                    if event.unicode:
                        self.keyboard._addUnicode(event.unicode)
                    else:
                        self.keyboard._addUnicode(self.keys.get(event.key, None))
                    #print(f"KEYDOWN: {event.key} ({event.unicode})")
                elif event.type == pygame.KEYUP:
                    self.keyboard._setKeyUp(event.key)
                    if event.unicode:
                        self.keyboard._removeUnicode(event.unicode)
                    else:
                        self.keyboard._removeUnicode(self.keys.get(event.key, None))
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
                    break
                elif event.type == pygame.VIDEORESIZE:
                    RESOLUTION = [*event.dict['size']]
            else:

                if not mouse_scrolled:
                    self.mouse.xscroll, self.mouse.yscroll = 0, 0

                self.mouse._setButtons(*pygame.mouse.get_pressed())
                self.mouse.position.x, self.mouse.position.y = pygame.mouse.get_pos()
                self.update()

                # self._screen.blit(
                # pygame.transform.scale(self.screen, self._resolution), (0, 0)#, self._screen
                # )

                pygame.display.update()
                continue
            
            sys.exit()
            
        sys.exit()

    def start(self):
        t = Thread(target=self._mainloop)
        self.running = True
        t.start()

    def stop(self):
        self.running = False

# 38  79 120
# 31  31  31
#  7  48  89
# 69 110 151

PATH = "./Engine/GraphicsEngine/resources/"

class Button(GraphicElement):
    def __init__(self, position:Vector2, button_text:str):
        self.position = position
        self.parent = None
        self.text = GraphicElement.Text(Vector2(self.position.x, 0), button_text, size=40)
        self.width, self.height = self.text.getSize() + [4, 4]
        
        self.bg = GraphicElement.Image(f"{PATH}dungeon_game_icon.png", Vector2(self.position.x, 0), 32)
        self.bg.frame_height = self.height
        self.bg._img = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.bg._img.fill((0, 0, 0, 0))
        self.bg._img.fill([125, 125, 125], (2, 0, self.width-4, 1))
        self.bg._img.fill([125, 125, 125], (1, 1, self.width-2, 1))
        self.bg._img.fill([125, 125, 125], (0, 2, self.width, self.height-4))
        self.bg._img.fill([125, 125, 125], (1, self.height-2, self.width-2, 1))
        self.bg._img.fill([125, 125, 125], (2, self.height-1, self.width-4, 1))
        
        super().__init__(pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32), self.position)

        self.frame = GraphicElement.Image(f"{PATH}dungeon_game_icon.png", Vector2(self.position.x, 0), 32)
        self.frame.frame_height = self.height
        self.frame._img = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.frame._img.fill((0, 0, 0, 0))
        self.frame._img.fill([28, 160, 0], (2, 0, self.width-4, 1))
        self.frame._img.fill([28, 160, 0], (1, 1, 1, 1))
        self.frame._img.fill([28, 160, 0], (self.width-2, 1, 1, 1))
        self.frame._img.fill([28, 160, 0], (0, 2, 1, self.height-4))
        self.frame._img.fill([28, 160, 0], (self.width-1, 2, 1, self.height-4))
        self.frame._img.fill([28, 160, 0], (1, self.height-2, 1, 1))
        self.frame._img.fill([28, 160, 0], (self.width-2, self.height-2, 1, 1))
        self.frame._img.fill([28, 160, 0], (2, self.height-1, self.width-4, 1))
        self.frame._img.set_alpha(0)

        self.fill = GraphicElement.Image(f"{PATH}dungeon_game_icon.png", Vector2(self.position.x, 0), 32)
        self.fill.frame_height = self.height
        self.fill._img = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.fill._img.fill((0, 0, 0, 0))
        self.fill._img.fill([45, 127, 0], (2, 1, self.width-4, 1))
        self.fill._img.fill([45, 127, 0], (1, 2, self.width-2, self.height-4))
        self.fill._img.fill([45, 127, 0], (2, self.height-4, self.width-2, 1))
        self.fill._img.set_alpha(0)

        # self.hoverable = self.clickable = True
        self.hover_tick = 0
        self.bg.setClickable()
        self.addChild(self.bg)
        self.addChild(self.frame)
        self.addChild(self.fill)
        self.addChild(self.text)

        self.bg.updater("hover updater")(self.bg_updater)

    def bg_updater(self, engine, _, screen):
        if self.bg.hovered:
            # print("hovered")
            if self.hover_tick < 255:
                self.hover_tick = min(self.hover_tick+5, 255)
                self.fill._img.set_alpha(self.hover_tick*0.75)
                # self.fill.getFrame()
            self.frame._img.set_alpha(255)
        else:
            # print("not hovered")
            self.frame._img.set_alpha(0)
            if self.hover_tick > 0:
                self.hover_tick = max(0, self.hover_tick-5)
                self.fill._img.set_alpha(self.hover_tick*0.75)
                # self.fill.getFrame()
            

    def onClick(self):
        def wrapper(func):
            self.bg.onLeftClick = func
        return wrapper

if __name__ == "__main__":
    engine = GraphicEngine(f"{PATH}dungeon_game_icon.png", "Insert Dungeon Name Here")
    engine.start()

    title = GraphicElement.Text(Vector2(0, 0), "<Insert Dungeon Name Here>", [255, 255, 255], size=30)
    title.setPosition(Vector2((RESOLUTION[0]-title.getSize().x)/2, RESOLUTION[1]/4))
    engine.addChild(title)


    logo = GraphicElement.Image(f"{PATH}dungeon_game_icon.png", Vector2(RESOLUTION[0]/2, RESOLUTION[1]/2), 32, 1)
    engine.addChild(logo)
    
    frame = 0
    tick = 0
    size = 1/32
    state = "load"
    @logo.updater("fade in")
    def fade_in(engine, obj, screen):
        global frame, tick, size, title, state
        tick += 1
        title.setPosition(Vector2((RESOLUTION[0]-title.getSize().x)/2, RESOLUTION[1]/4))
        obj.setPosition(Vector2((RESOLUTION[0] - size*32)/2, (RESOLUTION[1] - size*32)/2))
        if frame > 255:
            if tick >= 500:
                state = "load2"
                tick = 255
            return
        if tick >= 5:
            frame += 1
            size += 1/32
            tick = 0
            
            obj.scale = Vector2(size, size)
            obj._img.set_alpha(frame)
            
            title.surface.set_alpha(frame)

    while state == "load": time.sleep(1)
    
    logo._updaters.pop("fade in")
    
    @logo.updater("fade")
    def fade(engine, obj, screen):
        global tick, state, size
        
        title.setPosition(Vector2((RESOLUTION[0]-title.getSize().x)/2, RESOLUTION[1]/4))
        obj.setPosition(Vector2((RESOLUTION[0] - size*32)/2, (RESOLUTION[1] - size*32)/2))
        
        tick -= 5
        obj._img.set_alpha(tick)
        title.surface.set_alpha(tick)
        if tick <= 0:
            state = "select"
    
    while state == "load2": time.sleep(1)
    logo._updaters.pop("fade")
    engine.removeChild(title)

    launch_game = Button(Vector2(0, 0), "Launch Game")
    launch_editor = Button(Vector2(0, 0), "Launch Editor")
    logo._img.set_alpha(255)
    
    engine.addChild(launch_game)
    engine.addChild(launch_editor)
    
    state2 = ""
    
    @launch_game.updater("positioning")
    def position(engine, obj, screen):
        size = obj.getSize()
        obj.position.x = (RESOLUTION[0]/3) - (size.x/2)
        obj.position.y = (RESOLUTION[1]*2/3) - (size.y/2)
    
    @launch_game.onClick()
    def on_click_game(engine):
        global state, state2
        state = "fade"
        state2 = "game"
    @launch_editor.onClick()
    def on_click_editor(engine):
        global state, state2
        state = "fade"
        state2 = "editor"
    @launch_editor.updater("positioning")
    def position2(engine, obj, screen):
        size = obj.getSize()
        obj.position.x = (RESOLUTION[0]*2/3) - (size.x/2)
        obj.position.y = (RESOLUTION[1]*2/3) - (size.y/2)
    @logo.updater("positioning")
    def position3(engine, obj, screen):
        size = obj.getSize()
        obj.position.x = (RESOLUTION[0]-size.x)/2
        obj.position.y = RESOLUTION[1]*1/4
    
    # mtext = MultilineText(Vector2(RESOLUTION[0]/2, 0), open("./Engine/GraphicsEngine/GraphicEngine.py", "r+", encoding="utf-8").read(), True, text_size=20, background=[31, 31, 31], fixed_size=Vector2(RESOLUTION[0]/2, RESOLUTION[1]))
    # engine.addChild(mtext)
    # engine.addChild(b.bg)

    while state == "select": time.sleep(1)

    fade_box = GraphicElement.Box(Vector2(0, 0), Vector2(*RESOLUTION), [0, 0, 0, 0])
    engine.addChild(fade_box)
    tick = 0
    @fade_box.updater("fade")
    def fade2(engine, obj, sreen):
        global tick, state, state2
        tick += 5
        fade_box.updateBox(size=Vector2(*RESOLUTION), color=[0, 0, 0, tick])
        if tick >= 255:
            state = state2
            obj._updaters.pop("fade")
    
    while state == "fade": time.sleep(1)

    engine.removeChild(logo)
    engine.removeChild(launch_game)
    engine.removeChild(launch_editor)
    engine.removeChild(fade_box)

    if state == "game":

        engine.stop()
        pygame.quit()
        p = Popen("py -3.10 ./Engine/ConsoleRunner.py", shell=True)
        sys.exit()
    else:
        test = MultilineText(Vector2(0, 0), open("./resources/tools/scripts/fishing_rod/on_use.ds", "r+", encoding="utf-8").read(), True, text_size=14, fixed_size=Vector2(*RESOLUTION), background=[31, 31, 31])
        
        ec_highlighting = [
            [r"\b(if|elif|else|return|break|pass)\b", "\033[38;2;197;134;192m\\1\033[0m"],
            [r"\b(true|false|none|and|or)\b", "\033[38;2;86;156;214m\\1\033[0m"],
            ["(//[^\n]*)", "\033[38;2;106;153;85m\\1\033[0m"],
            [r"(\[)([^:\[\]]+:)((?:[^/\[\]]+/)*)([^\[\]]+)(\])", "\\1\033[38;2;86;156;214m\\2\033[38;2;156;220;254m\\3\033[38;2;220;220;170m\\4\033[0m\\5"],
            [r"(\"(?:\\.|[^\"\\])*\")", "\033[38;2;206;145;120m\\1\033[0m"],
            [r"((?<!<)%|@[^:]*:)", "\033[38;2;79;193;255m\\1\033[0m"],
            [r"(\d+(?:\.\d+)?|\.\d+)", "\033[38;2;181;206;168m\\1\033[0m"],
            [r"(<)([^#\$%][^>]*)(>)", "\\1\033[38;2;78;201;176m\\2\033[0m\\3"],
            [r"(<)(#[^>]*)(>)", "\\1\033[38;2;209;105;105m\\2\033[0m\\3"],
            [r"(<)(\$[^>]*)(>)", "\\1\033[38;2;220;220;170m\\2\033[0m\\3"],
            [r"(<)(%[^>]*)(>)", "\\1\033[38;2;79;193;255m\\2\033[0m\\3"],
        ]

        @test.updater("highliting")
        def ec_highlight(engine, obj, screen):
            t = obj.text


            for pattern, rep in ec_highlighting:
                t = re.sub(pattern, rep, t)


            obj._raw_text = t

        engine.addChild(test)



