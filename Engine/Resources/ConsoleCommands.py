# pylint: disable=[W,R,C,import-error]

from ConsoleCommand import ConsoleCommand
from Identifier import Identifier
from Player import Player
from Inventory import Inventory
from FunctionMemory import FunctionMemory
from Logger import Log
from EngineErrors import EngineError

@ConsoleCommand(
    Identifier("engine", "", "save-game"),
    {}
)
def engine_saveGame(function_memory:FunctionMemory):
    function_memory.saveGame()

@ConsoleCommand(
    Identifier("engine", "", "new-player"),
    {
        "player_id: engine:int": {
            "name: engine:str": None
        }
    }
)
def engine_newPlayer(function_memory:FunctionMemory, player_id, name):
    Player.newPlayer(function_memory, player_id, name, 20)


@ConsoleCommand(
    Identifier("engine", "", "run-function"),
    {
        "function: engine:dict": None
    }
)
def engine_runFunction(function_memory:FunctionMemory, function):
    function_memory.evaluateFunction(function)


@ConsoleCommand(
    Identifier("engine", "", "give"),
    {
        "target: engine:Player": {
            "objectType: engine:GameObjectType": {
                "gameObject: engine:str": None
            }
        }
    }
)
def engine_giveGameObject(function_memory:FunctionMemory, target, objectType, gameObject):
    ...


@ConsoleCommand(
    Identifier("engine", "", "toggle-log"),
    {}
)
def engine_toggle_log(function_memory:FunctionMemory):
    Log.toggle()


@ConsoleCommand(
    Identifier("engine", "", "stop"),
    {}
)
def engine_stop(function_memory:FunctionMemory):
    function_memory.saveGame()
    function_memory.unloadGame()

@ConsoleCommand(
    Identifier("engine", "ui/", "get_inventory"),
    {
        "player: engine:int": None
    }
)
def engine_ui_get_inventory(function_memory:FunctionMemory, player):
    try:
        player = function_memory.engine.getPlayer(player)
        function_memory.engine.sendOutput(2, player.inventory)
    except EngineError as e:
        Log["ERROR"]("\n".join(e.args))

@ConsoleCommand(
    Identifier("engine", "ui/", "get_combat"),
    {
        "player: engine:int": None
    }
)
def engine_ui_get_combat(function_memory:FunctionMemory, player):
    try:
        player = function_memory.engine.getPlayer(player)
        function_memory.engine.sendOutput(3, player._combat)
    except EngineError as e:
        Log["ERROR"]("\n".join(e.args))

@ConsoleCommand(
    Identifier("engine", "", "get-combat"),
    {
        "player: engine:int": None
    }
)
def engine_get_combat(function_memory:FunctionMemory, player):
    try:
        player = function_memory.engine.getPlayer(player)
        if player._combat:
            function_memory.engine.sendOutput(player, player._combat.fullStats(function_memory))
    except EngineError as e:
        Log["ERROR"]("\n".join(e.args))

@ConsoleCommand(
    Identifier("engine", "ui/", "get_player"),
    {
        "player: engine:int": None
    }
)
def engine_ui_get_player(function_memory:FunctionMemory, player:int):
    try:
        player = function_memory.engine.getPlayer(player)
        function_memory.engine.sendOutput(4, player)
    except EngineError as e:
        Log["ERROR"]("\n".join(e.args))
        function_memory.engine.sendOutput(4, None)

        

