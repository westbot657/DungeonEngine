# pylint: disable=[W,R,C,import-error]

try:
    from .Combat import Combat
    from .Identifier import Identifier
    from .FunctionMemory import FunctionMemory
    from .EngineErrors import CombatError
    from .Util import Util
    from .AbstractEnemy import AbstractEnemy, Enemy
except ImportError:
    from Combat import Combat
    from Identifier import Identifier
    from FunctionMemory import FunctionMemory
    from EngineErrors import CombatError
    from Util import Util
    from AbstractEnemy import AbstractEnemy, Enemy

import glob, json, re


class AbstractCombat:
    _loaded: dict = {}

    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data

        self.enemies: list = data.get("enemies", [])
        self.sequence: dict = data.get("sequence", {})
        self.data: dict = data.get("data", {})

    def getEnemies(self, function_memory:FunctionMemory) -> list:
        _unknown = []
        abstracts = {}
        for enemy in self.enemies:
            if isinstance(enemy, str):
                abstract:AbstractEnemy = AbstractEnemy.getFromIdentifier(enemy)
                _unknown.append(abstract)
            elif isinstance(enemy, dict):
                if any(k in enemy for k in ["function", "functions", "@check", "#ref", "#call"]):
                    res = function_memory.evaluateFunction(enemy)
                    if isinstance(res, Enemy):
                        pass

    def createInstance(self, function_memory:FunctionMemory, **override_values):
        return Combat(self,
            self.getEnemies(function_memory),
            Util.deepCopy(self.sequence),
            Util.deepCopy(self.data)
        )

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


