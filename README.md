
# Dungeon Building

Note: This is going to be a VERY long, detailed, guide to creating a dungeon and all it's components.  
[Dungeons](#dungeons) | [Rooms](#rooms)  
[Weapons](#weapons) | [Ammo](#ammo) | [Armor](#armor)  
[Items](#items) | [Tools](#tools)  
[StatusEffects](#status-effects)  
[Enemies](#enemies) | [Attacks](#attacks) | [Entities](#entities) | [Combats](#combats)  
[Interactable Types](#interactable-types)  
[Functions](#functions)  

## Dungeons

### Base JSON values:
```json
{
  "name": "...",
  "version": 1.0,
  "entry_point": "dungeon:rooms/room",
  "enter_message": "...",
  "exit_message": "...",
  "data": {
    "some_variable": "some value"
  }
}
```

More comming soon!  


## Rooms

### Base JSON values:
```json
{
  "name": "<string>",
  "enter_message": "<function|string>",
  "exit_message": "<function|string>",
  "interactions": [
    "// interactions will be explained below"
  ]
}
```

## Interactions
for interactable types, go [here](#interactable-types).  


Door Interactable JSON:  
```json
{
  "type": "engine:door",
  "id": "<string>",
  "target": "<room_identifier>",
  "travel_message": "<function|string>",
  "lock_message": "<function|string>",
  "locked": "<bool>",
  "open_message": "<function|string>",
  "disengeage_message": "<function|string>"
}
```

## Weapons

## Ammo

## Armor

## Items

## Tools

## Status Effects

## Enemies

## Attacks

## Entities

## Interactable Types
see the [door](./resources/interactable_types/door.json) interactable type as an example  

## Combats

## Functions

Function List:  
- player:
  - engine:player/message
  - engine:player/get_input
  - engine:player/give_item
  - engine:player/heal
  - engine:player/damage

- math:
  - engine:math/solve

- random:
  - engine:random/weighted
  - engine:random/uniform

- logic:
  - engine:logic/compare

- text:
  - engine:text/builder

### Function Examples
WIP






