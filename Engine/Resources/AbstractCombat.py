# pylint: disable=[W,R,C,import-error]

try:
    from .Combat import Combat
    from .Identifier import Identifier
    from .FunctionMemory import FunctionMemory
    from .EngineErrors import CombatError
    from .Util import Util
    from .AbstractEnemy import AbstractEnemy, Enemy
    from .Location import Location
    from .Position import Position
    from .Logger import Log
except ImportError:
    from Combat import Combat
    from Identifier import Identifier
    from FunctionMemory import FunctionMemory
    from EngineErrors import CombatError
    from Util import Util
    from AbstractEnemy import AbstractEnemy, Enemy
    from Location import Location
    from Position import Position
    from Logger import Log

import glob, json, re


class AbstractCombat:
    _loaded: dict = {}

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data

        self.enemies: list = data.get("enemies", [])
        self.sequence: dict = data.get("sequence", {})
        self.data: dict = data.get("data", {})

    def getEnemies(self, function_memory:FunctionMemory) -> list[AbstractEnemy]:
        
        enemies = []
        for enemy in self.enemies:
            if isinstance(enemy, str):
                abstract:AbstractEnemy = AbstractEnemy.getFromIdentifier(enemy)
                enemies.append(abstract)

            elif isinstance(enemy, dict):

                if any(k in enemy for k in ["function", "functions", "@check", "#ref", "#call"]):
                    Log["warning"]["abstract combat"][f"cannot load abstract enemy from data: '{enemy}'"]
                    res = function_memory.evaluateFunction(enemy)
                    if isinstance(res, Enemy):
                        pass
                    elif isinstance(res, list):
                        for r in res:
                            pass
                
                else:
                    identifier = Identifier("<combat>", "", "")
                    e = AbstractEnemy(identifier, enemy)
                    e.linkParent()
                    identifier.path = id(self)
                    identifier.name = e.name

                    enemies.append(e)
        
        return enemies
        

    def createInstance(self, function_memory:FunctionMemory, **override_values):
        combat = Combat(self,
            self.getEnemies(function_memory),
            Util.deepCopy(self.sequence),
            Util.deepCopy(self.data)
        )

        combat.location = function_memory.ref("#room").location.copy()

        return combat

    @classmethod
    def getCombat(cls, function_memory:FunctionMemory, combat_id:str|Identifier):
        combat_id = Identifier.fromString(combat_id).full()
        
        if (combat := cls._loaded.get(combat_id, None)) is not None:
            combat: AbstractCombat
            return combat.createInstance(function_memory)
        raise CombatError(f"No combat with id: '{combat_id}'")


    @classmethod
    def loadData(cls, engine) -> list:
        files: list[str] = glob.glob("**/combats/*.json", recursive=True)

        for file in files:
            file: str
            with open(file, "r+", encoding="utf-8") as f:
                data = json.load(f)
            
            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        return cls._loaded


