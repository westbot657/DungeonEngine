
# json based dungeons!



you can ignore this file, I'm juts using it to list possible values of stuff


## stuff with all (most) possible values

### dungeon1/dungeon.json
```json
{
    "name": "dungeon1",
    "version": 0.1,
    "enter_message": "",
    "exit_message": "",
    "data": {
        "boss_defeated": true|false
    },
    "entry_point": "dungeon1:room1"
}
```


### dungeon1/rooms/room1.json
```json
{
    "name": "Room 1",
    "interactions": [
        {
            "type": "door",
            "target": "dungeon1:room2",
            "locked": true|false,
            "travel_message": "..."
        }
    ]
}
```

### dungeon1/rooms/room2.json
```json

```

### dungeon1/rooms/room3.json
```json

```

### dungeon1/resources/weapons/excaliber.json
```json

```

### dungeon1/resources/ammo/acid_arrow.json
```json

```

### dungeon1/resources/armor/chainmail.json
```json

```

### 





