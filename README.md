
# Dungeon Building  

Note: This is going to be a VERY long, detailed, guide to creating a dungeon and all it's components.  
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
```
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
  "name": "...",
  "version": 1.0,
  "entry_point": "dungeon:rooms/room",
  "events": {
    "on_enter": {...},
    "on_exit": {...}
  }
  "data": {
    "some_variable": "some value"
  }
}
```

More comming soon!  


## Rooms

Base JSON values:
```json
{
  "name": "<string>",
  "interactions": [
    // interactions will be explained below
  ],
  "events": {
    "on_enter": {...},
    "on_exit": {...},
    "on_input": {...}
  }
}
```

## Interactions
for interactable types, go [here](#interactable-types).  


Door Interaction JSON:  
```json
{
  "type": "engine:door",
  "id": "<string>",
  "target": "<room identifier>",
  "travel_message": "<function|string>",
  "lock_message": "<function|string>",
  "locked": "<bool>",
  "open_message": "<function|string>",
  "disengeage_message": "<function|string>"
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
    "<name>: {boot engine code}
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







