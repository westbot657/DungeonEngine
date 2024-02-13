# pylint: disable=[W,R,C,import-error]

from enum import Enum, auto

import time, re

class _Log:
    _instance = None

    class _track(Enum):
        PASS = auto()
        FAIL = auto()
        NONE = auto()

    def __new__(cls):
        if _Log._instance is None:
            _Log._instance = super().__new__(cls)
            _Log._instance.init()
        return _Log._instance

    def init(self):
        self._tag_colors = {}
        self._disabled_tags = []
        self._tag_whitelist = []
        self.data = []
        self.counting = False
        self.counted = 0
        self.enabled = True

        self._file = None

        self.engine = None
        self.tags = []
        self.silent = False

    def log_to_file(self, file):
        self._file = open(file, "w+", encoding="utf-8")

    def toggle(self):
        self.enabled = not self.enabled

    class _o_off:
        def __init__(self): pass
        def __getitem__(self, tag): return self
        def __call__(self, *values): return None
    _off = _o_off()

    # def __init__(self):
    #     self.tags = []
    
    def __getitem__(self, tag):
        if not self.enabled:
            return _Log._off
        if tag in self._disabled_tags and not tag in self._tag_whitelist:
            self.tags.clear()
            return _Log._off
        self.tags.append(tag)
        return self
    
    def __call__(self, *values, sep=', '):
        out = ""
        for tag in self.tags:
            if tag in self._tag_colors:
                out += f"{self._tag_colors[tag]}[{tag}]\033[0m"
            else:
                out += f"[{tag}]"
        out += f": \033[38;2;160;160;160m{sep.join(str(v) for v in values)}\033[0m"
        out = f"[{time.asctime()[11:19]}] " + out.strip()
        if not self.silent:
            if self.engine:
                self.engine.sendOutput("log", out)
            else:
                print(out)#.encode()) # NOTE: print(out) for CMD version. print(out.encode()) for external version
        
        if self._file:
            self._file.write(re.sub("\033\\[(?:\\d+;?)*m", "", f"{out}\n"))
            self._file.flush()

        self.tags.clear()

    def track(self, num_items, *tags):
        self.counting = True
        self.counted = 0
        self.tags += [t for t in tags]
        self.data = [_Log._track.NONE for i in range(num_items)]

    def success(self):
        if not self.counting: return
        self.data[self.counted] = _Log._track.PASS
        self.counted += 1
        self._check_tracking()

    def fail(self):
        if not self.counting: return
        self.data[self.counted] = _Log._track.FAIL
        self.counted += 1
        self._check_tracking()
    
    def ERROR(self, *tags):
        """
        the last element in the 'tags' tuple will be treated as the output message
        """
        tgs = self.tags
        self.tags = ["ERROR"] + [t for t in tags]
        o = self.tags.pop(-1)
        self(o)
        self.tags = tgs

    def skip(self):
        if not self.counting: return
        self.counted += 1
        self._check_tracking()
    
    def end_track(self):
        if not self.counting: return
        out = ""
        last = _Log._track.NONE
        passes = 0
        fails = 0
        skips = 0
        for stat in self.data:
            if stat == _Log._track.PASS:
                if stat != last: out += "\033[38;2;0;200;20m"
                out += "+"
                passes += 1
            if stat == _Log._track.FAIL:
                if stat != last: out += "\033[38;2;200;20;0m"
                out += "-"
                fails += 1
            if stat == _Log._track.NONE:
                if stat != last: out += "\033[38;2;80;80;80m"
                out += "#"
                skips += 1
            last = stat
        out += f"\033[0m (\033[38;2;0;200;20m+{passes} \033[38;2;200;20;0m-{fails} \033[38;2;80;80;80m#{skips}\033[0m  {passes+fails+skips})"
        self(out)
        self.counting = False

    def _check_tracking(self):
        if not self.counting: return
        if self.counted >= len(self.data):
            self.end_track()

    def stop_log(self):
        if self._file:
            try:
                self._file.close()
            except:
                pass

Log = _Log()
