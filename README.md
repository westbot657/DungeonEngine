
# How to Run the game
1. make sure you have all the files on your computer with the same file structure as in this repo
2. remove all files within [DungeonEngine/Engine/save_data/](./Engine/save_data/)
3. remove/modify any file contents under the [DungeonEngine/Dungeons/](./Dungeons/) folder (do not change anything in [DungeonEngine/Dungeons/world/](./Dungeons/world/) though, that stuff is important for the Engine to run (see [dungeon building](#dungeon-building) for help on safely modifying the game)
4. run [DungeonEngine/Engine/ConsoleRunner.py](./Engine/ConsoleRunner.py) from the `DungeonEngine/` parent directory
5. I've had it take between 5 seconds and 3 minutes to load all resources, based on what computer I'm using, what apps are open in the background, etc...
6. If you have issues, there's an issues feature here on github, but to be fair, idk how it works, so yeah.
7. This Engine is still under development, don't expect much to work




# Dungeon Building  

Note: This is going to be a VERY long, detailed, guide to creating a dungeon and all it's components  
---
[File Structure](#file-structure)  
[Dungeons](#dungeons) | [Rooms](#rooms) | [Interactions](#interactions)    
[Weapons](#weapons) | [Ammo](#ammo) | [Armor](#armor)  
[Items](#items) | [Tools](#tools)  
[StatusEffects](#status-effects)  
[Enemies](#enemies) | [Attacks](#attacks) | [Entities](#entities) | [Combats](#combats)  
[Interactable Types](#interactable-types)  

[Engine Code](#engine-code)  

## File Structure
```file_tree
Dungeons/
|- <dungeon_id>
|  |- resources/
|  |  |- ammo/
|  |  |- armor/
|  |  |- enemies/
|  |  |- items/
|  |  |- tools/
|  |  \- weapons/
|  |- combats/
|  |- rooms/
|  |- <dungeon_id>.json
|  \- ec_functions.json
:
```

## Dungeons

Base JSON values:
```json
{
  "name": <text>,
  "version": <number>,
  "entry_point": <room identifier>,
  "events": {
    "on_enter": {engine code},
    "on_exit": {engine code}
  }
  "data": {
    "<name>": <value>|{boot engine code}
  }
}
```

More comming soon!  


## Rooms

```json
{
  "name": <text>,
  "interactions": [
    // interactions will be explained below
  ],
  "events": {
    "on_enter": {engine code},
    "on_exit": {engine code},
    "on_input": {engine code}
  }
}
```

## Interactions
for interactable types, go [here](#interactable-types).  


Door Interaction JSON:  
```json
{
  "type": "engine:door",
  "id": <text>,
  "target": <room identifier>,
  "travel_message": <text>|{engine code},
  "lock_message": <text>|{engine code},
  "locked": <boolean>,
  "open_message": <text>|{engine code},
  "disengage_message": <text>|{engine code}
}
```

## Weapons
WIP  

## Ammo
WIP  

## Armor
WIP  

## Items
```json
{
  "parent": <item identifier>,
  "name": <text>|{boot engine code},
  "max_count": <int>,
  "count": <int>|{boot engine code},
  "data": {
    "<name>": {boot engine code}
  },
  "events": {
    "on_use": {engine code},
    "on_expended": {engine code}
  }
}
```


## Tools
```json
{
  "parent": <tool identifier>,
  "name": <text>|{boot engine code},
  "max_durability": <int>,
  "durability": <int>|{boot engine code},
  "data": {
    "<name>": {boot engine code}
  },
  "events": {
    "on_use": {engine code},
    "on_equip": {engine code},
    "on_unequip": {engine code},
    "on_damaged": {engine code},
    "on_break": {engine code}
  }
}
```


## Status Effects
WIP  

## Enemies
WIP  

## Attacks
WIP  

## Entities
WIP  

## Interactable Types
WIP  
see the [door](./resources/interactable_types/door.json) interactable type as an example  

## Combats
WIP  


## Engine Code
WIP  

Engine Code is the scripting language used for events and operations within user-made dungeons.  

note:  
`boot engine code` is evaluated on dungeon load up. This means the functions you can use in it are limited  
`engine code` is evaluated as needed during runtime, it is not evaluated on load up.  







