# pylint: disable=[W,R,C,import-error]

try:
    from .ConsoleCommand import ConsoleCommand
    from .Identifier import Identifier
    from .Player import Player
    from .Inventory import Inventory
    from .FunctionMemory import FunctionMemory
    from .Logger import Log
    from .EngineErrors import EngineError
except ImportError:
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
            "max_health: engine:int": {
                "name: engine:str": None
            }
        }
    }
)
def engine_newPlayer(function_memory:FunctionMemory, player_id, max_health, name):
    Player.newPlayer(function_memory, player_id, name, max_health)


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
    function_memory.unloadGame()

@ConsoleCommand(
    Identifier("engine", "ui/", "get_inventory"),
    {
        "player: engine:Player": None
    }
)
def engine_ui_get_inventory(function_memory:FunctionMemory, player):
    function_memory.engine.sendOutput(2, player.inventory)

@ConsoleCommand(
    Identifier("engine", "ui/", "get_combat"),
    {
        "player: engine:Player": None
    }
)
def engine_ui_get_combat(function_memory:FunctionMemory, player):
    function_memory.engine.sendOutput(3, player.combat)

@ConsoleCommand(
    Identifier("engine", "ui/", "get_player"),
    {
        "player_id: engine:int": None
    }
)
def engine_ui_get_player(function_memory:FunctionMemory, player_id:int):
    try:
        player = function_memory.engine.getPlayer(player_id)
        function_memory.engine.sendOutput(4, player)
    except EngineError as e:
        Log["ERROR"]("\n".join(e.args))
        

