# pylint: disable=[W,R,C,import-error]
from typing import Any, Generator

class Util:
    ...

    @staticmethod
    def getRoundedUpKey(key:float, data:dict[float]):
        old = 0
        for v in data:
            if old <= key <= v:
                return v
            old = v

    @staticmethod
    def getRoundedDownKey(key:float, data:dict[float]):
        old = 0
        for v in data:
            if old <= key <= v:
                return old
            old = v

    # # May not need these? (hopefuly)
    # @staticmethod
    # def output(*values, sep=" ", end="\n"):
    #     out = sep.join([str(v) for v in values])

    #     print(out.replace("&", "&amp;").replace("\n", "&new;").encode("utf-8"), end=end)

    # @staticmethod
    # def message(player, *values, sep=" ", end="\n"):
    #     out = sep.join([str(v) for v in values])

    #     if hasattr(player, "user_id"):
    #         print(f"[@game->{player.user_id}]: {out}".replace("&", "&amp;").replace("\n", "&new;").encode("utf-8"), end=end)

    #     else:
    #         print(f"[@game]: {player}{sep}{out}".replace("&", "&amp;").replace("\n", "&new;").encode("utf-8"), end=end)

    @staticmethod
    def generator_started(gen:Generator):
        return gen.gi_frame.f_lasti != -1

    @staticmethod
    def getDurabilityBar(current_value, max_value, bar_width=10):
        if max_value < 0:
            return f"[{'INFINITE': ^{bar_width}}]"
        percent = current_value / max_value
        filled = int(percent * bar_width)

        return f"[{'='*filled:-<{bar_width}}] {current_value}/{max_value}"

    @staticmethod
    def deepCopy(data:Any):
        if isinstance(data, dict):
            dat = {}
            for key, value in data.items():
                dat.update({key: Util.deepCopy(value)})
            return dat
        elif isinstance(data, list):
            dat = []
            for val in data:
                dat.append(Util.deepCopy(val))
            return dat
        else:
            return data