# pylint: disable=[W,R,C]

try:
    from GraphicsEngine.UIElement import UIElement
    from GraphicsEngine.RenderPrimitives import Image
    from GraphicsEngine.Options import PATH
    from GraphicsEngine.AttributePanel import AttributePanel
    from GraphicsEngine.ConstructionCanvas import ConstructionCanvas
    from GraphicsEngine.FunctionalElements import Button
    from GraphicsEngine.AdvancedPanels.PanelTree import PanelTree
    from GraphicsEngine.AdvancedPanels.ShelfPanel import ShelfPanel
except ImportError:
    from UIElement import UIElement
    from RenderPrimitives import Image
    from Options import PATH
    from AttributePanel import AttributePanel
    from ConstructionCanvas import ConstructionCanvas
    from FunctionalElements import Button
    from AdvancedPanels.PanelTree import PanelTree
    from AdvancedPanels.ShelfPanel import ShelfPanel

class VisibilityToggle:
    def __init__(self, sub_app, typ, button, alt_text1, alt_text2, frames):
        self.sub_app = sub_app
        self.typ = typ
        self.button = button
        self.alt_text1 = alt_text1
        self.alt_text2 = alt_text2
        self.frames = frames
        
    def __call__(self, *_, set=None, **__):
        if set is not None:
            self.sub_app.visibility_toggled[self.typ] = not set
        if self.sub_app.visibility_toggled[self.typ]:
            self.button._alt_text = self.alt_text2
            self.button._bg_color = self.button.bg_color = self.frames[0]
            self.button.hover_color = self.frames[1]
        else:
            self.button._alt_text = self.alt_text1
            self.button._bg_color = self.button.bg_color = self.frames[2]
            self.button.hover_color = self.frames[3]
            
        self.sub_app.visibility_toggled[self.typ] = not self.sub_app.visibility_toggled[self.typ]



class AdvancedEditorSubApp(UIElement):
    
    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.editor = editor
        self.children = []
        self.popouts = {}
        
        self.construction_canvas = ConstructionCanvas(self, editor, 102, 22, editor.width-452, editor.height-111)
        self.children.append(self.construction_canvas)
        
        self.visibility_types = [
            None,
            "weapon", "ammo", "armor", "item", None,
            "road", "room", None,
            "combat", "script",
            None
        ]
        
        self.visibility_offsets = {}
        self.visibility_icons = {}
        self.visibility_toggles = {}
        self.visibility_toggled = {}
        self.visibility_groups = {}
        self.empty_visibility_toggle_spots = []
        
        self.object_tree = PanelTree(editor.width-352, 22, 350, editor.height-111, editor)
        self.children.append(self.object_tree)
        
        base_x = 102
        base_y = editor.height-100
        x_offset = 0
        seperator_width = 10
        
        for typ in self.visibility_types:
            if typ is None:
                img = Image(f"{PATH}/advanced_editor/empty_selector_spot.png", base_x+x_offset, base_y, seperator_width, 50)
                self.empty_visibility_toggle_spots.append(img)
                x_offset += seperator_width
                self.children.append(img)
                continue
            
            self.visibility_offsets.update({typ: x_offset})
            frames = [
                Image(f"{PATH}/advanced_editor/{typ}_visibility_selector.png", 0, 0, 50, 50),
                Image(f"{PATH}/advanced_editor/{typ}_visibility_selector_hovered.png", 0, 0, 50, 50),
                Image(f"{PATH}/advanced_editor/{typ}_visibility_selector_selected.png", 0, 0, 50, 50),
                Image(f"{PATH}/advanced_editor/{typ}_visibility_selector_selected_hovered.png", 0, 0, 50, 50)
            ]
            self.visibility_icons.update({typ: frames})
            
            button = Button(base_x+x_offset, base_y, 50, 50, "", frames[2], hover_color=frames[3], click_color=frames[2])
            alt_text1 = f"Hide {typ}" + ("" if typ.endswith(("r", "o")) else "s")
            alt_text2 = f"Show {alt_text1[5:]}"
            button._alt_text = alt_text1
            self.visibility_toggled.update({typ: True})
            
            on_click = VisibilityToggle(self, typ, button, alt_text1, alt_text2, frames)
            self.visibility_toggles.update({typ: (button, on_click)})

            button.on_left_click = on_click
            self.children.append(button)
            self.visibility_groups.update({typ: []})
            x_offset += 50
        
        img = Image(f"{PATH}/advanced_editor/selector_block.png", base_x+x_offset, base_y, 25, 79)
        self.children.append(img)
        self.empty_visibility_toggle_spots.append(img)
        
        a = AttributePanel(200, 200, 200, 400, True)
        a.scroll_directions = 0b1010
        a.rebuild()
        
        a_shelf = ShelfPanel(340, 35, "Test 1", a, self.construction_canvas)

        b = AttributePanel(500, 300, 300, 400, True)
        b.scroll_directions = 0b0110
        b.glow_time = -1
        b.glowing = True
        b.rebuild()
        
        b_shelf = ShelfPanel(340, 35, "Test 2", b, self.construction_canvas)

        self.object_tree.tree += [a_shelf, b_shelf]

        self.visibility_groups["weapon"] += [a, b]
        
    
    def _update(self, editor, X, Y):
        for child in self.children:
            child._update(editor, X, Y)
    
    def _event(self, editor, X, Y):
        
        if editor._do_layout_update:
            self._update_layout(editor)
        
        for child in self.children[::-1]:
            child._event(editor, X, Y)
            
    def _update_layout(self, editor):
        for button, _ in self.visibility_toggles.values():
            button.y = editor.height-100
        for blank in self.empty_visibility_toggle_spots:
            blank.y = editor.height-100
        
        self.construction_canvas.width = editor.width-452
        self.construction_canvas.height = editor.height-111
        self.construction_canvas.rebuild()
        self.object_tree.x = editor.width-352
        self.object_tree.height = editor.height-111
