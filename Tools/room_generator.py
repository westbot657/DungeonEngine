# pylint: disable=[W,R,C]

import json
import os

def generate():
    dungeon_namespace = input("enter dungeon folder name: ")
    
    if not os.path.exists(f"./Dungeons/{dungeon_namespace}"):
        act = input("File does not exist\ncreate|cancel: ")
        if act == "cancel":
            return
        elif act == "continue":
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
                json.dump(dungeon_config, f)
            
            os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/")
            
            entry_room_name = input("enter entry room display name: ")
            
            events = {}
            if input("add dungeon on_enter event? (y/n): ").lower().startswith("y"):
                os.mkdir(f"./Dungeons/{dungeon_namespace}/scripts/rooms/{entry_room}/")
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
            
            with open(f"./Dungeons/{dungeon_namespace}/rooms/{entry_room}.json") as f:
                json.dump({
                    "name": entry_room_name,
                    "interactions": [],
                    "events": events
                }, f)

    if input("add more rooms? (y/n): ").lower().startswith("y"):
        while True:
            room_namespace = input("enter room id: ")
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


generate()

print("Goodbye!")

