# pylint: disable=[W,R,C,import-error]


from .AbstractAmmo import AbstractAmmo, Ammo
from .AbstractArmor import AbstractArmor, Armor
from .AbstractAttack import AbstractAttack, Attack
from .AbstractEnemy import AbstractEnemy, Enemy
from .AbstractCombat import AbstractCombat, Combat
from .AbstractDungeon import AbstractDungeon, Dungeon
from .AbstractItem import AbstractItem, Item
from .AbstractRoom import AbstractRoom, Room
from .AbstractStatusEffect import AbstractStatusEffect, StatusEffect, StatusEffectCause
from .StatusEffectManager import StatusEffectManager
from .AbstractTool import AbstractTool, Tool
from .AbstractWeapon import AbstractWeapon, Weapon
from .Identifier import Identifier
from .EngineDummy import Engine
from .EngineErrors import InvalidObjectError, FunctionLoadError, LocationError
from .LootTable import LootTable
from .Player import Player
from .AbstractGameObject import AbstractGameObject, GameObject
from .Util import Util
from .Currency import Currency
from .Logger import Log
from .Location import Location
from .Position import Position
from .Environment import Environment
from .AbstractInteractable import AbstractInteractable, Interactable
from .Entity import Entity
from .DynamicValue import DynamicValue
from .ES3 import EngineScript
from .Serializer import Serializer, Serializable

import time

class EngineLoader:
    _loader = None
    
    def __new__(cls):
        if not cls._loader:
            cls._loader = self = super().__new__(cls)
            self.init()
        return cls._loader
    
    def init(self):
        self.abstract_ammo: dict[str, AbstractAmmo] = {}
        self.abstract_armor: dict[str, AbstractArmor] = {}
        self.abstract_attacks: dict[str, AbstractAttack] = {}
        self.abstract_combats: dict[str, AbstractCombat] = {}
        self.abstract_dungeons: dict[str, AbstractDungeon] = {}
        self.dungeons: dict[str, Dungeon] = {}
        self.abstract_enemies: dict[str, AbstractEnemy] = {}
        self.abstract_items: dict[str, AbstractItem] = {}
        self.abstract_interactables: dict[str, AbstractInteractable] = {}
        #self.abstract_loot_tables: dict[str, AbstractLootTable] = {}
        self.abstract_rooms: dict[str, AbstractRoom] = {}
        self.abstract_status_effects: dict[str, AbstractStatusEffect] = {}
        self.abstract_tools: dict[str, AbstractTool] = {}
        self.abstract_weapons: dict[str, AbstractWeapon] = {}
    
    def loadGame(self, engine:Engine):
        start_time = time.time()
    
        EngineScript.engine = engine
    
        if engine.is_console:
            Log.silent = True
        
        EngineScript.load()
        EngineScript.preCompileAll()

        
        Log["loadup"]["loader"]("Loading Abstract Status Effects...")
        self.abstract_status_effects = AbstractStatusEffect.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Ammo...")
        self.abstract_ammo = AbstractAmmo.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Armor...")
        self.abstract_armor = AbstractArmor.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Tools...")
        self.abstract_tools = AbstractTool.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Weapons...")
        self.abstract_weapons = AbstractWeapon.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Items...")
        self.abstract_items = AbstractItem.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Attacks...")
        self.abstract_attacks = AbstractAttack.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Enemies...")
        self.abstract_enemies = AbstractEnemy.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Combats...")
        self.abstract_combats = AbstractCombat.loadData(engine)
        
        Log["loadup"]["loader"]("Loading Abstract Interactables...")
        self.abstract_interactables = AbstractInteractable.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Rooms...")
        self.abstract_rooms = AbstractRoom.loadData(engine)

        Log["loadup"]["loader"]("Loading Abstract Dungeons...")
        self.abstract_dungeons: list[AbstractDungeon] = AbstractDungeon.loadData(engine)

        Log["loadup"]["loader"]("Loading Dungeons...")
        self.dungeons = {}
        for k, v in self.abstract_dungeons.items():
            self.dungeons.update({k: v.createInstance(engine)})

        for dungeon in self.dungeons.values():
            for room in dungeon.rooms.values():
                room: Room
                room.onLoad(engine)

        Log["loadup"]["loader"]("Loading Players...")
        self.players = Player.loadData(engine)

        Log.silent = False

        Log["loadup"]["loader"]("Engine resource loading completed")

        Log["loadup"]["loader"](f"Loading finished in {time.time()-start_time} seconds")


    def saveGame(self, engine:Engine):
        # TODO: implement saving

        Log["loadup"]["loader"]("Saving Dungeons...")
        AbstractDungeon.saveData(engine)

        Log["loadup"]["loader"]("Saving Players...")
        Player.saveData(engine)

        Log["loadup"]["loader"]("Finished saving")

    def unloadGame(self):

        Log["loader"]["shutdown"]("Unloading Weapons")
        AbstractWeapon._loaded.clear()
        self.abstract_weapons.clear()

        Log["loader"]["shutdown"]("Unloading Ammo")
        AbstractAmmo._loaded.clear()
        self.abstract_ammo.clear()

        Log["loader"]["shutdown"]("Unloading Armor")
        AbstractArmor._loaded.clear()
        self.abstract_armor.clear()

        Log["loader"]["shutdown"]("Unloading Tools")
        AbstractTool._loaded.clear()
        self.abstract_tools.clear()

        Log["loader"]["shutdown"]("Unloading Items")
        AbstractItem._loaded.clear()
        self.abstract_items.clear()

        Log["loader"]["shutdown"]("Unloading Combats")
        AbstractCombat._loaded.clear()
        self.abstract_combats.clear()

        Log["loader"]["shutdown"]("Unloading Enemies")
        AbstractEnemy._loaded.clear()
        self.abstract_enemies.clear()

        Log["loader"]["shutdown"]("Unloading Attacks")
        AbstractAttack._loaded.clear()
        self.abstract_attacks.clear()

        Log["loader"]["shutdown"]("Unloading Interactables")
        AbstractInteractable._loaded.clear()
        self.abstract_interactables.clear()

        Log["loader"]["shutdown"]("Unloading Dungeons")
        AbstractDungeon._loaded.clear()
        self.abstract_dungeons.clear()
        self.dungeons.clear()

        Log["loader"]["shutdown"]("Unloading Rooms")
        AbstractRoom._loaded.clear()
        self.abstract_rooms.clear()

        Log["loader"]["shutdown"]("Unloading Status Effects")
        AbstractStatusEffect._loaded.clear()
        self.abstract_status_effects.clear()

        Log["loader"]["shutdown"]("Unloading Scripts")
        EngineScript.unload()



