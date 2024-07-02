# pylint: disable=W,R,C,import-error,no-member

from UIElement import UIElement
from Options import PATH, TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR, TEXT_SIZE
from FunctionalElements import Button, BorderedButton
from MultilineText import MultilineText

from Outliner import Outliner
from RenderPrimitives import Image
from AttributePanel import AttributePanel
from Text import Text
from Hyperlink import Hyperlink

from Easing import easeInOutSine, interpolate2D

import pygame
import math
import time


class TutorialPanelPlacer(UIElement):
    
    packaged_panel = (
        Image(f"{PATH}/advanced_editor/panel_crate.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_crate_hovered.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_crate_selected.png", 0, 0, 33, 33),
        Image(f"{PATH}/advanced_editor/panel_crate_selected_hovered.png", 0, 0, 33, 33)
    )
    
    def __init__(self, tutorial):
        self.tutorial = tutorial
        self.width = 33
        self.height = 33
        self.frame = 0
        self.hovered = False
        self._alt_text = "Drag & drop panel on to\nconstruction canvas"
        
    def _event(self, editor, X, Y):
        # print(f"event: {X}, {Y}")
        editor.check_hover(editor, (X, Y, self.width, self.height), self)
        
        if self.hovered:
            self.frame = 1
            if editor.left_mouse_down():
                editor.sound_system.get_audio("AESA_pick_up", "editor").play()
                self.frame = 2
                editor.holding = True
                editor.held = self
                self.tutorial.shelf_placer = None
                self.tutorial.placer_outliner.clear()
                self.tutorial.shelf_panel2.show_buttons = True
                editor.hold_offset = (editor.mouse_pos[0]-X, editor.mouse_pos[1]-Y)
        else:
            self.frame = 0
            self.hovered = False
        
    
    def _update(self, editor, X, Y):
        TutorialPanelPlacer.packaged_panel[self.frame]._update(editor, X, Y)


class TutorialShelfPanel(UIElement):
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
    
    def __init__(self, tutorial, x, y):
        self.x = x
        self.y = y
        width = 340
        height = 35
        
        self.tutorial = tutorial
        self.id_text = Text(12, 2, 1, "tutorial:weapons/example", TEXT_BG3_COLOR, None, 11)
        self.label_text = Text(12, 14, 250, "Example", text_size=TEXT_SIZE+4, text_bg_color=None)

        self.show_buttons = False
        
        self.visibility_button = Button(width-88, (height-33)/2, 33, 33, "", self.visibility_frames[2], hover_color=self.visibility_frames[3], click_color=self.visibility_frames[3])
        self.focus_button = Button(width-54, (height-33)/2, 33, 33, "", self.refocus_frames[0], hover_color=self.refocus_frames[1], click_color=self.refocus_frames[2])

    def _event(self, editor, X, Y):
        if self.show_buttons:
            self.visibility_button._event(editor, X+self.x, Y+self.y)
            self.focus_button._event(editor, X+self.x, Y+self.y)
    
    def _update(self, editor, X, Y):
        if self.show_buttons:
            self.visibility_button._update(editor, X+self.x, Y+self.y)
            self.focus_button._update(editor, X+self.x, Y+self.y)
        self.id_text._update(editor, X+self.x, Y+self.y)
        self.label_text._update(editor, X+self.x, Y+self.y)

class EditorTutorial(UIElement):
    def __init__(self, aesa):
        self.aesa = aesa
        self.pages = {}
        self.masks = {}
        self.openers = {}
        self.background_objects = {}
    
        self.mask_opacity = 200
    
        self.page = 0
        self.x = aesa.x
        self.y = aesa.y
        
        self.animation = 0
        self.animation_state = 0
        self.animation_target = 0
        
        self.width = aesa.width
        self.height = aesa.height
        
        ### PAGE 0 ###
        p0_intro_text = MultilineText(self.aesa.x+70, self.aesa.y+30, 1, 1, "Welcome to the\nDungeon Editor!", text_size=40, text_bg_color=None)
        
        p0_text1 = MultilineText(self.aesa.x+70, p0_intro_text.y+p0_intro_text.height+30, 1, 1, "This tutorial will show you how to use the editor.\nIf you already know how to use the editor, you can skip this tutorial.\n\nIf you find part of this tutorial to be confusing,\nyou can create an issue on the Github     .\n\n\nPress Next to continue.", text_size=20, text_bg_color=None)
        
        p0_github_link = Hyperlink(self.aesa.x+526, p0_intro_text.y+p0_intro_text.height+122, 1, 1, "here", "https://github.com/Westbot657/DungeonEngine/issues", text_size=20, text_bg_color=None)
        
        self.pages.update({0: [p0_intro_text, p0_text1, p0_github_link]})
    
        ### PAGE 1 ### Opening a dungeon project
        p1_title_text = MultilineText(self.aesa.x+70, self.aesa.y+30, 1, 1, "Opening a dungeon", text_size=40, text_bg_color=None)
        
        p1_text1 = MultilineText(self.aesa.x+70, p1_title_text.y+p1_title_text.height+30, 1, 1, "To open an existing project, press the Open Dungeon button in the bottom left corner.\nOutside the tutorial, this button will open a folder selection prompt.\n\nTo create a new project, click the Create Dungeon button.\n\n\nPress Next to continue.", text_size=20, text_bg_color=None)
        
        self.p1_open_button_outliner = Outliner(self.aesa.open_dungeon_button.x - 6, self.aesa.open_dungeon_button.y-6, self.aesa.open_dungeon_button.width + 10, self.aesa.open_dungeon_button.height + 10, color=(255, 127, 39), thickness=2, direction=1, animation_time=1, start_angle=90)
        self.p1_fake_open_button = BorderedButton(self.aesa.open_dungeon_button.x, self.aesa.open_dungeon_button.y, -1, None, "    Open Dungeon    ")
        
        self.p1_create_button_outliner = Outliner(self.aesa.create_dungeon_button.x-6, self.aesa.create_dungeon_button.y-6, self.aesa.create_dungeon_button.width + 10, self.aesa.create_dungeon_button.height + 10, color=(255, 127, 39), thickness=2, direction=1, animation_time=1, start_angle=90)
        self.p1_fake_create_button = BorderedButton(self.aesa.create_dungeon_button.x, self.aesa.create_dungeon_button.y, -1, None, "    Create Dungeon    ")
        
        self.pages.update({1: [p1_title_text, p1_text1, self.p1_open_button_outliner, self.p1_fake_open_button, self.p1_create_button_outliner, self.p1_fake_create_button]})
        
        ### PAGE 2 ###
        self.p2_title_text = MultilineText(self.aesa.x+70, self.aesa.y+30, 1, 1, "Editing an object", text_size=40, text_bg_color=None)
        
        self.p2_text1 = MultilineText(self.aesa.x+70, self.p2_title_text.y+self.p2_title_text.height+30, 1, 1, "", text_size=20, text_bg_color=None)
        self.p2_text1.set_colored_content("To edit an object,\ndrag it from the \033[38;2;255;127;39mshelf\033[0m to the \033[38;2;255;255;28mconstruction canvas\033[0m.")
        
        self.p2_canvas_outliner = Outliner(0, 0, 0, 0, color=(255, 255, 28), thickness=2, direction=1, animation_time=1.5, start_angle=90)
        
        self.p2_shelf_outliner = Outliner(0, 0, 0, 0, color=(255, 127, 39), thickness=2, direction=1, animation_time=1.5, start_angle=90, animation_delay=0.5)
        self.shelf_panel = Image(f"{PATH}/advanced_editor/tutorial_shelf_panel.png", self.aesa.object_tree.x+10, self.aesa.object_tree.y+5, 320, 35)
        
        self.placer_pos = (self.shelf_panel.x+284, self.shelf_panel.y+1)
        self.placer = self.shelf_placer = TutorialPanelPlacer(self)
        self.shelf_panel2 = TutorialShelfPanel(self, self.aesa.object_tree.x+10, self.aesa.object_tree.y+5)
        self.panel_showing = False
        self.canvas_panel = AttributePanel(self.aesa.editor, None, self.x+280, self.y+190, 300, 400, True)
        
        self.placer_outliner = Outliner(self.shelf_panel.x+278, self.shelf_panel.y-5, 43, 43, color=(50, 200, 50), thickness=2, direction=1, animation_time=1, start_angle=90, animation_delay=1.5)
        
        self.masks.update({2: self.page2_mask_draw})
        self.pages.update({2: [self.p2_title_text, self.p2_text1, self.p2_canvas_outliner, self.p2_shelf_outliner, self.shelf_panel, self.shelf_panel2, self.placer_outliner]})
        
        ### PAGE 3 ###
        
        self.p3_collapse_y = self.p3_collapse_y_start = self.aesa.object_tree.y-6
        self.p3_collapse_y_height = self.aesa.object_tree.height+12
        self.p3_collapse_x = self.aesa.object_tree.x-1
        self.p3_animation_surface = pygame.Surface((self.aesa.editor.width, self.aesa.editor.height), pygame.SRCALPHA, 32)
        self.p3_animation_surface.set_alpha(self.mask_opacity)
        self.p3_fade = 0
        
        self.p3_title_text = MultilineText(self.aesa.x+70, self.aesa.y+30, 1, 1, "Canvas Navigation", text_size=40, text_bg_color=None)
        
        # max text width is 39 characters
        self.p3_info_text = MultilineText(self.aesa.x+self.aesa.width-350, self.p3_title_text.y+self.p3_title_text.height+120, 1, 1, "- Middle mouse button: Pan\n- Scroll wheel: Zoom in/out\n- R-click: Open context menu\n- L-click the edge of a\n  panel to drag it around or\n  move it back to the shelf\n\n(controls are disabled in\nthe tutorial)\n\n\nPress Next to continue.", text_size=20, text_bg_color=None)
        
        self.masks.update({3: self.page2_mask_draw})
        self.background_objects.update({3: [self.shelf_panel2], 4: [self.shelf_panel2]})
        self.pages.update({3: [self.canvas_panel, self.p3_title_text, self.p3_info_text, self.p2_canvas_outliner]})
        
        
        ### PAGE 4 ###
        self.p4_title_text = MultilineText(self.aesa.x+70, self.aesa.y+30, 1, 1, "Object Properties", text_size=40, text_bg_color=None)
        
        self.panel_rect = (105, 195, 290, 390)
        self.outline_rect = (95, 185, 310, 410)
        self.current_rect = [0, 0, 0, 0]
        self.panel_pos = (0, 0)
        self.panel_current = (0, 0)
        
        self.infill_rect = [0, 0, 0, 0]
        self.p4_animation_surface = pygame.Surface((self.aesa.editor.width, self.aesa.editor.height), pygame.SRCALPHA, 32)
        self.p4_animation_surface.set_alpha(self.mask_opacity)
        
        self.p4_info_text1 = MultilineText(415+self.x, 197+self.y, 1, 1, "- \033[38;2;200;60;39mObject ID\033[0m", text_size=20, text_bg_color=None)
        self.p4_info_text2 = MultilineText(415+self.x, 227+self.y, 1, 1, "- \033[38;2;255;127;39mObject Label\033[0m", text_size=20, text_bg_color=None)
        self.p4_info_text3 = MultilineText(415+self.x, 257+self.y, 1, 1, "- \033[38;2;100;220;40mObject Attributes\033[0m", text_size=20, text_bg_color=None)
        
        self.p4_panel_id = MultilineText(self.panel_rect[0]+10+self.x, self.panel_rect[1]+1+self.y, 1, 1, "tutorial:weapons/example", text_bg_color=None, text_size=15)
        self.p4_panel_label = MultilineText(self.panel_rect[0]+10+self.x, self.panel_rect[1]+30+self.y, 280, 25, "Example", text_bg_color=None, text_size=20)
        
        self.p4_panel_id_outliner = Outliner(self.panel_rect[0]-6+self.x, self.p4_panel_id.y-5, self.panel_rect[2]+11, self.p4_panel_id.height+10, (200, 60, 39), thickness=2)
        self.p4_panel_label_outliner = Outliner(self.panel_rect[0]-6+self.x, self.p4_panel_label.y-5, self.panel_rect[2]+11, self.p4_panel_label.height+10, (255, 127, 39), animation_delay=0.25, thickness=2)
        self.p4_panel_attributes_outliner = Outliner(self.panel_rect[0]-6+self.x, self.p4_panel_label.y+32, self.panel_rect[2]+11, 330, (100, 220, 40), animation_delay=0.5, thickness=2)
        
        
        self.masks.update({4: self.page4_mask_draw})
        self.pages.update({4: [self.p4_title_text, self.p4_info_text1, self.p4_info_text2, self.p4_info_text3, self.p4_panel_id, self.p4_panel_label, self.p4_panel_id_outliner, self.p4_panel_label_outliner, self.p4_panel_attributes_outliner]})
        ### General ###
        
        self.mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.mask.fill((0, 0, 0, self.mask_opacity))
        
        self.next_button = BorderedButton(0, aesa.editor.height-50, -1, 20, "  Next >  ", bg_color=TEXT_BG2_COLOR, hover_color=TEXT_BG3_COLOR, click_color=TEXT_BG2_COLOR, border_color=TEXT_BG3_COLOR)
        self.next_button.on_left_click = self.next_button_event
    
        self.back_button = BorderedButton(0, aesa.editor.height-50, -1, 20, "  < Back  ", bg_color=TEXT_BG2_COLOR, hover_color=TEXT_BG3_COLOR, click_color=TEXT_BG2_COLOR, border_color=TEXT_BG3_COLOR)
        self.back_button.on_left_click = self.back_button_event
    
        self.next_button.x = aesa.editor.width - (self.next_button.width + 15)
        
        self.skip_button = BorderedButton(0, aesa.editor.height-75, self.next_button.width + self.back_button.width + 10, 20, "    Skip Tutorial  ", bg_color=TEXT_BG2_COLOR, hover_color=TEXT_BG3_COLOR, click_color=TEXT_BG2_COLOR, border_color=TEXT_BG3_COLOR)
        self.skip_button.on_left_click = self.skip_button_event
        
        self.back_button.x = self.skip_button.x = self.next_button.x - (self.back_button.width + 10)
    
        self.openers.update({0: self.open0, 1: self.open1, 2: self.open2, 3: self.open3, 4: self.open4})
    
    
    ### PAGE 0 ###
    def open0(self):
        pass
    
    
    ### PAGE 1 ###
    def open1(self):
        self.p1_open_button_outliner.start_animation()
        self.p1_create_button_outliner.start_animation(0.25)
    
    ### PAGE 2 ###
    def open2(self):
        self.animation = 0
        self.p2_canvas_outliner.start_animation()
        self.p2_shelf_outliner.start_animation()
        self.placer_outliner.start_animation()
        self.shelf_placer = self.placer
        self.panel_showing = False
        self.shelf_panel2.show_buttons = False
        
        self.p2_title_text.surface.set_alpha(255)
        self.p2_text1.surface.set_alpha(255)
    
    def page2_mask_draw(self):
        self.mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        pygame.draw.polygon(self.mask, (0, 0, 0, self.mask_opacity), [
            (0, 0),
            (self.width, 0),
            (self.width, self.aesa.object_tree.y - self.y),
            (self.aesa.object_tree.x - self.x + 5, self.aesa.object_tree.y - self.y),
            (self.aesa.object_tree.x - self.x + 5, self.aesa.object_tree.y + self.aesa.object_tree.height - self.y),
            (self.aesa.object_tree.x + self.aesa.object_tree.width - self.x - 15, self.aesa.object_tree.y + self.aesa.object_tree.height - self.y),
            (self.aesa.object_tree.x + self.aesa.object_tree.width - self.x - 15, self.aesa.object_tree.y - self.y),
            (self.width, self.aesa.object_tree.y - self.y),
            (self.width, self.height),
            (0, self.height),
            (0, self.aesa.construction_canvas.y - self.y + 180),
            (self.aesa.construction_canvas.x - self.x + 20, self.aesa.construction_canvas.y - self.y + 180),
            (self.aesa.construction_canvas.x - self.x + 20, self.aesa.construction_canvas.y + self.aesa.construction_canvas.height - self.y - 15),
            (self.aesa.construction_canvas.x + self.aesa.construction_canvas.width - self.x - 20, self.aesa.construction_canvas.y + self.aesa.construction_canvas.height - self.y - 15),
            (self.aesa.construction_canvas.x + self.aesa.construction_canvas.width - self.x - 20, self.aesa.construction_canvas.y - self.y + 180),
            (0, self.aesa.construction_canvas.y - self.y + 180),
            (0, 0)
        ])
    
    def page4_mask_draw(self):
        self.mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        if self.animation and self.state == 0:
            pygame.draw.polygon(self.mask, (0, 0, 0, self.mask_opacity), [
                (0, 0),
                (self.width, 0),
                (self.width, self.height),
                (0, self.height),
                (0, self.aesa.construction_canvas.y - self.y + 180),
                (self.aesa.construction_canvas.x - self.x + 20, self.aesa.construction_canvas.y - self.y + 180),
                (self.aesa.construction_canvas.x - self.x + 20, self.aesa.construction_canvas.y + self.aesa.construction_canvas.height - self.y - 15),
                (self.aesa.construction_canvas.x + self.aesa.construction_canvas.width - self.x - 20, self.aesa.construction_canvas.y + self.aesa.construction_canvas.height - self.y - 15),
                (self.aesa.construction_canvas.x + self.aesa.construction_canvas.width - self.x - 20, self.aesa.construction_canvas.y - self.y + 180),
                (0, self.aesa.construction_canvas.y - self.y + 180),
                (0, 0)
            ])
        else:
            if self.state == 1:
                self.state = 2
                self.animation = time.time()
            self.mask.fill((0, 0, 0, self.mask_opacity))
    
    def p2_canvas_acceptor(self, obj, editor):
        self.panel_showing = True
        editor.sound_system.get_audio("AESA_thud", "editor").play()
        self.animation = time.time()
    
    def p2_default_acceptor(self, obj, editor):
        self.shelf_placer = obj
        editor.sound_system.get_audio("AESA_drop", "editor").play()
        self.placer_outliner.start_animation(-self.placer_outliner.animation_delay)
        self.shelf_panel2.show_buttons = False
    
    ### PAGE 3 ###
    def open3(self):
        # print("OPENING PAGE 3")
        self.animation = time.time()
        self.p3_info_text.surface.set_alpha(0)
        self.p3_title_text.surface.set_alpha(0)

    ### PAGE 4 ###
    def open4(self):
        self.animation = time.time()
        self.state = 0
        self.p4_info_text1.surface.set_alpha(0)
        self.p4_panel_id.surface.set_alpha(0)
        self.p4_info_text2.surface.set_alpha(0)
        self.p4_panel_label.surface.set_alpha(0)
        self.p4_info_text3.surface.set_alpha(0)
        
        self.p4_panel_id_outliner.clear()
        self.p4_panel_label_outliner.clear()
        self.p4_panel_attributes_outliner.clear()
        
        self.p2_canvas_outliner.x = self.p4_

    ### General ###
    
    def skip_button_event(self, *_, **__):
        self.aesa.seen_tutorial = True
        self.aesa.code_editor.settings_app.seen_tutorial_toggle.set_state(True)
        self.aesa.code_editor.settings_app.save_component_values()
        self.aesa.code_editor.settings_app.save_config()
        self.page = 0
        self.aesa.search_box.set_content("")
    
    def back_button_event(self, editor, *_, **__):
        if self.page > 0:
            self.page -= 1
            self.openers.get(self.page, self.open0)()
            self._event(editor, 0, 0)
            self._update_layout(editor)
            self._update(editor, 0, 0)
    
    def next_button_event(self, editor, *_, **__):
        if self.page < len(self.pages) - 1:
            self.page += 1
            self.openers.get(self.page, self.open0)()
            self._event(editor, 0, 0)
            self._update_layout(editor)
            self._update(editor, 0, 0)
            
    
    def plain_mask_draw(self):
        self.mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.mask.fill((0, 0, 0, self.mask_opacity))
    

    
    def _update_layout(self, editor):
        if editor._do_layout_update:
            self.width = self.aesa.width
            self.height = self.aesa.height
            self.next_button.x = editor.width - (self.next_button.width + 15)
            self.back_button.x = self.skip_button.x = self.next_button.x - (self.back_button.width + 10)
            self.back_button.y = editor.height-50
            self.next_button.y = editor.height-50
            self.skip_button.y = editor.height-75
            
            self.mask = pygame.Surface((self.width, self.height))
            self.masks.get(self.page, self.plain_mask_draw)()
            self.aesa.search_box.set_content("search...                                           random text so no actual results appear")
            
            match self.page:
                case 1:
                    self.p1_open_button_outliner.y = self.aesa.open_dungeon_button.y - 6
                    self.p1_create_button_outliner.y = self.aesa.create_dungeon_button.y - 6
                    
                    self.p1_fake_open_button.y = self.aesa.open_dungeon_button.y
                    self.p1_fake_create_button.y = self.aesa.create_dungeon_button.y
                case 2|3:
                    self.p2_canvas_outliner.x = self.aesa.construction_canvas.x + 20 - 6
                    self.p2_canvas_outliner.y = self.aesa.construction_canvas.y + 180 - 6
                    self.p2_canvas_outliner.resize(self.aesa.construction_canvas.width - 40 + 12, self.aesa.construction_canvas.height - 15 - 180 + 12)
                    
                    if self.page == 2:
                        self.p2_shelf_outliner.x = self.aesa.object_tree.x - 1
                        self.p2_shelf_outliner.y = self.aesa.object_tree.y - 6
                        self.p2_shelf_outliner.resize(self.aesa.object_tree.width - 8, self.aesa.object_tree.height + 12)
                        self.placer_outliner.x = self.shelf_panel.x+278
                        self.placer_outliner.y = self.shelf_panel.y-5
                    else:
                        self.p3_collapse_y = self.p3_collapse_y_start = self.aesa.object_tree.y-6
                        self.p3_collapse_y_height = self.aesa.object_tree.height+12
                        self.p3_collapse_x = self.aesa.object_tree.x-1
                        
                        self.p3_animation_surface = pygame.Surface((self.aesa.editor.width, self.aesa.editor.height), pygame.SRCALPHA, 32)
                        self.p3_animation_surface.set_alpha(self.mask_opacity)
                        
                        self.p3_info_text.x = self.aesa.x+self.aesa.width-350
                    
                    self.shelf_panel.x = self.aesa.object_tree.x+10
                    self.shelf_panel.y = self.aesa.object_tree.y+5
                    self.placer_pos = (self.shelf_panel.x+284, self.shelf_panel.y+1)
                    
                    self.shelf_panel2.x = self.aesa.object_tree.x+10
                    self.shelf_panel2.y = self.aesa.object_tree.y+5
                    
                    self.canvas_panel.x = self.aesa.construction_canvas.x + (self.aesa.construction_canvas.width - 300) // 2
                    self.canvas_panel.y = self.aesa.construction_canvas.y + 170 + ((self.aesa.construction_canvas.height - 170) - 400) // 2
                case 4:
                    
                    self.p4_animation_surface = pygame.Surface((self.aesa.editor.width, self.aesa.editor.height), pygame.SRCALPHA, 32)
                    self.canvas_panel.x = self.canvas_panel.y = 0
                    self.panel_pos = (
                        self.aesa.construction_canvas.x + (self.aesa.construction_canvas.width - 300) // 2,
                        self.aesa.construction_canvas.y + 170 + ((self.aesa.construction_canvas.height - 170) - 400) // 2
                    )

    def _event(self, editor, X, Y):
        self.back_button._event(editor, X, Y)
        self.next_button._event(editor, X, Y)
        self.skip_button._event(editor, X, Y)
    
        for child in self.pages.get(self.page, [])[::-1]:
            child._event(editor, X, Y)
    
        if self.page == 2:
            if self.shelf_placer:
                self.shelf_placer._event(editor, X+self.placer_pos[0], Y+self.placer_pos[1])
            
            if editor.drop_requested:
                canvas_collision = editor.collides(editor.mouse_pos, (self.aesa.construction_canvas.x, self.aesa.construction_canvas.y, self.aesa.construction_canvas.width, self.aesa.construction_canvas.height))
    
                if isinstance(editor.held, TutorialPanelPlacer) and canvas_collision:
                    editor.accept_drop(0, self.p2_canvas_acceptor)
    
                elif isinstance(editor.held, TutorialPanelPlacer):
                    editor.accept_drop(0, self.p2_default_acceptor)
            
            if self.animation:
                dt = (time.time() - self.animation) / 0.75
                if dt > 1:
                    self.animation = 0
                    self.page = 3
                    self.open3()
                    self._event(editor, 0, 0)
                    self._update_layout(editor)
                    self._update(editor, 0, 0)
                self.p2_title_text.surface.set_alpha(255 * (1-easeInOutSine(dt)))
                self.p2_text1.surface.set_alpha(255 * (1-easeInOutSine(dt)))
            
        elif self.page == 3:
            if self.animation and self.animation_state == 0:
                dt = (time.time() - self.animation) / 1.5
                dt2 = (time.time() - self.animation) / 0.75
                if dt2 > 1:
                    dt2 = 1
                if dt > 1:
                    dt = 1
                    self.animation_state = 1
                    self.animation = time.time()
                self.p3_title_text.surface.set_alpha(255 * easeInOutSine(dt2))
                self.p3_collapse_y = self.p3_collapse_y_start + (self.p3_collapse_y_height * easeInOutSine(dt))
            elif self.animation and self.animation_state == 1:
                dt = (time.time() - self.animation) / 0.75
                if dt > 1:
                    dt = 1
                    self.animation = 0
                    self.animation_state = 0
                self.p3_info_text.surface.set_alpha(255 * easeInOutSine(dt))
        elif self.page == 4:
            self.p2_canvas_outliner._event(editor, X, Y)
            if self.animation:
                if self.state == 0:
                    dt = (time.time() - self.animation) / 1.5
                    if dt > 1:
                        dt = 1
                        self.animation = 0
                        self.state = 1
                        self.p2_canvas_outliner.animation_time = 0.0001
                        self.p2_canvas_outliner.start_animation()
                    dt = easeInOutSine(dt)
                    # (self.aesa.construction_canvas.x - self.x + 20, self.aesa.construction_canvas.y - self.y + 180),
                    # (self.aesa.construction_canvas.x - self.x + 20, self.aesa.construction_canvas.y + self.aesa.construction_canvas.height - self.y - 15),
                    # (self.aesa.construction_canvas.x + self.aesa.construction_canvas.width - self.x - 20, self.aesa.construction_canvas.y + self.aesa.construction_canvas.height - self.y - 15),
                    # (self.aesa.construction_canvas.x + self.aesa.construction_canvas.width - self.x - 20, self.aesa.construction_canvas.y - self.y + 180),
        
                    top_left = (self.aesa.construction_canvas.x - self.x + 21, self.aesa.construction_canvas.y - self.y + 181)
                    bottom_left = (self.aesa.construction_canvas.x - self.x + 21, self.aesa.construction_canvas.y + self.aesa.construction_canvas.height - self.y - 16)
                    bottom_right = (self.aesa.construction_canvas.x + self.aesa.construction_canvas.width - self.x - 21, self.aesa.construction_canvas.y + self.aesa.construction_canvas.height - self.y - 16)
                    top_right = (self.aesa.construction_canvas.x + self.aesa.construction_canvas.width - self.x - 21, self.aesa.construction_canvas.y - self.y + 181)
                    
                    self.infill_rect = [*top_left, (top_right[0] - top_left[0]), (bottom_right[1] - top_right[1])]
                    
                    self.panel_current = interpolate2D(self.panel_pos, (self.panel_rect[0]-5+self.x, self.panel_rect[1]-5+self.y), dt)
                    
                    top_left = interpolate2D(top_left, (self.panel_rect[0], self.panel_rect[1]), dt)
                    top_right = interpolate2D(top_right, (self.panel_rect[0] + self.panel_rect[2], self.panel_rect[1]), dt)
                    bottom_right = interpolate2D(bottom_right, (self.panel_rect[0] + self.panel_rect[2], self.panel_rect[1] + self.panel_rect[3]), dt)
                    bottom_left = interpolate2D(bottom_left, (self.panel_rect[0], self.panel_rect[1] + self.panel_rect[3]), dt)
                    
                    self.current_rect = [*top_left, (top_right[0] - top_left[0]), (bottom_right[1] - top_right[1])]
                elif self.state == 1:
                    self.state = 2
                    self.animation = time.time()
                elif self.state == 2:
                    dt = (time.time() - self.animation) / 1.5
                    dt1 = min(max(0, dt/0.75), 1)
                    dt2 = min(max(0, (dt-0.25)/0.75), 1)
                    dt3 = min(max(0, (dt-0.5)/0.75), 1)
                    
                    if dt > 1.5:
                        dt = 1
                        self.animation = 0
                        self.state = 0
                    if dt <= 0.1 and not self.p4_panel_id_outliner.start_time:
                        self.p4_panel_id_outliner.start_animation()
                        self.p4_panel_label_outliner.start_animation()
                        self.p4_panel_attributes_outliner.start_animation()
                        self.p2_canvas_outliner.animate_out(-self.p2_canvas_outliner.animation_delay)
                        
                    dt = min(dt, 1)
                    self.p4_info_text1.surface.set_alpha(255 * easeInOutSine(dt1))
                    self.p4_panel_id.surface.set_alpha(255 * easeInOutSine(dt1))
                    self.p4_info_text2.surface.set_alpha(255 * easeInOutSine(dt2))
                    self.p4_panel_label.surface.set_alpha(255 * easeInOutSine(dt2))
                    self.p4_info_text3.surface.set_alpha(255 * easeInOutSine(dt3))
    
        if not editor._hovered:
            mx, my = editor.mouse_pos
            _x = mx-self.aesa.x
            _y = my-self.aesa.y
            if 0 <= _x < self.width and 0 <= _y < self.height:
                if self.page in []:
                    if self.mask.get_at((_x, _y)) == (0, 0, 0, self.mask_opacity):
                        editor._hovered = True
                        editor._hovering = self
                else:
                    editor._hovered = True
                    editor._hovering = self
    
    def _update(self, editor, X, Y):
        
        
        for child in self.background_objects.get(self.page, []):
            child._update(editor, X, Y)
        
        editor.screen.blit(self.mask, (self.aesa.x, self.aesa.y))
        
        if self.page == 3:
            # print(self.animation)
            if self.animation and self.animation_state == 0:
                pygame.draw.polygon(self.p3_animation_surface, (0, 0, 0), [
                    (self.p3_collapse_x+7, min(self.p3_collapse_y+7, self.p3_collapse_y_start + self.p3_collapse_y_height-7)),
                    (self.p3_collapse_x-7 + self.aesa.object_tree.width - 8, min(self.p3_collapse_y+7, self.p3_collapse_y_start + self.p3_collapse_y_height-7)),
                    (self.p3_collapse_x-7 + self.aesa.object_tree.width - 8, self.p3_collapse_y_start+7),
                    (self.p3_collapse_x+7, self.p3_collapse_y_start+7)
                ])
                editor.screen.blit(self.p3_animation_surface, (0, 0))
                pygame.draw.polygon(editor.screen, (255, 127, 39), [
                    (self.p3_collapse_x, self.p3_collapse_y),
                    (self.p3_collapse_x + self.aesa.object_tree.width - 8, self.p3_collapse_y),
                    (self.p3_collapse_x + self.aesa.object_tree.width - 8, self.p3_collapse_y_start + self.p3_collapse_y_height),
                    (self.p3_collapse_x, self.p3_collapse_y_start + self.p3_collapse_y_height)
                ], 2)
            else:
                self.p3_animation_surface.fill((0, 0, 0), (self.p3_collapse_x+7, self.p3_collapse_y_start+7, self.aesa.object_tree.width - 8-13, self.p3_collapse_y_height-13))
                editor.screen.blit(self.p3_animation_surface, (0, 0))
        elif self.page == 4:
            if (self.animation and self.state == 0) or self.state == 1:
                self.p4_animation_surface.fill((0, 0, 0, 0))
                pygame.draw.polygon(self.p4_animation_surface, (0, 0, 0), [
                    (self.infill_rect[0], self.infill_rect[1]),
                    (self.infill_rect[0] + self.infill_rect[2], self.infill_rect[1]),
                    (self.infill_rect[0] + self.infill_rect[2], self.infill_rect[1] + self.infill_rect[3]),
                    (self.infill_rect[0], self.infill_rect[1] + self.infill_rect[3]),
                    (self.infill_rect[0], self.infill_rect[1]),
                    (self.current_rect[0], self.current_rect[1]),
                    (self.current_rect[0], self.current_rect[1] + self.current_rect[3]),
                    (self.current_rect[0] + self.current_rect[2], self.current_rect[1] + self.current_rect[3]),
                    (self.current_rect[0] + self.current_rect[2], self.current_rect[1]),
                    (self.current_rect[0], self.current_rect[1])
                ])
                self.p4_animation_surface.set_alpha(self.mask_opacity)
                editor.screen.blit(self.p4_animation_surface, (self.aesa.x, self.aesa.y))
            
                pygame.draw.lines(editor.screen, (255, 255, 28), True, [
                    (min(self.current_rect[0]-6, self.panel_rect[0]-11) + self.aesa.x, min(self.current_rect[1]-6, self.panel_rect[1]-11) + self.aesa.y),
                    (max(self.current_rect[0]+self.current_rect[2]+5, self.panel_rect[0]+self.panel_rect[2]+10) + self.aesa.x, min(self.current_rect[1]-6, self.panel_rect[1]-11) + self.aesa.y),
                    (max(self.current_rect[0]+self.current_rect[2]+5, self.panel_rect[0]+self.panel_rect[2]+10) + self.aesa.x, max(self.current_rect[1]+self.current_rect[3]+5, self.panel_rect[1]+self.panel_rect[3]+10) + self.aesa.y),
                    (min(self.current_rect[0]-6, self.panel_rect[0]-11) + self.aesa.x, max(self.current_rect[1]+self.current_rect[3]+5, self.panel_rect[1]+self.panel_rect[3]+10) + self.aesa.y)
                ], 2)
            else:
                self.p2_canvas_outliner._update(editor, X, Y)
            
            self.canvas_panel._update(editor, X+self.panel_current[0], Y+self.panel_current[1])
        
        
        for child in self.pages.get(self.page, []):
            child._update(editor, X, Y)
        
        if self.page == 2:
            if self.panel_showing:
                self.canvas_panel._update(editor, X, Y)
            if self.shelf_placer:
                self.shelf_placer._update(editor, X+self.placer_pos[0], Y+self.placer_pos[1])

            
        self.back_button._update(editor, X, Y)
        self.next_button._update(editor, X, Y)
        self.skip_button._update(editor, X, Y)
        
    