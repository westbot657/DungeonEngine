# pylint: disable=[W,R,C,import-error]

from Resources.Logger import Log

import sys, os

Log._tag_colors = {
    "loadup": "\u001b[38;2;10;200;80m",
    "player": "\u001b[38;2;10;40;180m",
    "loader": "\u001b[38;2;200;200;10m",
    "ERROR": "\u001b[38;2;255;0;0m",
    "WARNING": "\u001b[38;2;255;127;0m",
    "abstract": "\u001b[38;2;100;100;100m",
    "object": "\u001b[38;2;200;200;200m",
    "inventory": "\u001b[38;2;0;100;100m",
    "dungeon": "\u001b[38;2;0;180;30m",
    "evaluate-result": "\u001b[38;2;255;0;0m",
    "engine script": "\u001b[38;2;127;255;10m",
    "debug": "\u001b[38;2;10;110;10m",
    "engine": "\u001b[38;2;255;215;0m"
}

Log.log_to_file("./latest.log")

sys.path.append(os.getcwd())


from Resources.AbstractAmmo         import AbstractAmmo, Ammo
from Resources.AbstractArmor        import AbstractArmor, Armor
from Resources.AbstractCombat       import AbstractCombat, Combat
from Resources.AbstractItem         import AbstractItem, Item
from Resources.LootTable            import LootTable, LootPool
from Resources.AbstractStatusEffect import AbstractStatusEffect, StatusEffect
from Resources.AbstractWeapon       import AbstractWeapon, Weapon
from Resources.Inventory            import Inventory
from Resources.Location             import Location
from Resources.Identifier           import Identifier
from Resources.Player               import Player
from Resources.EngineErrors         import EngineError, EngineBreak, UnknownPlayerError
from Resources.Util                 import Util
from Resources.Position             import Position

from threading import Thread
# from multiprocessing import Process


from typing import Any, Generator, Callable
import time
import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame.time import Clock
#import asyncio


class Engine:
    
    _engine = None

    def __new__(cls, *args, **kwargs):
        if not cls._engine:
            cls._engine = self = super().__new__(cls)
            self.init(*args, **kwargs)
        return cls._engine

    def init(self, io_hook, is_ui=False, is_console=False):
        self.running = False
        self.thread_running = False
        self.input_queue = {}
        self._loaded = False
        self.players: dict[str, Player] = {}
        self.combats: list[Combat] = []
        
        self.io_hook = io_hook
        self.is_ui = is_ui
        self.is_console = is_console

        self.clock = Clock()
        Log.engine = self

    def loadGame(self):
        pass
    
    def saveGame(self):
        pass
    
    def start(self):
        if not self.thread_running:
            t = Thread(target=self.mainloop)
            t.daemon = True
            self.thread_running = True
            self.running = True
            t.start()

    def run(self):
        self.running = True
        self.thread_running = True
        self.mainloop()
    
    def stop(self):
        pass
    
    def pause(self):
        self.running = False

    def mainloop(self):
        
        self.io_hook.init(self)
        
        self.io_hook.start()
        self.loadGame()
        
        # TODO: move players to their saved location
        
        while self.thread_running:
            
            self.tps = self.clock.get_fps()
            
            
            self.clock.tick(60)
        

