# pylint: disable=W,R,C


class EditorMimic:
    def __init__(self, editor, overrider):
        super().__setattr__("_EditorMimic__editor", editor)
        super().__setattr__("_EditorMimic__overrider", overrider)
    def __getattribute__(self, __name: str):
        editor = super().__getattribute__("_EditorMimic__editor")
        overrider = super().__getattribute__("_EditorMimic__overrider")
        if hasattr(overrider, __name):
            return getattr(overrider, __name)
        elif hasattr(editor, __name):
            return getattr(editor, __name)
        else:
            raise AttributeError(f"'EditorMimic' object has no attribute '{__name}'")
    def __setattr__(self, __name: str, __value) -> None:
        if __name == "_editor":
            return super().__setattr__("_EditorMimic__editor", __value)
        editor = super().__getattribute__("_EditorMimic__editor")
        overrider = super().__getattribute__("_EditorMimic__overrider")
        if hasattr(overrider, __name):
            setattr(overrider, __name, __value)
        elif hasattr(editor, __name):
            setattr(editor, __name, __value)
        else:
            setattr(overrider, __name, __value)
