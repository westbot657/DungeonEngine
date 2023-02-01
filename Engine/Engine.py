# pylint: disable=[W,R,C,import-error]
from Resources.AbstractAmmo         import AbstractAmmo, Ammo
from Resources.AbstractArmor        import AbstractArmor, Armor
from Resources.AbstractCombat       import AbstractCombat, Combat
from Resources.AbstractItem         import AbstractItem, Item
from Resources.LootTable            import LootTable, LootPool, LootEntry
from Resources.AbstractStatusEffect import AbstractStatusEffect, StatusEffect
from Resources.AbstractWeapon       import AbstractWeapon, Weapon
from Resources.Identifier           import Identifier
from Resources.Player               import Player
from Resources.DungeonLoader        import DungeonLoader
from Resources.FunctionMemory       import FunctionMemory
from Resources.EngineOperation      import EngineOperation, _EngineOperation, OpType
from Resources.EngineErrors         import EngineError
from Resources.Util                 import Util

from threading import Thread


from typing import Any, Generator, Callable
import glob, json, re
#import asyncio

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
        self.default_input_handler = self._default_input_handler()
        #self.default_input_handler.send(None)

    def evaluateFunction(self, data:dict):
        return self.loader.evaluateFunction(self, data)

    def loadGame(self):
        self.loader.loadGame(self)
        self.players = Player.loadData(self)
        print(self.players)

    def saveGame(self):
        self.loader.saveGame(self)
        Player.saveData(self)

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
            self.input_queue.update({player_id: [self._default_input_handler, self.default_input_handler, text]})
        else:
            self.input_queue[player_id][2] = text

    def sendOutput(self, target:str|int, text:str):
        self.io_hook.sendOutput(target, text)

    def _default_input_handler(self) -> Generator:
        while self.running:
            player_id, text = yield EngineOperation.Continue()
            
            # TODO: checks for stuff like moving, inventory stuff, etc...

    def getPlayer(self, player_id:int) -> Player:
        if p := Player._loaded.get(player_id, None): return p
        raise EngineError(f"Player does not exist with id: '{player_id}'")

    def evaluateResult(self, handler_getter:Callable, handler:Generator, result:_EngineOperation, player_id:int, text:str):
        
        match result:
            case EngineOperation.GetInput():
                target:int = result.target
                prompt:str = result.prompt
                
            case EngineOperation.Restart():
                gen = self.input_queue[player_id][0]
                self.input_queue[player_id][1] = gen
            case EngineOperation.Cancel():
                ...
            case EngineOperation.Success():
                ...
            case EngineOperation.Failure():
                ...
            case EngineOperation.Error():
                ...
            case EngineOperation.Continue():
                ...
            case _:
                raise EngineError("Unknown Operation")

    def _main_loop_threaded(self):
        
    #    asyncio.run(self._async_main_loop())
    #async def _async_main_loop(self):
        
        self.io_hook.init(self)
        self.io_hook.start()
        while self.thread_running:
            if not self.running:
                # Pause Menu thingy?
                continue
            # Main Loop
            
            # check inputs
            while self.input_queue:
                for key in [k for k in self.input_queue.keys()]:
                    player_id, [handler_getter, response_handler, text] = self.input_queue[key]
                    handler_getter: Callable
                    response_handler: Generator|Callable
                    player_id: int
                    text: str
                    if text:
                        if isinstance(response_handler, Generator):
                            if not Util.generator_started(response_handler):
                                result = response_handler.send(None)
                                if not isinstance(result, _EngineOperation):
                                    raise EngineError("generator did not yield/return an EngineOperation")
                                #print(result)
                                self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                                continue
                            try:
                                result = response_handler.send(player_id, text)
                                if not isinstance(result, _EngineOperation):
                                    raise EngineError("generator did not yield/return an EngineOperation")
                                #print(result)
                                self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                                continue
                                
                            except StopIteration as e:
                                result = e.value
                                if not isinstance(result, _EngineOperation):
                                    raise EngineError("generator did not yield/return an EngineOperation")
                                #print(result)
                                self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                                continue
                                
                        elif isinstance(response_handler, Callable):
                            result = response_handler(player_id, text)
                            if isinstance(result, Generator):
                                self.input_queue[player_id][1] = response_handler = result
                                result = response_handler.send(None)
                            if not isinstance(result, _EngineOperation):
                                raise EngineError("function did not return an EngineOperation")
                            self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                            continue



        self.io_hook.stop()


    



if __name__ == "__main__":
    pass