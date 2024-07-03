
# Insert Dungeon Name Here

### A text-adventure style multiplayer game engine

**CURRENTLY IN BETA**

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

see the [wiki](https://github.com/westbot657/DungeonEngine/wiki)
