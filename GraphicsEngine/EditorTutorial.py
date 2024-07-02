# pylint: disable=W,R,C,import-error,no-member

from UIElement import UIElement
from Options import PATH, TEXT_COLOR, TEXT_BG_COLOR, TEXT_BG2_COLOR, TEXT_BG3_COLOR
from FunctionalElements import Button, BorderedButton
from MultilineText import MultilineText

from Outliner import Outliner
from RenderPrimitives import Image
from AttributePanel import AttributePanel

from Hyperlink import Hyperlink

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
                editor.hold_offset = (editor.mouse_pos[0]-X, editor.mouse_pos[1]-Y)
        else:
            self.frame = 0
            self.hovered = False
        
    
    def _update(self, editor, X, Y):
        TutorialPanelPlacer.packaged_panel[self.frame]._update(editor, X, Y)


class EditorTutorial(UIElement):
    def __init__(self, aesa):
        self.aesa = aesa
        self.pages = {}
        self.masks = {}
        self.openers = {}
    
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
        
        p0_text1 = MultilineText(self.aesa.x+70, p0_intro_text.y+p0_intro_text.height+30, 1, 1, "This tutorial will show you how to use the editor.\nIf you already know how to use the editor, you can skip this tutorial.\n\nIf you find part of this tutorial confusing,\nyou can create an issue on the Github     .\n\nPress Next to continue.", text_size=20, text_bg_color=None)
        
        p0_github_link = Hyperlink(self.aesa.x+526, p0_intro_text.y+p0_intro_text.height+122, 1, 1, "here", "https://github.com/Westbot657/DungeonEngine/issues", text_size=20, text_bg_color=None)
        
        self.pages.update({0: [p0_intro_text, p0_text1, p0_github_link]})
    
        ### PAGE 1 ### Opening a dungeon project
        p1_title_text = MultilineText(self.aesa.x+70, self.aesa.y+30, 1, 1, "Opening a dungeon", text_size=40, text_bg_color=None)
        
        p1_text1 = MultilineText(self.aesa.x+70, p1_title_text.y+p1_title_text.height+30, 1, 1, "To open an existing project, press the Open Dungeon button in the bottom left corner.\nOutside the tutorial, this button will open a folder selection prompt.\n\nTo create a new project, click the Create Dungeon button.\n\nPress Next to continue.", text_size=20, text_bg_color=None)
        
        self.p1_open_button_outliner = Outliner(self.aesa.open_dungeon_button.x - 6, self.aesa.open_dungeon_button.y-6, self.aesa.open_dungeon_button.width + 10, self.aesa.open_dungeon_button.height + 10, color=(255, 127, 39), thickness=2, direction=1, animation_time=1, start_angle=90)
        self.p1_fake_open_button = BorderedButton(self.aesa.open_dungeon_button.x, self.aesa.open_dungeon_button.y, -1, None, "    Open Dungeon    ")
        
        self.p1_create_button_outliner = Outliner(self.aesa.create_dungeon_button.x-6, self.aesa.create_dungeon_button.y-6, self.aesa.create_dungeon_button.width + 10, self.aesa.create_dungeon_button.height + 10, color=(255, 127, 39), thickness=2, direction=1, animation_time=1, start_angle=90)
        self.p1_fake_create_button = BorderedButton(self.aesa.create_dungeon_button.x, self.aesa.create_dungeon_button.y, -1, None, "    Create Dungeon    ")
        
        self.pages.update({1: [p1_title_text, p1_text1, self.p1_open_button_outliner, self.p1_fake_open_button, self.p1_create_button_outliner, self.p1_fake_create_button]})
        
        ### PAGE 2 ###
        p2_title_text = MultilineText(self.aesa.x+70, self.aesa.y+30, 1, 1, "Editing an object", text_size=40, text_bg_color=None)
        
        p2_text1 = MultilineText(self.aesa.x+70, p2_title_text.y+p2_title_text.height+30, 1, 1, "", text_size=20, text_bg_color=None)
        p2_text1.set_colored_content("To edit an object,\ndrag it from the \033[38;2;255;127;39mshelf\033[0m to the \033[38;2;255;255;28mconstruction canvas\033[0m.")
        
        self.p2_canvas_outliner = Outliner(0, 0, 0, 0, color=(255, 255, 28), thickness=2, direction=1, animation_time=2, start_angle=90)
        
        self.p2_shelf_outliner = Outliner(0, 0, 0, 0, color=(255, 127, 39), thickness=2, direction=1, animation_time=2, start_angle=90, animation_delay=0.5)
        self.shelf_panel = Image(f"{PATH}/advanced_editor/tutorial_shelf_panel.png", self.aesa.object_tree.x+10, self.aesa.object_tree.y+5, 320, 35)
        
        self.placer_pos = (self.shelf_panel.x+284, self.shelf_panel.y+1)
        self.placer = self.shelf_placer = TutorialPanelPlacer(self)
        self.panel_showing = False
        self.canvas_panel = AttributePanel(self.aesa.editor, None, self.x+280, self.y+190, 300, 400, True)
        
        self.masks.update({2: self.page2_mask_draw})
        self.pages.update({2: [p2_title_text, p2_text1, self.p2_canvas_outliner, self.p2_shelf_outliner, self.shelf_panel]})
        
        ### PAGE 3 ###
        
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
    
        self.openers.update({0: self.open0, 1: self.open1, 2: self.open2, 3: self.open3})
    
    
    ### PAGE 0 ###
    def open0(self):
        pass
    
    
    ### PAGE 1 ###
    def open1(self):
        self.p1_open_button_outliner.start_animation()
        self.p1_create_button_outliner.start_animation(0.25)
    
    ### PAGE 2 ###
    def open2(self):
        self.p2_canvas_outliner.start_animation()
        self.p2_shelf_outliner.start_animation()
        self.shelf_placer = self.placer
        self.panel_showing = False
    
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
    
    def p2_canvas_acceptor(self, obj, editor):
        self.panel_showing = True
        editor.sound_system.get_audio("AESA_thud", "editor").play()
    
    def p2_default_acceptor(self, obj, editor):
        self.shelf_placer = obj
        editor.sound_system.get_audio("AESA_drop", "editor").play()
    
    ### PAGE 3 ###
    def open3(self):
        ...


    ### General ###
    
    def skip_button_event(self, *_, **__):
        self.aesa.seen_tutorial = True
        self.aesa.code_editor.settings_app.seen_tutorial_toggle.set_state(True)
        self.aesa.code_editor.settings_app.save_component_values()
        self.aesa.code_editor.settings_app.save_config()
        self.page = 0
    
    def back_button_event(self, *_, **__):
        if self.page > 0:
            self.page -= 1
            self.openers.get(self.page, self.open0)()
    
    def next_button_event(self, *_, **__):
        if self.page < len(self.pages) - 1:
            self.page += 1
            self.openers.get(self.page, self.open0)()
            
    
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
            
            match self.page:
                case 1:
                    self.p1_open_button_outliner.y = self.aesa.open_dungeon_button.y - 6
                    self.p1_create_button_outliner.y = self.aesa.create_dungeon_button.y - 6
                    
                    self.p1_fake_open_button.y = self.aesa.open_dungeon_button.y
                    self.p1_fake_create_button.y = self.aesa.create_dungeon_button.y
                case 2:
                    self.p2_canvas_outliner.x = self.aesa.construction_canvas.x + 20 - 6
                    self.p2_canvas_outliner.y = self.aesa.construction_canvas.y + 180 - 6
                    self.p2_canvas_outliner.resize(self.aesa.construction_canvas.width - 40 + 12, self.aesa.construction_canvas.height - 15 - 180 + 12)
                    
                    self.p2_shelf_outliner.x = self.aesa.object_tree.x - 1
                    self.p2_shelf_outliner.y = self.aesa.object_tree.y - 6
                    self.p2_shelf_outliner.resize(self.aesa.object_tree.width - 8, self.aesa.object_tree.height + 12)
                    
                    self.shelf_panel.x = self.aesa.object_tree.x+10
                    self.shelf_panel.y = self.aesa.object_tree.y+5
                    self.placer_pos = (self.shelf_panel.x+284, self.shelf_panel.y+1)
                    

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
        
        editor.screen.blit(self.mask, (self.aesa.x, self.aesa.y))
        
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
        
    