# pylint: disable=[W,R,C,import-error]

from threading import Thread
import re, os, sys
from typing import Any
# from colorama import AnsiToWin32
# from pydub import AudioSegment
# from pydub.playback import play
import simpleaudio as sa
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import imp
# import glob

# if getattr(sys, 'frozen', False):
#     # If the application is run as a bundle, the PyInstaller bootloader
#     # extends the sys module by a flag frozen=True and sets the app 
#     # path into variable _MEIPASS'.
#     application_path = sys._MEIPASS
# else:
#     application_path = os.path.dirname(os.path.abspath(__file__))


# sys.path.append(application_path)
# print(f"PATH: {application_path} {sys.path}")

from Engine import Engine


os.system('') # this fixes console ansi colors for some reason

# VOLUME_MOD = 0

# if not os.path.exists("./Dungeons/"):

#     os.mkdir("./Dungeons/")
#     os.mkdir("./Dungeons/world/")

#     x = glob.glob("./DungeonSource/**/*", recursive=True)

#     for f in x:
#         bits = f.replace("\\", "/").replace("DungeonSource", "Dungeons").split("/")[0:-1]
#         p = bits.pop(0) + "/"

#         for b in bits:
#             p += b + "/"
#             if not os.path.exists(p):
#                 os.mkdir(p)
        
#         with open(f, "r", encoding="utf-8") as file:
#             t = file.read()
        
#         with open(f.replace("DungeonSource", "Dungeons"), "w", encoding="utf-8") as file:
#             file.write(t)

try:
    _IOHook = imp.load_source("IOHook", "./IOHook.py")
    IOHook = _IOHook.IOHook

except ImportError as e:
    class IOHook:
        def __init__(self):
            self.print_queue = []
            self.engine = None
            self.running = False

        def init(self, engine):
            self.engine = engine

        def stop(self):
            self.running = False

        def sendOutput(self, target:int|str, text:str|Any):
            if self.running:
                if target == 0:
                    print(f"[engine]: {text}")
                elif target == 1:
                    print(f"[sound]: {text}")
                    if os.path.exists(text):
                        sa.WaveObject.from_wave_file(text).play()

                        # audio = AudioSegment.from_file(text) + VOLUME_MOD

                        

                elif target in [2, 3, 4]:
                    pass
                elif target == "log":
                    print(f"[{target}]: {text}")

                else:
                    print(f"\n\033[38;2;0;0;0m\033[48;2;0;255;0m[>>{target}]\033[0m: \033[38;2;200;200;230m{text}\033[0m")

        def start(self):
            self.running = True
            # o = Thread(target=self._output_loop)
            # o.start()
            i = Thread(target=self._input_loop)
            i.start()


        def _input_loop(self):
            while self.running:
                text = input()
                if m := re.search(r"(?P<targeter>\[(?P<player_id>\d+)\]: *)", text):
                    d = m.groupdict()
                    player_id = int(d["player_id"])
                    txt = text.replace(d["targeter"], "")
                    self.engine.handleInput(player_id, txt)


if __name__ == "__main__":
    # from Engine import Engine
    io_hook = IOHook()
    game_engine = Engine(io_hook)  # pylint: disable=[not-callable]
    game_engine.start()
