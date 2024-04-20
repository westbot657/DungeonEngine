# pylint: disable=[W,R,C, import-error]
from UIElement import UIElement
from RenderPrimitives import Image
from FunctionalElements import Button
from AttributePanel import AttributePanel
from MultilineTextBox import MultilineTextBox
from Options import PATH, TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG3_COLOR, TEXT_SIZE
from CursorFocusTextBox import CursorFocusTextBox

import time

class ShelfPanel(UIElement):
    
    visibility_frames = (
        Image(f"{PATH}/advanced_editor/panel_hidden.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_hidden_hovered.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_shown.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_shown_hovered.png", 0, 0, 33, 33)
    )
    refocus_frames = (
        Image(f"{PATH}/advanced_editor/panel_focus.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_focus_hovered.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_focus_selected.png", 0, 0, 33, 33)
    )
    menu_frames = (
        Image(f"{PATH}/advanced_editor/panel_ellipsis_menu.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_ellipsis_menu_hovered.png", 0, 0, 33, 33),
    )
    
    def __init__(self, width, height, label, category, attr_panel, canvas, editor, tags:list|None=None):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.label = label # Used for panel search filtering
        self.category = category
        self.tags = tags or []
        self.attr_panel = attr_panel
        self.effective_height = height
        self.canvas = canvas
        self.panel = AttributePanel(0, 0, width, height, False, TEXT_BG_COLOR)
        self.panel.texture_scale = 1
        self.panel.rebuild()
        self.label_text_box = CursorFocusTextBox(12, 9, 150, TEXT_SIZE+4, editor, "enter label...", content=label)
        # self.label_text_box.collides = self.collide_override
        self.label_text_box.on_enter(self.set_label)
        self.visibility_button = Button(self.width-68, (height-33)/2, 33, 33, "", self.visibility_frames[2], hover_color=self.visibility_frames[3], click_color=self.visibility_frames[3])
        self.visibility_button.on_left_click = self.visibility_toggle
        self.focus_button = Button(self.width-34, (height-33)/2, 33, 33, "", self.refocus_frames[0], hover_color=self.refocus_frames[1], click_color=self.refocus_frames[2])
        self.focus_button.on_left_click = self.focus_object
        self.attr_panel_visible = True
        self.placer = self._placer = None
        self.placer_offset = (self.width-35, (height-33)/2)
        self.children = []

    def set_label(self, textbox):
        self.label = textbox.get_content()
    
    def visibility_toggle(self, editor, *_, **__):
        self.set_label(self.label_text_box)
        if self.attr_panel_visible:
            self.visibility_button._bg_color = self.visibility_button.bg_color = self.visibility_frames[0]
            self.visibility_button.hover_color = self.visibility_button.click_color = self.visibility_frames[1]
            self.label_text_box.set_text_color(TEXT_BG3_COLOR)
        else:
            self.visibility_button._bg_color = self.visibility_button.bg_color = self.visibility_frames[2]
            self.visibility_button.hover_color = self.visibility_button.click_color = self.visibility_frames[3]
            self.label_text_box.set_text_color(TEXT_COLOR)
        self.label_text_box.set_content(self.label)
        self.attr_panel.visible = self.attr_panel_visible = not self.attr_panel_visible
    
    def focus_object(self, editor, *_, **__):
        self.focus_button._bg_color = self.focus_button.bg_color = self.focus_button.hover_color = self.refocus_frames[1]
        
        def make_glow():
            self.attr_panel.glow_time = time.time()+0.75
            self.attr_panel.glowing = True
            self.focus_button._bg_color = self.focus_button.bg_color = self.refocus_frames[0]
            self.focus_button.hover_color = self.refocus_frames[1]
            
        targetX = self.attr_panel.x - (((self.canvas.width / self.canvas.scale)-(self.attr_panel.width * self.canvas.scale))/2)
        targetY = self.attr_panel.y - (((self.canvas.height / self.canvas.scale)-(self.attr_panel.height * self.canvas.scale))/2)
    
        self.canvas.setOffset(targetX, targetY, 1, make_glow)
    
    def _update(self, editor, X, Y):
        
        # update
        self.panel._update(editor, X, Y)
        self.label_text_box.x = self.x+12
        self.label_text_box.y = self.y+9
        self.label_text_box._update(editor, 0, 0)
        if self.placer is not None:
            self.placer._update(editor, X+self.placer_offset[0], Y+self.placer_offset[1])
        else:
            self.visibility_button._update(editor, X, Y)
            self.focus_button._update(editor, X, Y)
        
        self.effective_height = self.height
        for child in self.children:
            if hasattr(child, "effective_height"):
                child._update(editor, X, Y+self.effective_height)
                self.effective_height += child.effective_height
            else:
                child._update(editor, X, Y)
                
        
    
    def drop_acceptor(self, _, __):
        self.placer = self._placer
        return True
    
    def _event(self, editor, X, Y):
        self.x = X
        self.y = Y
        # print(f"offsetY: {offsetY}")
        self.effective_height = self.height
        
        
        
        for child in self.children: # Can not reverse-iterate, as positions are constructed iteratively
            if hasattr(child, "effective_height"):
                child._event(editor, X, Y+self.effective_height)
                self.effective_height += child.effective_height
            else:
                child._event(editor, self.x, self.y)

        self.label_text_box.x = self.x+12
        self.label_text_box.y = self.y+9
        self.label_text_box._event(editor, 0, 0)
        
        if self.placer is not None:
            self.placer._event(editor, X+self.placer_offset[0], Y+self.placer_offset[1])
        
        else:
            if editor.drop_requested and editor.held is self._placer:
                editor.accept_drop(0, self.drop_acceptor)
                
            self.focus_button._event(editor, self.x, self.y)
            self.visibility_button._event(editor, self.x, self.y)
            
        self.panel._event(editor, self.x, self.y)
        

