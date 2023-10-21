#pylint: disable=[W,R,C]

import glob, json, os

def script_gen(namespace: str):
    
    room_jsons = list(glob.glob(f"./Dungeons/{namespace}/rooms/**/*.json", recursive=True))


    for room_json in room_jsons:
        with open(room_json, "r+", encoding="utf-8") as f:
            data: dict = json.load(f)
        
        r = room_json.replace(f"./Dungeons/{namespace}/", "").replace(".json", "").replace("\\", "/")


        if "events" not in data:
            data.update({"events": {}})

        if not os.path.exists(f"./Dungeons/{namespace}/scripts/{r}/"):

            pieces = r.split("/")
            p = ""
            while pieces:
                p += "/" + pieces.pop(0)
                try:
                    os.mkdir(f"./Dungeons/{namespace}/scripts{p}")
                except: pass

            # os.mkdir(f"./Dungeons/{namespace}/scripts/{r}/")

        if not os.path.exists(f"./Dungeons/{namespace}/scripts/{r}/on_enter.ds"):
            
            with open(f"./Dungeons/{namespace}/scripts/{r}/on_enter.ds", "w+", encoding="utf-8") as f:
                f.write("// on_enter script")
            data["events"].update({"on_enter": {"#script": f"{namespace}/scripts/{r}/on_enter"}})
            
        if not os.path.exists(f"./Dungeons/{namespace}/scripts/{r}/on_input.ds"):
            with open(f"./Dungeons/{namespace}/scripts/{r}/on_input.ds", "w+", encoding="utf-8") as f:
                f.write("// on_input script")
            data["events"].update({"on_input": {"#script": f"{namespace}/scripts/{r}/on_input"}})

        with open(room_json, "w+", encoding="utf-8") as f:
            json.dump(data, f, indent=4)





if __name__ == "__main__":
    x = input("Enter dungeon namespace: ")

    script_gen(x)
