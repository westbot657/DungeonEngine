# pylint: disable=[W,R,C,import-error]


class GraphicsEngine:

    def __init__(self):
        self.tick_events = []


    def events(self):
        return self.tick_events.copy()



    def main_loop(self):
        ...


