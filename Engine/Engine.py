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
from Resources.EngineErrors         import EngineError, EngineBreak, UnknownPlayerError
from Resources.Util                 import Util
from Resources.ConsoleCommands      import ConsoleCommand # import the base class through the file that adds sub classes
from Resources.Position             import Position

from threading import Thread


from typing import Any, Generator, Callable
import time
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
        self._loaded = False
        self.io_hook = io_hook
        self.loader: DungeonLoader = DungeonLoader()
        #self.function_memory: FunctionMemory = FunctionMemory()
        self._function_memory = FunctionMemory(self)
        self.default_input_handler = self._default_input_handler
        self.players: dict[str, Player] = {}
        self.combats: list[Combat] = []
        self.tasks: list[Generator] = []
        self._player_input_categories = ["common", "global", "world"]
        self._frame_times = [1 for _ in range(60)]
        self._frame_start = 0
        self._frame_end = 0
        self.tps = []
        
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
            if isinstance(v, _EngineOperation):
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

    def start(self):
        if not self.thread_running:
            t = Thread(target=self._main_loop_threaded)
            self.thread_running = True
            self.running = True
            t.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread_running = False
            self.saveGame()
            self.unloadGame()

    def pause(self):
        self.running = False

    def handleInput(self, player_id:str|int, text:str):
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

    def _default_input_handler(self, _, player_id, text) -> Generator:
        while self.running:
            try:
                Log["debug"]["engine"]["input-handler"](f"handling: '{text}' from {player_id}")

                if player_id == 0: # id 0 means engine basically
                    self._function_memory.clear()
                    ConsoleCommand.handle_input(self._function_memory, text)

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

    def _move_player(self, function_memory:FunctionMemory, player:Player, target_location:Location, handler_getter:Callable, handler:Generator, is_death=False):
        old_room = self.loader.getLocation(self._function_memory, player.location)
        new_room = self.loader.getLocation(self._function_memory, target_location)

        yield

        if is_death:
            ev = old_room.onDeath(function_memory, player)
        else:
            ev = old_room.onExit(function_memory, player)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield (handler_getter, handler, v, player.uuid, "")
                v = ev.send(res)
        except StopIteration as e:
            if isinstance(e.value, _EngineOperation):
                res = yield (handler_getter, handler, e.value, player.uuid, "")

        if old_room.location.dungeon != new_room.location.dungeon:
            old_dungeon = self.loader.getLocation(self._function_memory, f"dungeon:{old_room.location.dungeon}")
            new_dungeon = self.loader.getLocation(self._function_memory, f"dungeon:{new_room.location.dungeon}")

            if is_death:
                ev = old_dungeon.onDeath(function_memory, player)
            else:
                ev = old_dungeon.onExit(function_memory, player)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield (handler_getter, handler, v, player.uuid, "")
                    v = ev.send(res)
            except StopIteration as e:
                if isinstance(e.value, _EngineOperation):
                    res = yield (handler_getter, handler, e.value, player.uuid, "")

            ev = new_dungeon.onEnter(function_memory, player, False)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield (handler_getter, handler, v, player.uuid, "")
                    v = ev.send(res)
            except StopIteration as e:
                if isinstance(e.value, _EngineOperation):
                    res = yield (handler_getter, handler, e.value, player.uuid, "")
        
        ev = new_room.onEnter(function_memory, player)
        v = None
        try:
            v = ev.send(None)
            while isinstance(v, _EngineOperation):
                res = yield (handler_getter, handler, v, player.uuid, "")
                v = ev.send(res)
        except StopIteration as e:
            if isinstance(e.value, _EngineOperation):
                res = yield (handler_getter, handler, e.value, player.uuid, "")

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

            case EngineOperation.StartCombat():
                player: Player = result.player
                combat: Combat = result.combat
                combat.addPlayer(player)
                combat.start(FunctionMemory(self))
                
            case EngineOperation.MovePlayer():
                player = result.player
                target_location = result.target_location

                mover = self._move_player(self._function_memory, player, target_location, handler_getter, handler)
                mover.send(None)
                self.tasks.append(mover)

            # case EngineOperation.KillPlayer():
            #     player = result.player

            #     self.players.pop(player.uuid)

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
                if player_id in self.input_queue:
                    self.input_queue[player_id][2] = ""
            # case Combat.Operation._Operation():
            #     print(f"\u001b[38;2;255;0;0mEngine got Combat Operation: {result}\0")

            case _:
                raise EngineError("Unknown Operation")

    def _handler_getter_wrapper(self, handler):
        yield handler

    def _main_loop_threaded(self):
        
    #    asyncio.run(self._async_main_loop())
    #async def _async_main_loop(self):
        
        self.io_hook.init(self)
        self.io_hook.start()
        self.loadGame()

        for player in self.players.values():
            self.evaluateResult(self._default_input_handler, self.default_input_handler, EngineOperation.MovePlayer(player, player.location), player.uuid, "")

        while self.thread_running:

            self._frame_end = time.time()
            self._frame_times = self._frame_times[1:] + [self._frame_end - self._frame_start]
            if sum(self._frame_times) != 0:
                self.tps = len(self._frame_times)/sum(self._frame_times)
            self._frame_start = time.time()

            #print(f"\u001b[0F\u001b[30G{self.tps}\r")

            if not self.running:
                # Pause Menu thingy?
                continue
            # Main Loop

            # run scheduled tasks
            while self.tasks:
                task = self.tasks.pop(0)
                v = None
                try:
                    while True:
                        v = task.send(None)
                        try:
                            self.evaluateResult(*v)
                        except EngineError as e:
                            print(e)
                except StopIteration as e:
                    Log["debug"]["engine"](f"Task completed: {task}  {v=}  {e.value=}")

            for combat in self.combats.copy():
                try:
                    ops: dict = combat.tick.send(None)

                    for player_id, op in ops.items():
                        if isinstance(op, _EngineOperation):
                            try:
                                self.evaluateResult(
                                    self._handler_getter_wrapper(combat.onInput),
                                    combat.onInput,
                                    op, player_id, ""
                                )
                            except EngineError as e:
                                Log["ERROR"]["engine"](e)
                        else:
                            Log["WARNING"]["engine"](f"\combat returned non-engine operation??")
                except StopIteration:
                    self.combats.remove(combat)

            # check inputs
            for player_id in [k for k in self.input_queue.copy().keys()]:
                handler_getter, response_handler, text = self.input_queue[player_id]
                handler_getter: Callable
                response_handler: Generator|Callable
                player_id: int
                text: str

                if player_id == 0:
                    if text:
                        self.input_queue.update({0: [self._default_input_handler, self.default_input_handler, ""]})
                        ConsoleCommand.handle_input(self._function_memory, text)
                    continue
                try:
                    player: Player = Player.getPlayer(player_id)
                except Exception as e:
                    self.sendOutput(0, "\n".join(e.args))
                    self.input_queue.pop(player_id)
                    continue

                if text:

                    if player.in_combat:
                        player._combat.onInput(player, text)
                        self.input_queue[player.uuid][2] = ""
                        continue

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
                            self.evaluateResult(self._default_input_handler, self.default_input_handler, e.value, player_id, text)

                    if isinstance(response_handler, Generator):
                        if not Util.generator_started(response_handler):
                            result = response_handler.send(None)
                            if not isinstance(result, _EngineOperation):
                                raise EngineError(f"generator did not yield/return an EngineOperation! ({result})")
                            #print(result)
                            try:
                                self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                            except EngineError as e:
                                Log["ERROR"]["engine"](e)
                            continue
                        try:
                            result = response_handler.send((self, player_id, text))
                            if not isinstance(result, _EngineOperation):
                                raise EngineError(f"generator did not yield/return an EngineOperation! ({result})")
                            #print(result)
                            try:
                                self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                            except EngineError as e:
                                Log["ERROR"]["engine"](e)
                            continue
                            
                        except StopIteration as e:
                            result = e.value
                            if not isinstance(result, _EngineOperation):
                                raise EngineError(f"generator did not yield/return an EngineOperation! ({result})")
                            #print(result)
                            try:
                                self.evaluateResult(handler_getter, response_handler, result, player_id, text)
                            except EngineError as e:
                                Log["ERROR"]["engine"](e)
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
                            Log["ERROR"]["engine"](e)
                        continue

            # do other engine stuff

        # self.saveGame()
        self.io_hook.stop()


if __name__ == "__main__":
    ...