# pylint: disable=[W,R,C,import-error]

from threading import Thread
import re

class ConsoleIOHook:
    def __init__(self):
        self.print_queue = []
        self.engine = None
        self.running = False
    
    def init(self, engine):
        self.engine = engine

    def stop(self):
        self.running = False
        
    def sendOutput(self, target:int|str, prompt:str):
        self.print_queue.append((target, prompt))

    def start(self):
        self.running = True
        o = Thread(target=self._output_loop)
        o.start()
        i = Thread(target=self._input_loop)
        i.start()
    
    def _output_loop(self):
        while self.running:
            while self.print_queue:
                target, text = self.print_queue.pop(0)
                print(f"[@game->{target}]: {text}")

    def _input_loop(self):
        while self.running:
            text = input()
            if m := re.search(r"(?P<targeter>\[(?P<player_id>\d+)\]: *)", text):
                d = m.groupdict()
                player_id = int(d["player_id"])
                txt = text.replace(d["targeter"], "")
                self.engine.handleInput(player_id, txt)


if __name__ == "__main__":
    from Engine import Engine
    console_hook = ConsoleIOHook()
    game_engine = Engine(console_hook) # pylint: disable=[not-callable]
    game_engine.start()
    




