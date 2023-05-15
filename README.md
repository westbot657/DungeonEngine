
# Dungeon Building

Note: This is going to be a VERY long, detailed, guide to creating a dungeon and all it's components.  
[File Structure](#file-structure)
[Dungeons](#dungeons) | [Rooms](#rooms) | [Interactions](#interactions)    
[Weapons](#weapons) | [Ammo](#ammo) | [Armor](#armor)  
[Items](#items) | [Tools](#tools)  
[StatusEffects](#status-effects)  
[Enemies](#enemies) | [Attacks](#attacks) | [Entities](#entities) | [Combats](#combats)  
[Interactable Types](#interactable-types)  
[Functions](#functions)  

## File Structure
```
Dungeons/
|- resources/
|  |- ammo/
|  |- armor/
|  |- combats/
|  |- enemies/
|  |- items/
|  |- tools/
|  |- weapons/

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
  "parent": "<item identifier>",
  "name": "...",
  "max_count": "<int>",
  "count": "<int>",
  "data": {...},
  "events": {
    "on_use": {...},
    "on_expended": {...}
  }
}
```


## Tools
```json
{
  "parent": "<tool identifier>",
  "name": "...",
  "max_durability": "<int>",
  "durability": "<int>",
  "data": {...},
  "events": {
    "on_use": {...},
    "on_equip": {...},
    "on_unequip": {...},
    "on_damaged": {...},
    "on_break": {...}
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

## Functions

Function and Parameter List:  
- player:
  - engine:player/message
    * message
  - engine:player/get_input
  - engine:player/give_item
    * item
  - engine:player/heal
    * amount
  - engine:player/damage
    * amount

the following functions have more complex parameters.  
more in-depth explanation can be found [here](#complex-parameters)
- math:
  - engine:math/solve

- random:
  - engine:random/weighted
  - engine:random/uniform

- logic:
  - engine:logic/compare

- text:
  - engine:text/builder

Usage:
```json
...
  {
    "function": "<function-id>",
    "<parameter>": "<value>",
    ...
  }
...
```


### Function Examples
WIP




#### complex parameters
WIP





