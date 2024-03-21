# pylint: disable=[W,R,C]

try:
    from GraphicsEngine.Util import PopoutElement
    from GraphicsEngine.UIElement import UIElement
    from GraphicsEngine.NumberedTextArea import NumberedTextArea
    from GraphicsEngine.MultilineTextBox import MultilineTextBox, Selection, Cursor
except ImportError:
    from Util import PopoutElement
    from UIElement import UIElement
    from NumberedTextArea import NumberedTextArea
    from MultilineTextBox import MultilineTextBox, Selection, Cursor

import re

@PopoutElement()
class FileEditor(UIElement):
    
    def __init__(self, x, y, width, height, file_location, file_name, editor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.file_location = file_location
        self.file_name = file_name
        
        with open(self.file_location, "r+", encoding="utf-8") as f:
            self.contents = f.read()
        
        self.edit_area = NumberedTextArea(self.x, self.y, self.width, self.height, text_bg_color=(31, 31, 31), scroll_speed=45)
        self.edit_area.set_content(self.contents)
        self.edit_area.editable.save_history()
        self.edit_area.editable.on_save(self.save_file)

        match file_name.rsplit(".", 1)[-1]:
            case "json"|"piskel":
                self.edit_area.editable.color_text = self.json_colors

            case "ds"|"dungeon_script"|"dse":
                self.edit_area.editable.color_text = self.ds_colors

            case "md":
                self.edit_area.editable.color_text = self.md_colors

        self.edit_area.editable.refresh_surfaces()

    def __repr__(self):
        return f"File Editor: {self.file_location}/{self.file_name}"

    def save_file(self, text_box:MultilineTextBox, content:str, selection:Selection|None, cursorPos:Cursor):
        with open(self.file_location, "w+", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def json_colors(text:str) -> str:

        def repl(match:re.Match) -> str:
            t = match.group()

            if (m := re.match(r"(\"(?:\\.|[^\"\\])*\":)", t)): # "...":
                t = re.sub(r"(\\.)", "\033[38;2;215;186;125m\\1\033[38;2;156;220;254m", m.group())
                return f"\033[38;2;156;220;254m{t[0:-1]}\033[0m:"
            
            elif (m := re.match(r"(\"(?:\\.|[^\"\\])*\")", t)): # "..."
                t = re.sub(r"(\\.)", "\033[38;2;215;186;125m\\1\033[38;2;206;145;120m", m.group())
                return f"\033[38;2;206;145;120m{t}\033[0m"
            
            elif (m := re.match(r"\b(true|false|null)\b", t)): # keywords - and/or/not/...
                return f"\033[38;2;86;156;214m{m.group()}\033[0m"
            
            elif (m := re.match(r"\d+(?:\.\d+)?", t)):
                return f"\033[38;2;181;206;168m{m.group()}\033[0m"
            
            else:
                return t

        return re.sub(r"((?:\"(?:\\.|[^\"\\])*\":)|(?:\"(?:\\.|[^\"\\])*\")|\d+(\.\d+)?|\b(true|false|null)\b)", repl, text)

    @staticmethod
    def ds_colors(text:str) -> str:

        def repl(match:re.Match) -> str:
            t = match.group()

            if (m := re.match(r"(\/\*(?:\\.|\*[^/]|[^*])*\*\/|\/\/.*)", t)): # /* */ # //
                return f"\033[38;2;106;153;85m{m.group()}\033[0m"
            
            elif (m := re.match(r"(\"(?:\\.|[^\"\\])*\"|\'(?:\\.|[^\'\\])*\')", t)): # "..." # '...'
                t = re.sub(r"(\\.|`[^`]*`)", "\033[38;2;215;186;125m\\1\033[38;2;206;145;120m", m.group())
                return f"\033[38;2;206;145;120m{t}\033[0m"
            
            elif (m := re.match(r"\[([^:]+:)((?:[^/\]]+/)*)([^\]]+)\]", t)): # [engine:combat/start]
                ns, g, f = m.groups()
                return f"[\033[38;2;86;156;214m{ns}\033[38;2;156;220;254m{g}\033[38;2;220;220;170m{f}\033[0m]"
            
            elif (m := re.match(r"(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)(?P<after> *\()", t)):
                return f"\033[38;2;220;220;170m{m.groupdict()["name"]}\033[0m{m.groupdict()["after"]}"
            
            elif (m := re.match(r"<([^>]+)>", t)): # <variables>
                t = m.groups()[0]

                if t.startswith("#"):
                    v = re.sub(r"([./])", "\033[0m\\1\033[38;2;209;105;105m", t)
                    return f"<\033[38;2;209;105;105m{v}\033[0m>"
                
                elif t.startswith("%"):
                    v = re.sub(r"([./])", "\033[0m\\1\033[38;2;79;193;255m", t)
                    return f"<\033[38;2;79;193;255m{v}\033[0m>"
                
                elif t.startswith("$"):
                    v = re.sub(r"([./])", "\033[0m\\1\033[38;2;220;220;170m", t)
                    return f"<\033[38;2;220;220;170m{v}\033[0m>"
                
                else:
                    v = re.sub(r"([./])", "\033[0m\\1\033[38;2;78;201;176m", t)
                    return f"<\033[38;2;78;201;176m{v}\033[0m>"
                
            elif (m := re.match(r"(@[^:]*:|#|%|\$[a-zA-Z_][a-zA-Z0-9_]*)", t)): # @tags:
                return f"\033[38;2;79;193;255m{m.group()}\033[0m"
            
            elif (m := re.match(r"\b(if|elif|else|break|return|pass|for|in)\b", t)): # keywords - if/elif/else/...
                return f"\033[38;2;197;134;192m{m.group()}\033[0m"
            
            elif (m := re.match(r"\b(true|false|none|not|and|or)\b", t)): # keywords - and/or/not/...
                return f"\033[38;2;86;156;214m{m.group()}\033[0m"
            
            elif (m := re.match(r"\d+(?:\.\d+)?", t)):
                return f"\033[38;2;181;206;168m{m.group()}\033[0m"
            
            else:
                return t
            
        return re.sub(r"(\/\*(?:\\.|\*[^/]|[^*])*\*\/|\/\/.*|(?:\"(?:\\.|[^\"\\])*\"|\'(?:\\.|[^\'\\])*\')|\[[^:]+:[^\]]+\]|[a-zA-Z_][a-zA-Z0-9_]* *\(|<=|>=|<<|>>|==|!=|<[^>]+>|@[^:]+:|\$[a-zA-Z_0-9]+|\d+(?:\.\d+)?|\b(and|if|or|not|elif|else|not|return|break|pass|for|in)\b|#|%)", repl, text)

    @staticmethod
    def md_colors(text:str) -> str:

        text = re.sub(r"(?<=\n)( *#{1,6}.*)", "\033[38;2;86;156;214m\\1\033[0m", text)
        text = re.sub(r"(?<=\n)( *-(?!-))", "\033[38;2;103;150;230m\\1\033[0m", text)

        def repl(match:re.Match) -> str:
            t = match.group()

            if (m := re.match(r"#{1,6}[^#\n].*", t)):
                return f"\033[38;2;86;156;214m{m.group()}\033[0m"
            elif (m := re.match(r" *(\-|\+|\*|\d+(:|\.))", t)):
                return f"\033[38;2;103;150;230m{m.group()}\033[0m"
            # elif (m := re.match(r"[│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌]+", t)):
            #     return f"\033[38;2;150;150;150m{m.group()}\033[0m"
            else:
                return t

        return re.sub(r"((?:^|(?<=\n))#{1,6}[^#\n].*|(?:^|(?<=\n)) *(\-|\+|\*)|(?:^|(?<=\n)) *\d+(?:\.|:)|[│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌]+)", repl, text)

    def _update_layout(self, editor):
        self.edit_area.width = self.width
        self.edit_area.height = self.height
        
        self.edit_area._update_layout()

    def _update(self, editor, X, Y):
        self.edit_area._update(editor, X, Y)
    
    def _event(self, editor, X, Y):
        
        if editor._do_layout_update:
            self._update_layout(None)
        
        self.edit_area.x = self.x
        self.edit_area.y = self.y
        self.edit_area.width = self.width
        self.edit_area.height = self.height
        
        self.edit_area._event(editor, X, Y)

