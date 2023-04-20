# pylint: disable=[W,R,C,import-error]

try:
    from .ConsoleCommand import ConsoleCommand
    from .Identifier import Identifier
except ImportError:
    from ConsoleCommand import ConsoleCommand
    from Identifier import Identifier


@ConsoleCommand(
    Identifier("engine", "", "new-player"),
    {
        "player_id:int": {
            "max_health:int": {
                "name:str": None
            }
        }
    }
)
def engine_NewPlayer(function_memory, player_id, max_health, name):
    ...


@ConsoleCommand(
    Identifier("engine", "", "run-function"),
    {
        "function:dict": None
    }
)
def engine_runFunction(function_memory, function):
    function_memory.evaluateFunction(function)


@ConsoleCommand(
    Identifier("engine", "", "give"),
    {
        "target:Player": {
            "objectType:GameObjectType": {
                "gameObject:str": None
            }
        }
    }
)
def engine_giveGameObject(function_memory, target, objectType, gameObject):
    ...




