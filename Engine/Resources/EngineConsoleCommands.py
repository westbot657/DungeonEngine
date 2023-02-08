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
def engine_NewPlayer(engine, player_id, max_health, name):
    ...


@ConsoleCommand(
    Identifier("engine", "", "run-function"),
    {
        "function": None
    }
)
def engine_runFunction(engine, function):
    engine.loader.evaluateFunction()







