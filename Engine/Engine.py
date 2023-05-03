# pylint: disable=[W,R,C,import-error]
from Resources.Logger import Log

Log._tag_colors = {
    "loadup": "\033[38;2;10;200;80m",
    "player": "\033[38;2;10;40;180m",
    "loader": "\033[38;2;200;200;10m",
    "ERROR": "\033[38;2;255;0;0m",
    "abstract": "\033[38;2;100;100;100m",
    "object": "\033[38;2;200;200;200m",
    "inventory": "\033[38;2;0;100;100m",
    "dungeon": "\033[38;2;0;180;30m",
    "evaluate-result": "\033[38;2;255;0;0m"
}

from Resources.AbstractAmmo         import AbstractAmmo, Ammo
from Resources.AbstractArmor        import AbstractArmor, Armor
from Resources.AbstractCombat       import AbstractCombat, Combat
from Resources.AbstractItem         import AbstractItem, Item
from Resources.LootTable            import LootTable, LootPool, LootEntry
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
from Resources.EngineErrors         import EngineError, EngineBreak
from Resources.Util                 import Util
from Resources.ConsoleCommands      import ConsoleCommand # import the base class through the file that adds sub classes

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
        #self.function_memory: FunctionMemory = FunctionMemory()
        self._function_memory = FunctionMemory(self)
        self.default_input_handler = self._default_input_handler
        self.players = {}
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
            if isinstance(v, _EngineOperation):
                res = yield v
                v = ev.send(res)
        except StopIteration as e:
            v = e.value or (v if not isinstance(v, _EngineOperation) else None)
        return v

    def loadGame(self):
        self.loader.loadGame(self)
        self.players = Player.loadData(self)

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

    def setInputHandler(self, player_id, handler, handler_getter):
        self.input_queue.update({player_id: [handler_getter, handler, ""]})

    def sendOutput(self, target:str|int, text:str):
        self.io_hook.sendOutput(target, text)

    def _default_input_handler(self, _, player_id, text) -> Generator:
        while self.running:
            try:
                Log["debug"]["engine"]["input-handler"](f"handling: '{text}' from {player_id}")

                if player_id == 0: # id 0 means engine basically
                    self._function_memory.clear()
                    ConsoleCommand.handle_input(self._function_memory, text)

                elif player := self.getPlayer(player_id, None):
                    player: Player
                    
                    self._function_memory.clear()
                    
                    res = TextPattern.handleInput(self._function_memory, player, text, player._text_pattern_categories)
                    #if isinstance(res, Generator):
                    v = None
                    try:
                        v = res.send(None)
                        if isinstance(v, _EngineOperation):
                            #ret = yield v
                            self.evaluateResult(self._default_input_handler, res, v, player_id, text)
                            #v = res.send(ret)
                    except StopIteration as e:
                        
                        if isinstance(e.value, _EngineOperation):
                            _, player_id, text = yield e.value
                            continue
                    _, player_id, text = yield EngineOperation.Continue()
                    #else:
                    #    _, player_id, text = yield res

                    continue

            except EngineBreak: pass
            _, player_id, text = yield EngineOperation.Continue()

    def getPlayer(self, player_id:int, default=...) -> Player:
        if p := Player._loaded.get(player_id, None): return p
        if default is ...: raise EngineError(f"Player does not exist with id: '{player_id}'")
        return default


    def inputGetterWrapper(self, handler:Generator):
        _, player_id, text = yield

        v = None
        try:
            v = handler.send(text)
        except StopIteration as e:
            v = e.value or (v if not isinstance(v, _EngineOperation) else None)

        if isinstance(v, (_EngineOperation)):
            return v
        else:
            return EngineOperation.Success(v)

    def evaluateResult(self, handler_getter:Callable, handler:Generator, result:_EngineOperation, player_id:int, text:str):
        Log["debug"]["engine"]["evaluate-result"](f"result:{result}  id:{player_id} text:'{text}'")
        match result:
            case EngineOperation.GetInput():
                target:int = result.target
                prompt:str = result.prompt
                if prompt:
                    self.io_hook.sendOutput(target, prompt)
                #self.input_queue.pop(player_id)

                wrapper = self.inputGetterWrapper(handler)
                wrapper.send(None)
                self.input_queue.update({player_id: [handler_getter, wrapper, ""]})

            case EngineOperation.Restart():
                gen = self.input_queue[player_id][0]
                self.input_queue[player_id][1] = gen
            case EngineOperation.Cancel():
                ...
            case EngineOperation.Success():
                #if result.value:
                #self.io_hook.sendOutput(player_id, result.value)
                if result.value: Log["debug"]["engine"]["evaluate-result"](f"EngineOperation.Success ({result.value})")
                self.input_queue.pop(player_id)
            case EngineOperation.Failure():
                ...
            case EngineOperation.Error():
                ...
            case EngineOperation.Continue():
                #self.io_hook.sendOutput(player_id, result.value)
                if result.value: Log["debug"]["engine"]["evaluate-result"](f"EngineOperation.Continue ({result.value})")
                #if self.input_queue[player_id][1] == self._default_input_handler:
                self.input_queue[player_id][2] = ""
            case _:
                raise EngineError("Unknown Operation")

    def _main_loop_threaded(self):
        
    #    asyncio.run(self._async_main_loop())
    #async def _async_main_loop(self):
        
        self.io_hook.init(self)
        self.io_hook.start()
        self.loadGame()
        while self.thread_running:
            if not self.running:
                # Pause Menu thingy?
                continue
            # Main Loop
            
            # check inputs
            while self.input_queue:
                for player_id in [k for k in self.input_queue.keys()]:
                    handler_getter, response_handler, text = self.input_queue[player_id]
                    handler_getter: Callable
                    response_handler: Generator|Callable
                    player_id: int
                    text: str
                    if text:
                        if isinstance(response_handler, Generator):
                            if not Util.generator_started(response_handler):
                                result = response_handler.send(None)
                                if not isinstance(result, _EngineOperation):
                                    raise EngineError(f"generator did not yield/return an EngineOperation! ({result})")
                                #print(result)
                                try:
                                    self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                                except EngineError as e:
                                    print(e)
                                continue
                            try:
                                result = response_handler.send((self, player_id, text))
                                if not isinstance(result, _EngineOperation):
                                    raise EngineError(f"generator did not yield/return an EngineOperation! ({result})")
                                #print(result)
                                try:
                                    self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                                except EngineError as e:
                                    print(e)
                                continue
                                
                            except StopIteration as e:
                                result = e.value
                                if not isinstance(result, _EngineOperation):
                                    raise EngineError(f"generator did not yield/return an EngineOperation! ({result})")
                                #print(result)
                                try:
                                    self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                                except EngineError as e:
                                    print(e)
                                continue
                                
                        elif isinstance(response_handler, Callable):
                            result = response_handler(self, player_id, text)
                            if isinstance(result, Generator):
                                self.input_queue[player_id][1] = response_handler = result
                                result = response_handler.send(None)
                            if not isinstance(result, _EngineOperation):
                                raise EngineError(f"function did not return an EngineOperation! ({result})")
                            try:
                                self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                            except EngineError as e:
                                print(e)
                            continue

            # do other engine stuff

        self.saveGame()
        self.io_hook.stop()


if __name__ == "__main__":
    ...