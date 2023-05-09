# pylint: disable=[W,R,C,import-error]

from typing import Any, Generator

class Engine:
    #def evaluateFunction(self, data:dict, function_memory=None, context_data=None, local_variables=None) -> Any: ...
    def generatorEvaluateFunction(self, data:dict, function_memory=None, context_data=None, local_variables=None) -> Generator: ...
    def saveGame(self) -> None: ...
    def loadGame(self) -> None: ...
    def getPlayer(self) -> None: ...
    def sendOutput(self) -> None: ...
    class _loader_dummy:
        #def evaluateFunction(self, function_memory, data:dict, expected_key:str|None=None) -> Any: ...
        def generatorEvaluateFunction(self, function_memory, data:dict, expected_key:str|None=None) -> Generator: ...
        def loadGame(self, engine): ...
        def saveGame(self, engine): ...
        def getDynamicValue(self, expected_value_types:list[type], data): ...
        def constructAmmo(self, data:dict): ...
        def constructArmor(self, data:dict): ...
        def constructCombat(self, data:dict): ...
        def constructItem(self, data:dict): ...
        def constructLootTable(self, data:dict): ...
        def constructStatusEffect(self, data:dict): ...
        def constructTool(self, data:dict): ...
        def constructWeapon(self, data:dict): ...
        def constructGameObject(self, data:dict): ...
        def getAmmo(self, identifier): ...
        def getArmor(self, identifier): ...
        def getItem(self, identifier): ...
        def getStatusEffect(self, identifier): ...
        def getTool(self, identifier): ...
        def getWeapon(self, identifier): ...
        def getGameObject(self, identifier): ...
    loader = _loader_dummy()
    
    