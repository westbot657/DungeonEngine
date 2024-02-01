# pylint: disable=[W,R,C]

from threading import Thread
import simpleaudio as sa
import os
import re


# You can modify this class to change how/where the game sends output.

print("USING CUSTOM HOOK")

class IOHook:
    def __init__(self):
        self.print_queue = []
        self.engine = None
        self.running = False

    # required function
    def init(self, engine):
        self.engine = engine

    # required function
    def stop(self):
        self.running = False

    # required function
    def sendOutput(self, target:int|str, text:str):
        """
        Targets:
        log: Debug Logger
        0: Engine
        1: Sound System
        2: Inventory UI
        3: Combat UI
        """
        if self.running:
            if target == 0:
                print(f"[engine]: {text}")
            if target == 1:
                print(f"[sound]: {text}")
                if os.path.exists(text):
                    sa.WaveObject.from_wave_file(text).play()
            if target in [2, 3]:
                pass
                
            elif target == "log":
                print(f"[{target}]: {text}")

            else:
                print(f"\n\033[38;2;0;0;0m\033[48;2;0;255;0m[>>{target}]\033[0m: \033[38;2;200;200;230m{text}\033[0m")

    # required function
    def start(self):
        self.running = True
        i = Thread(target=self._input_loop)
        i.start()



    def _input_loop(self):
        while self.running:
            text = input()
            if m := re.search(r"(?P<targeter>\[(?P<player_id>\d+)\]: *)", text):
                d = m.groupdict()
                player_id = int(d["player_id"])
                txt = text.replace(d["targeter"], "")
                # it doesn't matter how you receive input, but this function:
                self.engine.handleInput(player_id, txt)
                # must be used to tell the engine to handle the input
                # the function takes 2 arguments: the id of the player (int), and their input (str)
