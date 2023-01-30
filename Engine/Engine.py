# pylint: disable=[W,R,C,import-error]
from Resources.AbstractAmmo         import AbstractAmmo, Ammo
from Resources.AbstractArmor        import AbstractArmor, Armor
from Resources.AbstractCombat       import AbstractCombat, Combat
from Resources.AbstractItem         import AbstractItem, Item
from Resources.LootTable            import LootTable, LootPool, LootEntry
from Resources.AbstractStatusEffect import AbstractStatusEffect, StatusEffect
from Resources.AbstractWeapon       import AbstractWeapon, Weapon
from Resources.Identifier           import Identifier
from Resources.DungeonLoader        import DungeonLoader
from Resources.FunctionMemory       import FunctionMemory

from threading import Thread

import glob, json, re
import asyncio

class Engine:
    _engine = None
    def __new__(cls, *args, **kwargs):
        if not cls._engine:
            cls._engine = self = super().__new__(cls)
            self.init(*args, **kwargs)
        return cls._engine

    def init(self, io_hook):
        self.running = False
        self.thread_running = False
        self.input_queue = {}
        self.io_hook = io_hook
        self.loader: DungeonLoader = DungeonLoader()
        self.function_memory: FunctionMemory = FunctionMemory()

    def evaluateFunction(self, data:dict):
        return self.loader.evaluateFunction(self, data)

    def loadGame(self):
        self.loader.loadGame(self)

    def saveGame(self):
        self.loader.saveGame(self)

    def start(self):
        if not self.thread_running:
            t = Thread(target=self._main_loop_threaded)
            self.thread_running = True
            self.running = True
            t.start()
    
    def stop(self):
        self.running = False
        self.thread_running = False

    def pause(self):
        self.running = False

    def handleInput(self, player_id:str|int, text:str):
        if player_id not in self.input_queue:
            self.input_queue.update({player_id: [None, text]})

    def sendOutput(self, target:str|int, text:str):
        self.io_hook.sendOutput(target, text)

    def _main_loop_threaded(self):
        self.io_hook.init(self)
        self.io_hook.start()
        while self.thread_running:
            if not self.running:
                # Pause Menu thingy?
                continue
            # Main Loop

            # check inputs
            for player_id, [response_handler, text] in self.input_queue.items():
                player_id: int|str
                text: str
                if text:
                    if response_handler:
                        ...
                    

        self.io_hook.stop()

if __name__ == "__main__":
    def test():
        target = "user"

        while True:
            response = yield target, "some message to reply to"

            if response == "yes":
                print("yay")
                return
            elif response == "no":
                response = yield target, "why not?"
                ...
                return

    t = test()

    while t:
        i = input()
        ret = t.send(i)
        print(ret)
