# pylint: disable=[W,R,C]

# README:
# run this file to help automate dungeon setup.
# 
# this code will help you set up your dungeon
# folder, and will generate json and ds files
# for you.
# 
# If your dungeon folder already exists, this code
# will assist in adding rooms to the dungeon
# 



import json
import os

def generate():
    dungeon_namespace = input("enter dungeon folder name: ")
    
    if not os.path.exists(f"./Dungeons/{dungeon_namespace}"):
        act = input("Dungeon does not exist.\ncreate|cancel: ")
        if act == "cancel":
            return
        elif act == "create":
            os.mkdir(f"./Dungeons/{dungeon_namespace}/")
            os.mkdir(f"./Dungeons/{dungeon_namespace}/rooms/")
            os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/")
            os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/")
            os.mkdir(f"./Dungeons/{dungeon_namespace}/resources/")
            
            dungeon_name = input("enter dungeon display name: ")
            
            events = {}
            if input("add dungeon on_enter event? (y/n): ").lower().startswith("y"):
                os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/{dungeon_namespace}/")
                events.update({
                    "on_enter": {
                        "#script": f"{dungeon_namespace}/scripts/{dungeon_namespace}/on_enter"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/{dungeon_namespace}/on_enter.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {dungeon_namespace} on_enter script")
                
            if input("add dungeon on_input event? (y/n): ").lower().startswith("y"):
                if not os.path.exists(f"./Dungeons/{dungeon_namespace}/scripts/{dungeon_namespace}/"):
                    os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/{dungeon_namespace}/")
                
                events.update({
                    "on_input": {
                        "#script": f"{dungeon_namespace}/scripts/{dungeon_namespace}/on_input"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/{dungeon_namespace}/on_input.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {dungeon_namespace} on_input script")
            if input("add dungeon on_exit event? (y/n): ").lower().startswith("y"):
                if not os.path.exists(f"./Dungeons/{dungeon_namespace}/scripts/{dungeon_namespace}/"):
                    os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/{dungeon_namespace}/")
                
                events.update({
                    "on_exit": {
                        "#script": f"{dungeon_namespace}/scripts/{dungeon_namespace}/on_exit"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/{dungeon_namespace}/on_exit.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {dungeon_namespace} on_exit script")
                
            
            entry_room = input("enter entry room id: ")
            
            dungeon_config = {
                "name": dungeon_name,
                "version": 1,
                "interactions": [],
                "entry_point": f"{dungeon_namespace}:rooms/{entry_room}",
                "events": events
            }
            
            with open(f"./Dungeons/{dungeon_namespace}/{dungeon_namespace}.json", "w+", encoding="utf-8") as f:
                json.dump(dungeon_config, f, indent=4)
            
            os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/")
            
            entry_room_name = input("enter entry room display name: ")
            
            events = {}
            if input("add dungeon on_enter event? (y/n): ").lower().startswith("y"):
                try:
                    os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/")
                except FileExistsError:
                    pass
                events.update({
                    "on_enter": {
                        "#script": f"{dungeon_namespace}/scripts/rooms/{entry_room}/on_enter"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/on_enter.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {entry_room_name} on_enter script")
                
            if input("add dungeon on_input event? (y/n): ").lower().startswith("y"):
                if not os.path.exists(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/"):
                    os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/")
                
                events.update({
                    "on_input": {
                        "#script": f"{dungeon_namespace}/scripts/rooms/{entry_room}/on_input"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/on_input.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {entry_room_name} on_input script")
            if input("add dungeon on_exit event? (y/n): ").lower().startswith("y"):
                if not os.path.exists(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/"):
                    os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/")
                
                events.update({
                    "on_exit": {
                        "#script": f"{dungeon_namespace}/scripts/rooms/{entry_room}/on_exit"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/on_exit.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {entry_room_name} on_exit script")
            
            with open(f"./Dungeons/{dungeon_namespace}/rooms/{entry_room}.json", "w+", encoding="utf-8") as f:
                json.dump({
                    "name": entry_room_name,
                    "interactions": [],
                    "events": events
                }, f, indent=4)

    if input("add more rooms? (y/n): ").lower().startswith("y"):
        while True:
            room_namespace = input("enter room id (or EXIT to stop): ")
            
            if room_namespace == "EXIT":
                break
            room_name = input("enter room display name: ")
            events = {}
            
            if input("add on_enter event? (y/n): ").lower().startswith("y"):
                os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{room_namespace}/")
                events.update({
                    "on_enter": {
                        "#script": f"{dungeon_namespace}/scripts/rooms/{room_namespace}/on_enter"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{room_namespace}/on_enter.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {room_name} on_enter script")
            
            if input("add on_input event? (y/n): ").lower().startswith("y"):
                if not os.path.exists(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{room_namespace}/"):
                    os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{room_namespace}/")
                events.update({
                    "on_input": {
                        "#script": f"{dungeon_namespace}/scripts/rooms/{room_namespace}/on_input"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{room_namespace}/on_input.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {room_name} on_input script")
            
            if input("add on_exit event? (y/n): ").lower().startswith("y"):
                if not os.path.exists(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{room_namespace}/"):
                    os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{room_namespace}/")
                events.update({
                    "on_exit": {
                        "#script": f"{dungeon_namespace}/scripts/rooms/{room_namespace}/on_exit"
                    }
                })
                with open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{room_namespace}/on_exit.ds", "w+", encoding="utf-8") as f:
                    f.write(f"// {room_name} on_exit script")

            with open(f"./Dungeons/{dungeon_namespace}/rooms/{room_namespace}.json", "w+", encoding="utf-8") as f:
                json.dump({
                    "name": room_name,
                    "interactions": [],
                    "events": events
                }, f)

    if input("Generate room connections? (y/n): ").lower().startswith("y"):
        while True:
            start = input("enter room id to add passages/doors from (type EXIT to stop): ")
            

            if start == "EXIT":
                break

            # check that start room exists
            
            if not os.path.exists(f"./Dungeons/{dungeon_namespace}/rooms/{start}.json"):
                print("That room does not exist!")
                continue
            
            if not os.path.exists(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{start}/on_input.ds"):
                os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{start}/")
                open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{start}/on_input.ds", "w+", encoding="utf-8").close()
            
            
            
            
            ends = []
            print("enter connection room ids (each on a new line, enter a blank line to stop):")
            print("examples:\n> door <room>\n> passage /<room>\n")
            
            while (i := input(">")):
                
                t, name = i.split(" ")
                
                # check that `i` exists
                
                if not os.path.exists(f"./Dungeons/{dungeon_namespace}/rooms/{name}.json"):
                    print("That room does not exist!")
                    continue

                if t == "remove":
                    x = 0
                    for _, _t in ends.copy():
                        if _t == name:
                            ends.pop(x)
                            print(f"removed {_t}")
                            break
                        x += 1
                    continue
                
                if t not in ["passage", "door"]:
                    print("Invalid connection type")
                    continue
                
                ends.append((name, t))
            
            
            code = ["[engine:text/match]([engine:text/set_case](<#text>, \"lower\"), \"search\")"]
            
            with open(f"./Dungeons/{dungeon_namespace}/rooms/{start}.json", "r+", encoding="utf-8") as f:
                room_data: dict = json.load(f)
            
            for room_id, conn_type in ends:
                if "interactions" not in room_data:
                    room_data.update({"interactions": []})
                room_data["interactions"].append(x := {
                    "type": f"engine:interactable/{conn_type}",
                    "id": f"{room_id.replace('/', '_')}_{conn_type}",
                    "target": f"{dungeon_namespace}:rooms/{room_id}"
                })

                print(f"{start} -> {room_id} ({conn_type})")

                code += [
                    f"@pattern: \"{input('input text to interact : ')}\" # {{",
                    f"    [engine:interaction/interact](\".{room_id.replace('/', '_')}_{conn_type}\")",
                    "}"
                ]

                
                if y := input("travel message? : "):
                    x.update({
                        "travel_message": y
                    })
            
            with open(f"./Dungeons/{dungeon_namespace}/rooms/{start}.json", "w+", encoding="utf-8") as f:
                json.dump(room_data, f, indent=4)
            
            with open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{start}/on_input.ds", "r+", encoding="utf-8") as f:
                t = f.read()

            with open(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{start}/on_input.ds", "w+", encoding="utf-8") as f:
                f.write(t + f"\n\n\n// generated interaction code:\n" + "\n".join(code) + "\n\n\n")
            


generate()

print("Goodbye!")

