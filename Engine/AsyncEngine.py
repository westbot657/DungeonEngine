# pylint: disable=[W,R,C,import-error]
from Resources.Logger import Log

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
from Resources.DungeonLoader        import DungeonLoader
from Resources.FunctionMemory       import FunctionMemory
from Resources.TextPattern          import TextPattern
from Resources.EngineOperation      import EngineOperation, _EngineOperation, OpType
from Resources.EngineErrors         import EngineError, EngineBreak, UnknownPlayerError
from Resources.Util                 import Util
from Resources.ConsoleCommands      import ConsoleCommand # import the base class through the file that adds sub classes
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
        self.cmd_queue = []
        self._loaded = False
        self.io_hook = io_hook
        self.is_ui = is_ui
        self.is_console = is_console
        self.loader: DungeonLoader = DungeonLoader()
        #self.function_memory: FunctionMemory = FunctionMemory()
        self._function_memory = FunctionMemory(self)
        FunctionMemory._engine_instance = self
        self.default_input_handler = self._default_input_handler
        self.players: dict[str, Player] = {}
        self.combats: list[Combat] = []
        self.tasks: list[Generator] = []
        self.delays: list = []
        # self.delays2: list = []
        self._player_input_categories = ["common", "global", "world"]
        self._frame_times = [1 for _ in range(60)]
        self._frame_start = 0
        self._frame_end = 0
        self.tps = []
        self.clock = Clock()
        
        Log.engine = self
        #self.default_input_handler.send(None)

    def evaluateFunction(self, data:dict, function_memory:FunctionMemory=None, context_data:dict=None, local_variables:dict=None):
        if function_memory is None:
            function_memory = FunctionMemory(self)
        if context_data:
            function_memory.addContextData(context_data)
        if local_variables:
            function_memory.update(local_variables)
        return self.loader.evaluateFunction(function_memory, data)

    def generatorEvaluateFunction(self, data:dict, function_memory:FunctionMemory=None, context_data:dict=None, local_variables:dict=None):
        if function_memory is None:
            function_memory = FunctionMemory(self)
        if context_data:
            function_memory.addContextData(context_data)
        if local_variables:
            function_memory.update(local_variables)
        ev = self.loader.generatorEvaluateFunction(function_memory, data)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield v
                v = ev.send(res)
        except StopIteration as e:
            v = e.value or (v if not isinstance(v, _EngineOperation) else None)
        return v

    def loadGame(self):
        self.loader.loadGame(self)

        # self.engine_player = Player(
        #     0,
        #     "EnginePlayer",
        #     -1, 0,
        #     Inventory(self._function_memory, []),
        #     Location("world", "rooms/", "start"),
        #     Position(0, 0),
        #     ["%commands%"],
        #     False
        # )
        self.players = self.loader.players
        # self.players.update({0: self.engine_player})
        self._loaded = True

    def saveGame(self):
        if self._loaded:
            self.loader.saveGame(self)
        #Player.saveData(self)
    
    def unloadGame(self):
        if self._loaded:
            self.loader.unloadGame()
            self._loaded = False

            self.sendOutput(4, None)

    def start(self):
        if not self.thread_running:
            t = Thread(target=self._main_loop_threaded)
            t.daemon = True # don't enable this, otherwise the main process ends, taking the engine with it
            self.thread_running = True
            self.running = True
            t.start()
    
    def run(self):
        self.running = True
        self.thread_running = True
        self._main_loop_threaded()

    def stop(self):
        if self.running:
            self.running = False
            self.thread_running = False
            self.saveGame()
            self.unloadGame()

    def pause(self):
        self.running = False

    def handleInput(self, player_id:str|int, text:str):
        # print(f"Engine handle-input: {player_id}: '{text}'")
        if player_id == 0:
            if player_id not in self.input_queue:
                self.input_queue.update({player_id: [self._default_input_handler, self.default_input_handler, text]})
            else:
                self.cmd_queue.append({player_id: [self._default_input_handler, self.default_input_handler, text]})
            return
        
        if player_id not in self.input_queue:
            self.input_queue.update({player_id: [self._default_input_handler, self.default_input_handler, text]})
        else:
            self.input_queue[player_id][2] = text

    def setInputHandler(self, player_id, handler, handler_getter):
        Log["debug"]["engine"](f"Setting input handler for player {player_id}: {handler}")
        self.input_queue.update({player_id: [handler_getter, handler, ""]})

    def resetInputHandler(self, player_id):
        if (player := self.players.get(player_id, None)) is not None:
            player: Player
            player._text_pattern_categories = self._player_input_categories.copy()
            self.input_queue.update({player_id: [self._default_input_handler, self.default_input_handler, ""]})

    def sendOutput(self, target:str|int, text:str):
        self.io_hook.sendOutput(target, text)

    def getPlayer(self, player_id:int, default=...) -> Player:
        if p := Player._loaded.get(player_id, None): return p
        if default is ...: raise EngineError(f"Player does not exist with id: '{player_id}'")
        return default


if __name__ == "__main__":
    ...
