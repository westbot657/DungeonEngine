
# Insert Dungeon Name Here

### A text-adventure style multiplayer game engine

**CURRENTLY IN BETA**  

Join [the discord](https://discord.gg/cj77mFZ8eh) for development updates, to give feedback, report bugs and issues, and share your custom dungeons with others!
The discord is also where you can find help on anything related to IDNH.  

## Installing and running

1. Download the latest zip file release
2. unzip into whatever directory you see fit.
3. run `Insert Dungeon Name Here.exe`

The game can also be run in the command line by running
`Insert Dungeon Name Here cmd.exe`

**For linux/mac:**

1. (linux) things do exist that let you run windows executables
2. download/clone the repo, and run in python (version 3.12+)
    - run the file `GraphicsEngine/ui_library.py`
3. download and build (via [pyinstaller](https://pypi.org/project/pyinstaller/)) for your platform
4. official builds may be downloadable at some point in the future, once I figure out a reliable way to build for other platforms

## Playing the game

**THE GAME IS NOT CURRENTLY IN A PLAYABLE STATE**  
(building dungeons works fine)

### Playing via the app

1. Click on the game tab on the left (top icon)
2. Click either the multiplayer or singleplayer play button (Multiplayer button is currently broken)
3. Make a new player with the `+ New Player` button (bottom left of the screen)
4. Note that nearly all buttons will display a quick description if hovered for a second or so.

### Playing via the console

1. type `[0]: engine:new-player <id> <max_health> <name>`
    - `id` must be a number larger than 9
    - `max_health` will be removed when I find a good default, (around 20 is ideal for the main story dungeon that is currently in development)
2. pre-fix any messages as your new player with the id you used for creation (`[<id>]: whatever you want to say`)
3. Note that ids 0-9 are reservered for the game system

## Dungeon Building

See the [wiki](https://github.com/westbot657/DungeonEngine/wiki) for the (eventually) in-depth guide to building a dungeon.

## Versioning system

```ascii
0.0.0.0
^ ^ ^ ^
│ │ │ └───────────────────────────────────────────────────┐
│ │ └────────────────────────────────┐                    │
│ └─────────────┐                    │                    │
Major version   Engine Sub Version   Editor Sub Version   Story Version
```

### Major Version

- This number represents a version that is incompatible with a prior version in a breaking way.  
- ie: v0.0.0.0 is incompatible with v1.0.0.0

### Engine Sub Version

- this number represents the version of the game engine in relation to the Major Version.  (this number restarts at 0 when the Major Version Changes)
- content made for a lower engine sub version will always be compatible with versions after it, but not vice versa.
- ie: a dungeon for v0.1.0.0 should work in v0.2.0.0 but a dungeon for v0.2.0.0 is not likely to work for v0.1.0.0

### Editor Sub Version

- this represents the version of the editor relative to the Major version (restarts at 0 when Major version changes)
- changes in this version number only impact your experience for editing a dungeon, and have no compatibility issues (given that other version numbers are matching compatibility)

### Story Version

- this number will never reset after a Major Version change.
- this version is just an indication of how much content is available in the main story and has no impact on compatibility.


