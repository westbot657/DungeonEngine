# pylint: disable=[W,R,C,import-error]

try:
    from .ConsoleCommand import ConsoleCommand
    from .Identifier import Identifier
    from .Player import Player
    from .Inventory import Inventory
except ImportError:
    from ConsoleCommand import ConsoleCommand
    from Identifier import Identifier
    from Player import Player
    from Inventory import Inventory

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
def engine_NewPlayer(function_memory, player_id, max_health, name):
    Player.newPlayer(function_memory, player_id, name, max_health)


@ConsoleCommand(
    Identifier("engine", "", "run-function"),
    {
        "function: engine:dict": None
    }
)
def engine_runFunction(function_memory, function):
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
def engine_giveGameObject(function_memory, target, objectType, gameObject):
    ...




