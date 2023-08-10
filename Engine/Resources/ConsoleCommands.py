# pylint: disable=[W,R,C,import-error]

try:
    from .ConsoleCommand import ConsoleCommand
    from .Identifier import Identifier
    from .Player import Player
    from .Inventory import Inventory
    from .FunctionMemory import FunctionMemory
except ImportError:
    from ConsoleCommand import ConsoleCommand
    from Identifier import Identifier
    from Player import Player
    from Inventory import Inventory
    from FunctionMemory import FunctionMemory

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
                "name: enigne:str": None
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




