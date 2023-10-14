# pylint: disable=[W,R,C,import-error]
from typing import Any, Generator

class Util:

    @classmethod
    def flatten_list(cls, ls:list):
        out = []
        for k in ls:
            if isinstance(k, list):
                out += cls.flatten_list(k)
            else:
                out.append(k)
        return out

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
    #         print(f"[>>{player.user_id}]: {out}".replace("&", "&amp;").replace("\n", "&new;").encode("utf-8"), end=end)

    #     else:
    #         print(f"[>>]: {player}{sep}{out}".replace("&", "&amp;").replace("\n", "&new;").encode("utf-8"), end=end)

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

    @classmethod
    def deepCopy(cls, data:Any):
        if isinstance(data, dict):
            dat = {}
            for key, value in data.items():
                dat.update({key: cls.deepCopy(value)})
            return dat
        elif isinstance(data, list):
            dat = []
            for val in data:
                dat.append(cls.deepCopy(val))
            return dat
        else:
            return data

    @staticmethod
    def wrapNumber(min_num, x, max_num):
        diff = (max_num+1) - min_num

        while x > max_num:
            x -= diff
        while x < min_num:
            x += diff
        return x
