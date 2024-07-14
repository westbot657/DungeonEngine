# pylint: disable=W,R,C

import os, sys, re

def main():
    with open("./Engine/ConsoleRunner.py", "r+", encoding="utf-8") as f:
        runner_text = f.read()
    
    t_os_sys = re.sub(r"### COMPILER MARKER ###\n#?(?:[^#]+)### END COMPILER MARKER ###", "### COMPILER MARKER ###\nos.system('')\n### END COMPILER MARKER ###", runner_text)
    t_vs_ver = re.sub(r"### COMPILER MARKER ###\n#?(?:[^#]+)### END COMPILER MARKER ###", "### COMPILER MARKER ###\n# os.system('')\n### END COMPILER MARKER ###", runner_text)

    with open("./Engine/Resources/Logger.py", "r+", encoding="utf-8") as f:
        logger_text = f.read()
    
    t_print_out = re.sub(r"### COMPILER MARKER ###\n#?(?:[^#]+)### END COMPILER MARKER ###", "### COMPILER MARKER ###\n                print(out)\n                ### END COMPILER MARKER ###", logger_text)
    t_print_out_encode = re.sub(r"### COMPILER MARKER ###\n#?(?:[^#]+)### END COMPILER MARKER ###", "### COMPILER MARKER ###\n                print(out.encode())\n                ### END COMPILER MARKER ###", logger_text)

    # VS version
    with open("./Engine/Resources/Logger.py", "w+", encoding="utf-8") as f:
        f.write(t_print_out)
    with open("./Engine/ConsoleRunner.py", "w+", encoding="utf-8") as f:
        f.write(t_vs_ver)
    
    os.system('py -3.12 -O -m PyInstaller "Insert Dungeon Name Here vs.spec"')
    print("VS version compiled")
    
    # CMD version
    with open("./Engine/ConsoleRunner.py", "w+", encoding="utf-8") as f:
        f.write(t_os_sys)
        
    os.system('py -3.12 -O -m PyInstaller "Insert Dungeon Name Here cmd.spec"')
    print("CMD version compiled")
    
    # EXT version
    with open("./Engine/Resources/Logger.py", "w+", encoding="utf-8") as f:
        f.write(t_print_out_encode)
    with open("./Engine/ConsoleRunner.py", "w+", encoding="utf-8") as f:
        f.write(t_vs_ver)

    os.system('py -3.12 -O -m PyInstaller "Insert Dungeon Name Here external.spec"')
    print("EXT version compiled")

if __name__ == "__main__":
    main()

