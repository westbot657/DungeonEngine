# pylint: disable=[W,R,C,import-error]

from threading import Thread
import re, os, sys
from typing import Any
# from colorama import AnsiToWin32
# from pydub import AudioSegment
# from pydub.playback import play
import simpleaudio as sa
import importlib
import time
from importlib.machinery import SourceFileLoader
# import glob

import socket
from Stockings import Stocking
import random

from Engine import Engine


os.system('') # this fixes console ansi colors for some reason # NOTE: comment out when compiling VS version, it causes Windows 10 to think the exe is a virus

try:
    _IOHook = SourceFileLoader("IOHook", "./IOHook.py").load_module() # pylint: disable=no-value-for-parameter
    IOHook = _IOHook.IOHook

except (ImportError, FileNotFoundError) as e:
    print("Using default IOHook")
    class IOHook:
        def __init__(self):
            self.print_queue = []
            self.engine = None
            self.running = False
            self._server = None
            self.server = None
            self._server_running = False
            self.connections = []

        def init(self, engine):
            self.engine = engine

        def stop(self):
            self.running = False

        def sendOutput(self, target:int|str, text:str|Any):
            if self.running:
                out = ""
                if target == 0:
                    out = f"[engine]: {text}"
                elif target == 1:
                    out = f"[sound]: {text}"
                    if os.path.exists(text):
                        sa.WaveObject.from_wave_file(text).play()

                        # audio = AudioSegment.from_file(text) + VOLUME_MOD

                elif target in [2, 3, 4]:
                    pass
                elif target == "log":
                    out = f"[{target}]: {text}"
                else:
                    out = f"\n\033[38;2;0;0;0m\033[48;2;0;255;0m[>>{target}]\033[0m: \033[38;2;200;200;230m{text}\033[0m"
                
                if out:
                    print(out)
                    if self._server_running:
                        self.broadcast(out)

        def start(self):
            self.running = True
            # o = Thread(target=self._output_loop)
            # o.start()
            i = Thread(target=self._input_loop)
            i.daemon = True
            i.start()

        def accepter(self, conn, addr):
            c = Stocking(conn)
            t = time.time()
            
            while not c.handshakeComplete:
                if t + 10 < time.time():
                    print(f"\033[38;2;240;130;130mConnection from \033[0m{addr} \033[38;2;240;130;130mtimed out before fully connected\033[0m")
                    return
            self.connections.append(c)
            print(f"\033[38;2;130;250;130mConnection from \033[0m{addr} \033[38;2;130;250;130maccepted!\033[0m")

        def connect_loop(self):
            while self.running:
                conn, addr = self._server.accept()
                acc = Thread(target=self.accepter, args=(conn, addr))
                acc.daemon = True
                acc.start()

        def _input_loop(self):
            while self.running:
                text = input()
                self.do_input(text)

        def do_input(self, text):
            if m := re.search(r"(?P<targeter>\[(?P<player_id>\d+)\]: *)", text):
                d = m.groupdict()
                player_id = int(d["player_id"])
                txt = text.replace(d["targeter"], "")
                self.engine.handleInput(player_id, txt)
                
            elif m := re.match(r"/server *(?P<port>\d{5})?", text):
                d = m.groupdict()
                port = min(max(1000, int(d["port"] or random.randint(10000, 25560))), 25565)
                self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._server.bind(("127.0.0.1", port))
                self._server.listen(5)
                self._server_running = True
                cl = Thread(target=self.connect_loop)
                # cl.daemon = True
                cl.start()
                rl = Thread(target=self.read_loop)
                # rl.daemon = True
                rl.start()
                print(f"Server started on port \033[38;2;100;255;100m{port}\033[0m.")


        def broadcast(self, data:str):
            for conn in self.connections:
                conn.write(data)

        def read_loop(self):
            while True:
                for conn in self.connections.copy():
                    try:
                        if r := conn.read():
                            if r.strip():
                                self.do_input(r.strip())
                    except BrokenPipeError as e:
                        self.connections.remove(conn)


if __name__ == "__main__":
    # from Engine import Engine
    
    argv = sys.argv[1:]
    print(f"{argv=}")
    if argv:
        host, port = argv
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to server\r")
        try:
            sock.connect((host, int(port)))
        except Exception as e:
            print("Could not connect.    \n")
            exit()

        conn = Stocking(sock)

        dots = 0
        print("                    \r")
        while not conn.handshakeComplete:
            print(f"Connecting{'.'*dots}", end="\r")
            time.sleep(0.5)
            dots += 1
            if dots > 3:
                dots = 0
        print("             ", end="\r")

        def input_loop():
            while True:
                text = input().strip()
                if text:
                    try:
                        conn.write(text)
                    except BrokenPipeError as e:
                        return
        

        t = Thread(target=input_loop)
        # t.daemon = True
        t.start()

        while True:
            try:
                if r := conn.read():
                    if r == "%disconnect%":
                        print(f"Disconnected from server.")
                        exit()
                    print(r)
            except BrokenPipeError as e:
                print("\033[38;2;255;140;140mCONNECTION LOST\033[0m\r")
                exit()

    else:
        io_hook = IOHook()
        game_engine = Engine(io_hook)  # pylint: disable=[not-callable]
        # print("starting engine")
        game_engine.run()

