# pylint: disable=[W,R,C,import-error]


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

    # May not need these? (hopefuly)
    @staticmethod
    def output(*values, sep=" ", end="\n"):
        out = sep.join([str(v) for v in values])

        print(out.replace("&", "&amp;").replace("\n", "&new;").encode("utf-8"), end=end)

    @staticmethod
    def message(player, *values, sep=" ", end="\n"):
        out = sep.join([str(v) for v in values])

        if hasattr(player, "user_id"):
            print(f"[@game->{player.user_id}]: {out}".replace("&", "&amp;").replace("\n", "&new;").encode("utf-8"), end=end)

        else:
            print(f"[@game]: {player}{sep}{out}".replace("&", "&amp;").replace("\n", "&new;").encode("utf-8"), end=end)
