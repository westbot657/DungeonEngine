# pylint: disable=[W,R,C]

try:
    from GraphicsEngine.UIElement import UIElement
    from GraphicsEngine.Geometry import Box
    from GraphicsEngine.RenderPrimitives import Image
    from GraphicsEngine.Options import PATH, SETTINGS
    from GraphicsEngine.Text import Text
    from GraphicsEngine.MultilineText import MultilineText
    from GraphicsEngine.FunctionalElements import Button, Scrollable
    from GraphicsEngine.MultilineTextBox import MultilineTextBox
    from GraphicsEngine.Popup import Popup
    from GraphicsEngine.DiscordPresence import RPC, RPCD
except ImportError:
    from UIElement import UIElement
    from Geometry import Box
    from RenderPrimitives import Image
    from Options import PATH, SETTINGS
    from Text import Text
    from MultilineText import MultilineText
    from FunctionalElements import Button, Scrollable
    from MultilineTextBox import MultilineTextBox
    from Popup import Popup
    from DiscordPresence import RPC, RPCD

import random

class GameApp(UIElement):
    
    ####XXX###############################################XXX####
    ### XXX UI elements for game objects and combat stats XXX ###
    ####XXX###############################################XXX####
    
    class HealthBar(UIElement):
        
        __slots__ = [
            "x", "y", "width", "height", "max_health", "current_health", "background",
            "current", "shadow_heal", "shadow_damage", "full_bar", "current_bar",
            "shadow_heal_bar", "shadow_damage_bar", "shadow"
        ]
        
        def __init__(self, x, y, width, height, max_health, current_health, **options):
            """
            options:
                background (tuple | list | Color): color of empty bar. Defaults to (90, 90, 90)
                current_hp (tuple | list | Color): color of current health. Defaults to (20, 168, 0)
                shadow_heal (tuple | list | Color): color of recently earned health. Defaults to (26, 218, 0)
                shadow_damage (tuple | list | Color): color of recently lost health. Defaults to (210, 4, 4)
                
            """
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.max_health = max_health
            self.current_health = self.previous_health = current_health
            self.background = options.get("background", (90, 90, 90))
            self.current = options.get("current_hp", (20, 168, 0))
            self.shadow_heal = options.get("shadow_heal", (26, 218, 0))
            self.shadow_damage = options.get("shadow_damage", (210, 4, 4))
            self.full_bar = Box(0, 0, width, height, self.background)
            self.current_bar = Box(0, 0, (self.current_health/self.max_health)*width, height, self.current)
            self.shadow_heal_bar = Box(0, 0, 0, height, self.shadow_heal)
            self.shadow_damage_bar = Box(0, 0, 0, height, self.shadow_damage)
            self.shadow = ""
            self._alt_text = f"{self.current_health}/{self.max_health}"
    
        def set_current_health(self, health):

            if health < self.current_health:
                health = max(0, health)
                self.shadow_damage_bar.x = (health/self.max_health)*self.width
                self.shadow_damage_bar.width = ((self.current_health/self.max_health)*self.width) - self.shadow_damage_bar.x
                self.current_bar.width = (health/self.max_health)*self.width
                self.shadow = "damage"
                self.current_health = health
                
            elif health > self.current_health:
                health = min(self.max_health, health)
                self.shadow_heal_bar.x = (self.current_health/self.max_health)*self.width
                self.current_bar.width = (health/self.max_health)*self.width
                self.shadow_heal_bar.width =  self.current_bar.width - self.shadow_heal_bar.x
                self.shadow = "heal"
                self.current_health = health

            else:
                self.shadow = ""
            
            self._alt_text = f"{self.current_health}/{self.max_health}"
            
            
        def _event(self, editor, X, Y):
            if editor.collides(editor.mouse_pos, (X+self.x, Y+self.y, self.width, self.height)):
                if editor._hovering is None:
                    self.hovered = editor._hovered = True
                    editor._hovering = self
            else:
                self.hovered = False
    
        def _update(self, editor, X, Y):
            self.full_bar._update(editor, X+self.x, Y+self.y)
            self.current_bar._update(editor, X+self.x, Y+self.y)

            if self.shadow == "heal":
                self.shadow_heal_bar._update(editor, X+self.x, Y+self.y)

            elif self.shadow == "damage":
                self.shadow_damage_bar._update(editor, X+self.x, Y+self.y)

    class EnemyCard(UIElement):
        def __init__(self, game_app, enemy, y_pos):
            self.children = []
            self.width = 400
            self.height = 85
            self.x = 25
            self.y = y_pos
            self.enemy = enemy
            self.game_app = game_app
            self.background = Image(f"{PATH}/enemy_card.png", 0, 0, 400, 85)
            self.background_turn = Image(f"{PATH}/enemy_card_turn.png", 0, 0, 400, 85)
            self.name_display = Text(10, 10, 1, enemy.name, text_bg_color=None)
            self.health_bar = GameApp.HealthBar(290, 10, 100, 20, enemy.max_health, enemy.health)
            self._max = enemy.max_health
            self.health_display = Text(290, 12, 100, f"{enemy.health}/{enemy.max_health}", (0, 0, 0), text_size=14, text_bg_color=None)
            self.health_display.set_text(f"{self.enemy.health}/{self._max}")
            self.health_display.x = 340 - (self.health_display.width/2)
            self.old_health = enemy.health
            self.children.append(self.name_display)
            self.children.append(self.health_bar)
            self.children.append(self.health_display)
        
        def _update(self, editor, X, Y):

            if self.enemy is self.game_app.current_combat.turn:
                self.background_turn._update(editor, X+self.x, Y+self.y)

            else:
                self.background._update(editor, X+self.x, Y+self.y)

            for child in self.children:
                child._update(editor, X+self.x, Y+self.y)

        def _event(self, editor, X, Y):

            if self.old_health != self.enemy.health:
                self.health_display.set_text(f"{max(0, self.enemy.health)}/{self._max}")
                self.health_display.x = 340 - (self.health_display.width/2)
                self.health_bar.set_current_health(self.enemy.health)
                self.old_health = self.enemy.health
            
            for child in self.children:
                child._event(editor, X+self.x, Y+self.y)

    class GameCard(UIElement):
        height = 75

        @staticmethod
        def get_icon(obj):

            if p := SETTINGS["icons"].get(obj.abstract.identifier.full(), None):
                return Image(f"{PATH}/{p}.png", 0, 0, 25, 25)
            
            elif p := SETTINGS["icons"].get(obj.identifier.full()):
                return Image(f"{PATH}/{p}.png", 0, 0, 25, 25)
            
            return f"{PATH}/sword_icon.png"

    class WeaponCard(UIElement):
        
        def __init__(self, game_app, obj, x, y, active):
            self.game_app = game_app
            self.obj = obj
            self.x = x
            self.y = y
            self.width = 400
            self.height = GameApp.GameCard.height
            self.children = []
            self.background = Image(f"{PATH}/object_card.png", 0, 0, 400, GameApp.GameCard.height)
            self.background_active = Image(f"{PATH}/object_card_active.png", 0, 0, 400, GameApp.GameCard.height)
            self.icon = GameApp.GameCard.get_icon(obj)
            self.name_display = Text(30, 5, 370, obj.name, (255, 255, 255), text_bg_color=None)
            self.description_display = MultilineText(5, 30, 395, 20, obj.description or "", (206, 145, 120), None, text_size=10)
            self.damage_display = Text(5, 55, 100, f"{obj.damage.quickDisplay(self.game_app.editor.engine._function_memory)} damage", text_bg_color=None)
            self.damage_display._alt_text = obj.damage.fullDisplay(self.game_app.editor.engine._function_memory)
            self.durability_bar = GameApp.HealthBar(295, 55, 100, 15, obj.max_durability, obj.durability)
            self.children.append(self.icon)
            self.children.append(self.name_display)
            self.children.append(self.description_display)
            self.children.append(self.damage_display)
            self.children.append(self.durability_bar)
            self.active = active

        def _update(self, editor, X, Y):

            if self.active:
                self.background_active._update(editor, X+self.x, Y+self.y)

            else:
                self.background._update(editor, X+self.x, Y+self.y)

            for child in self.children:
                child._update(editor, X+self.x, Y+self.y)

        def _event(self, editor, X, Y):
            _c = self.children.copy()
            _c.reverse()

            for child in _c:
                child._event(editor, X+self.x, Y+self.y)

    class ToolCard(UIElement):

        def __init__(self, game_app, obj, x, y, active):
            self.game_app = game_app
            self.obj = obj
            self.x = x
            self.y = y
            self.width = 400
            self.height = GameApp.GameCard.height
            self.children = []
            self.background = Image(f"{PATH}/object_card.png", 0, 0, 400, GameApp.GameCard.height)
            self.background_active = Image(f"{PATH}/object_card_active.png", 0, 0, 400, GameApp.GameCard.height)
            self.icon = GameApp.GameCard.get_icon(obj)
            self.name_display = Text(30, 5, 370, obj.name, (255, 255, 255), text_bg_color=None)
            self.description_display = MultilineText(5, 30, 395, 20, obj.description or "", (206, 145, 120), None, text_size=10)
            self.durability_bar = GameApp.HealthBar(295, 55, 100, 15, obj.max_durability, obj.durability)
            self.children.append(self.icon)
            self.children.append(self.name_display)
            self.children.append(self.description_display)
            self.children.append(self.durability_bar)
            self.active = active

        def _update(self, editor, X, Y):

            if self.active:
                self.background_active._update(editor, X+self.x, Y+self.y)

            else:
                self.background._update(editor, X+self.x, Y+self.y)

            for child in self.children:
                child._update(editor, X+self.x, Y+self.y)

        def _event(self, editor, X, Y):
            _c = self.children.copy()
            _c.reverse()

            for child in _c:
                child._event(editor, X+self.x, Y+self.y)

    class AmmoCard(UIElement):
        def __init__(self, game_app, obj, x, y, active):
            self.game_app = game_app
            self.obj = obj
            self.x = x
            self.y = y
            self.width = 400
            self.height = GameApp.GameCard.height
            self.children = []
            self.background = Image(f"{PATH}/object_card.png", 0, 0, 400, GameApp.GameCard.height)
            self.background_active = Image(f"{PATH}/object_card_active.png", 0, 0, 400, GameApp.GameCard.height)
            self.icon = GameApp.GameCard.get_icon(obj)
            self.name_display = Text(30, 5, 370, obj.name, (255, 255, 255), text_bg_color=None)
            self.description_display = MultilineText(5, 30, 395, 20, obj.description or "", (206, 145, 120), None, text_size=10)
            dmg = obj.bonus_damage.quickDisplay(self.game_app.editor.engine._function_memory)
            self.damage_display = Text(5, 55, 100, f"{dmg} bonus damage", text_bg_color=None)
            self.damage_display._alt_text = obj.bonus_damage.fullDisplay(self.game_app.editor.engine._function_memory)
            self.count_disp = f"{obj.count}/{obj.max_count}" if obj.max_count > 0 else f"{obj.count}"
            self.count_display = Text(0, 0, 1, self.count_disp, text_bg_color=None)
            self.count_display.x = 395 - self.count_display.width
            self.count_display.y = 70 - self.count_display.height
            self.old_count = obj.count
            self.children.append(self.icon)
            self.children.append(self.name_display)
            self.children.append(self.description_display)
            self.children.append(self.damage_display)
            self.children.append(self.count_display)
            self.active = active

        def _update(self, editor, X, Y):

            if self.active:
                self.background_active._update(editor, X+self.x, Y+self.y)

            else:
                self.background._update(editor, X+self.x, Y+self.y)

            for child in self.children:
                child._update(editor, X+self.x, Y+self.y)

        def _event(self, editor, X, Y):

            if self.old_count != self.obj.count:
                self.count_disp = f"{self.obj.count}/{self.obj.max_count}" if self.obj.max_count > 0 else f"{self.obj.count}"
                self.count_display.set_text(self.count_disp)
                self.count_display.x = 395 - self.count_display.width

            _c = self.children.copy()
            _c.reverse()

            for child in _c:
                child._event(editor, X+self.x, Y+self.y)
    
    class ArmorCard(UIElement):

        def __init__(self, game_app, obj, x, y, active):
            self.game_app = game_app
            self.obj = obj
            self.x = x
            self.y = y
            self.width = 400
            self.height = GameApp.GameCard.height
            self.children = []
            self.background = Image(f"{PATH}/object_card.png", 0, 0, 400, GameApp.GameCard.height)
            self.background_active = Image(f"{PATH}/object_card_active.png", 0, 0, 400, GameApp.GameCard.height)
            self.icon = GameApp.GameCard.get_icon(obj)
            self.name_display = Text(30, 5, 370, obj.name, (255, 255, 255), text_bg_color=None)
            self.description_display = MultilineText(5, 30, 395, 20, obj.description or "", (206, 145, 120), None, text_size=10)
            self.damage_display = Text(5, 55, 100, f"{obj.damage_reduction.quickDisplay(self.game_app.editor.engine._function_memory)} defense", text_bg_color=None)
            self.damage_display._alt_text = obj.damage_reduction.fullDisplay(self.game_app.editor.engine._function_memory)
            self.durability_bar = GameApp.HealthBar(295, 55, 100, 15, obj.max_durability, obj.durability)
            self.children.append(self.icon)
            self.children.append(self.name_display)
            self.children.append(self.description_display)
            self.children.append(self.damage_display)
            self.children.append(self.durability_bar)
            self.active = active

        def _update(self, editor, X, Y):

            if self.active:
                self.background_active._update(editor, X+self.x, Y+self.y)

            else:
                self.background._update(editor, X+self.x, Y+self.y)

            for child in self.children:
                child._update(editor, X+self.x, Y+self.y)

        def _event(self, editor, X, Y):
            _c = self.children.copy()
            _c.reverse()

            for child in _c:
                child._event(editor, X+self.x, Y+self.y)
    
    class ItemCard(UIElement):

        def __init__(self, game_app, obj, x, y, active):
            self.game_app = game_app
            self.obj = obj
            self.x = x
            self.y = y
            self.width = 400
            self.height = GameApp.GameCard.height
            self.children = []
            self.background = Image(f"{PATH}/object_card.png", 0, 0, 400, GameApp.GameCard.height)
            self.background_active = Image(f"{PATH}/object_card_active.png", 0, 0, 400, GameApp.GameCard.height)
            self.icon = GameApp.GameCard.get_icon(obj)
            self.name_display = Text(30, 5, 370, obj.name, (255, 255, 255), text_bg_color=None)
            self.description_display = MultilineText(5, 30, 395, 20, obj.description or "", (206, 145, 120), None, text_size=10)
            self.count_disp = f"{obj.count}/{obj.max_count}" if obj.max_count > 0 else f"{obj.count}"
            self.count_display = Text(0, 0, 1, self.count_disp, text_bg_color=None)
            self.count_display.x = 395 - self.count_display.width
            self.count_display.y = 70 - self.count_display.height
            self.old_count = obj.count
            self.children.append(self.icon)
            self.children.append(self.name_display)
            self.children.append(self.description_display)
            self.children.append(self.count_display)
            self.active = active

        def _update(self, editor, X, Y):

            if self.active:
                self.background_active._update(editor, X+self.x, Y+self.y)

            else:
                self.background._update(editor, X+self.x, Y+self.y)

            for child in self.children:
                child._update(editor, X+self.x, Y+self.y)

        def _event(self, editor, X, Y):

            if self.old_count != self.obj.count:
                self.count_disp = f"{self.obj.count}/{self.obj.max_count}" if self.obj.max_count > 0 else f"{self.obj.count}"
                self.count_display.set_text(self.count_disp)
                self.count_display.x = 395 - self.count_display.width

            _c = self.children.copy()
            _c.reverse()

            for child in _c:
                child._event(editor, X+self.x, Y+self.y)

    def __init__(self, code_editor, editor):
        self.code_editor = code_editor
        self.children = []
        self.play_c1 = []
        self.play_c2 = []
        self.editor = editor
        self.player_id = 10
        self.player = None
        editor.game_app = self
        self.io_hook = editor.io_hook
        editor.io_hook.game_app = self

        self._available_buttons = "both" # for the play/online play buttons. options are "both" "online" "local"

        self.main_hud = Box(51, editor.height-106, editor.width-57, 85, (24, 24, 24))
        self.children.append(self.main_hud)
        self.main_hud_line = Box(51, editor.height-107, editor.width-52, 1, (70, 70, 70))
        self.children.append(self.main_hud_line)
        self.player_inventory = None
        self.current_combat = None
        self.page = "inv"

        self.page_inv_icons = (
            Image(f"{PATH}/page_inv_icon.png", 0, 0, 50, 51),
            Image(f"{PATH}/page_inv_icon_hovered.png", 0, 0, 50, 51),
            Image(f"{PATH}/page_inv_icon_selected.png", 0, 0, 50, 51)
        )
        self.page_inv_tab = Button(editor.width-(50*3), editor.height-107, 50, 51, "", self.page_inv_icons[2], hover_color=self.page_inv_icons[2], click_color=self.page_inv_icons[2])
        self.page_inv_tab.on_left_click = self.page_inv_onclick
        self.page_inv_tab._alt_text = "Inventory"
        self.children.append(self.page_inv_tab)

        self.page_combat_icons = (
            Image(f"{PATH}/page_combat_icon.png", 0, 0, 50, 51),
            Image(f"{PATH}/page_combat_icon_hovered.png", 0, 0, 50, 51),
            Image(f"{PATH}/page_combat_icon_selected.png", 0, 0, 50, 51)
        )
        self.page_combat_tab = Button(editor.width-(50*2), editor.height-107, 50, 51, "", self.page_combat_icons[0], hover_color=self.page_combat_icons[1], click_color=self.page_combat_icons[2])
        self.page_combat_tab.on_left_click = self.page_combat_onclick
        self.page_combat_tab._alt_text = "Combat Info"
        self.children.append(self.page_combat_tab)

        self.page_log_icons = (
            Image(f"{PATH}/page_log_icon.png", 0, 0, 50, 51),
            Image(f"{PATH}/page_log_icon_hovered.png", 0, 0, 50, 51),
            Image(f"{PATH}/page_log_icon_selected.png", 0, 0, 50, 51)
        )
        self.page_log_tab = Button(editor.width-(50), editor.height-107, 50, 51, "", self.page_log_icons[0], hover_color=self.page_log_icons[1], click_color=self.page_log_icons[2])
        self.page_log_tab.on_left_click = self.page_log_onclick
        self.page_log_tab._alt_text = "Game Output log"
        self.children.append(self.page_log_tab)

        self.tab_buttons = (
            ("inv", self.page_inv_tab, self.page_inv_icons),
            ("combat", self.page_combat_tab, self.page_combat_icons),
            ("log", self.page_log_tab, self.page_log_icons)
        )
        self.play_pause_buttons = (
            Image(f"{PATH}/play_gray.png", 0, 0, 50, 50),
            Image(f"{PATH}/play_solid.png", 0, 0, 50, 50),
            Image(f"{PATH}/pause_gray.png", 0, 0, 50, 50),
            Image(f"{PATH}/pause_solid.png", 0, 0, 50, 50)
        )
        self.online_play_pause_buttons = (
            Image(f"{PATH}/online_play_gray.png", 0, 0, 50, 50),
            Image(f"{PATH}/online_play_solid.png", 0, 0, 50, 50),
            Image(f"{PATH}/online_pause_gray.png", 0, 0, 50, 50),
            Image(f"{PATH}/online_pause_solid.png", 0, 0, 50, 50)
        )

        self.page_seperator_line = Box(editor.width-451, 21, 1, editor.height-128, (70, 70, 70))
        self.children.append(self.page_seperator_line)

        self.main_out_scrollable = Scrollable(52, 22, editor.width-504, editor.height-130, (31, 31, 31), left_bound=0, top_bound=0)
        self.main_output = MultilineText(0, 0, editor.width-504, editor.height-130, "", text_bg_color=(31, 31, 31))
        self.main_out_scrollable.children.append(self.main_output)
        self.children.append(self.main_out_scrollable)

        self.log_scrollable = Scrollable(editor.width-449, 22, 450, editor.height-130, (24, 24, 24), left_bound=0, top_bound=0)
        self.log_output = MultilineText(0, 0, 450, editor.height-130, "")
        self.log_scrollable.children.append(self.log_output)

        self.enemy_card_scrollable = Scrollable(editor.width-449, 22, 450, editor.height-130, left_bound=0, top_bound=0, right_bound=0)
        self.no_combat_text = Text(0, 0, 1, "You are not in combat", text_size=25)
        self.inventory_scrollable = Scrollable(editor.width-449, 22, 450, editor.height-130, left_bound=0, top_bound=0, right_bound=0, scroll_speed=30)
        self.empty_inventory_text = Text(0, 0, 1, "Your inventory is empty or not loaded", text_size=18)

        self.buttons_left_bar = Box(editor.width-553, 21, 1, 50, (70, 70, 70))
        self.buttons_middle_bar = Box(editor.width-502, 21, 1, 50, (70, 70, 70))
        self.buttons_bottom_bar_left = Box(editor.width-552, 71, 51, 1, (70, 70, 70))
        self.buttons_bottom_bar_right = Box(editor.width-501, 71, 51, 1, (70, 70, 70))
        self.children.append(self.buttons_left_bar)
        self.children.append(self.buttons_middle_bar)
        self.children.append(self.buttons_bottom_bar_left)
        self.children.append(self.buttons_bottom_bar_right)

        self.play_pause = Button(editor.width-501, 21, 50, 50, "", self.play_pause_buttons[0], hover_color=self.play_pause_buttons[1])
        self.play_pause._alt_text = "Start Game"
        self.play_pause.on_left_click = self.play_pause_toggle
        self.children.append(self.play_pause)
        self.play_c2 += [self.buttons_middle_bar, self.buttons_bottom_bar_right, self.play_pause]

        self.online_play_pause = Button(editor.width-552, 21, 50, 50, "", self.online_play_pause_buttons[0], hover_color=self.online_play_pause_buttons[1])
        self.online_play_pause._alt_text = "Play Online"
        self.online_play_pause.on_left_click = self.online_play_click
        self.children.append(self.online_play_pause)
        self.play_c1 += [self.buttons_left_bar, self.buttons_bottom_bar_left, self.online_play_pause]

        self.input_marker = Text(52, editor.height-106, content="Input:", text_bg_color=(70, 70, 70))
        self.input_box = MultilineTextBox(52+self.input_marker.width, editor.height-106, editor.width-504-self.input_marker.width, self.input_marker.height, text_bg_color=(70, 70, 70))
        self.children.append(self.input_marker)
        self.children.append(self.input_box)
        self.input_box.on_enter(self.input_on_enter)

        self.id_refresh = Button(56, editor.height-75, 15, 15, "", Image(f"{PATH}/id_refresh.png", 0, 0, 15, 15), hover_color=Image(f"{PATH}/id_refresh_hovered.png", 0, 0, 15, 15))
        self.id_refresh.on_left_click = self.refresh_player_data
        self.id_input = MultilineTextBox(71, editor.height-75, 15, 15, "10", text_bg_color=(31, 31, 31))
        self.id_input.single_line = True
        self.id_input.char_whitelist = [a for a in "0123456789"]
        self.children.append(self.id_refresh)
        self.children.append(self.id_input)

        self.player_name_display = Text(96, editor.height-75, content="[Start game to load player info]", text_size=15)
        self.player_location_display = Text(56, editor.height-55, 1, "[location]", text_size=12)
        self.player_money_display = Text(editor.width - 460, editor.height-75, 1, "[money]", text_bg_color=None, text_size=13)
        self._old_location = ""
        self.player_health_bar = GameApp.HealthBar(80+self.player_name_display.width + self.id_input._text_width+self.id_refresh.width, editor.height-75, 200, self.player_name_display.height, 20, 20)
        self._old_health = 0
        self.children += [self.player_name_display, self.player_location_display, self.player_money_display]

        self.new_player_button = Button(50, editor.height-33, 85, 13, " + NEW PLAYER", (31, 31, 31), text_size=10, hover_color=(70, 70, 70))
        self.new_player_button.on_left_click = self.popup_createplayer
        self.children.append(self.new_player_button)

        self.new_player_id_label = Text(15, 25, 1, "Player ID:", text_bg_color=None)
        self.new_player_name_label = Text(125, 25, 1, "Player Name:", text_bg_color=None)
        self.new_player_id_box = MultilineTextBox(15, 50, 75, 1, "10", text_bg_color=(70, 70, 70))
        self.new_player_id_box.single_line = True
        self.new_player_id_box.char_whitelist = [a for a in "0123456789"]
        self.new_player_id_box.on_enter(self.create_player_id_on_enter)
        self.new_player_name_box = MultilineTextBox(125, 50, 450, 1, "", text_bg_color=(70, 70, 70))
        self.new_player_name_box.single_line = True
        self.new_player_name_box.on_enter(self.create_player)

        self.new_player_error = MultilineText(15, 75, 570, 300, "", text_color=(255, 180, 180), text_bg_color=None)
        self.new_player_popup = Popup(600, 400).add_children(
            self.new_player_id_label,
            self.new_player_name_label,
            self.new_player_id_box,
            self.new_player_name_box,
            self.new_player_error
        )

    def popup_createplayer(self, editor):
        self.new_player_popup.popup()

    def create_player_id_on_enter(self, text_box):
        id = int(text_box.get_content())

        if id < 10:
            self.new_player_error.set_colored_content(f"Invalid ID:\nID must be 10 or larger.")
            text_box.set_content("10")
            return

        MultilineTextBox.set_focus(self.new_player_name_box)

    def create_player(self, text_box):
        name = text_box.get_content().strip()
        id = int(self.new_player_id_box.get_content())

        if id < 10 and not name:
            self.new_player_error.set_colored_content(f"Invalid ID:\nID must be 10 or larger.\n\nInvalid Name:\nName cannot be blank or whitespace.")
            self.new_player_id_box.set_content("10")
            return
        
        elif id < 10:
            self.new_player_error.set_colored_content(f"Invalid ID:\nID must be 10 or larger.")
            self.new_player_id_box.set_content("10")
            return
        
        elif not name:
            self.new_player_error.set_colored_content(f"Invalid Name:\nName cannot be blank or whitespace.")
            self.new_player_id_box.set_content("10")
            return
        
        else:
            self.editor.engine.handleInput(0, f"engine:new-player {id} \"{name}\"")

    def id_input_on_enter(self, text_box:MultilineTextBox):
        c = int(text_box.get_content())
        
        if c < 10:
            c = 10
            text_box.set_content("10")

        self.player_id = c
        self.refresh_player_data(self.editor)
    
    def refresh_player_data(self, editor):
        self.player_id = max(10, int(self.id_input.get_content()))
        self.id_input.set_content(str(self.player_id))
        editor.engine.handleInput(0, f"engine:ui/get_player {self.player_id}")

    def updateInventory(self, inventory=...):
        if inventory is not ...:
            self.player_inventory = inventory

        self.inventory_scrollable.children.clear()

        if self.player_inventory is not None:
            equips = self.player_inventory.equips.values()
            y = 10
            x = 25

            for item in self.player_inventory.contents:
                card = {
                    "engine:object/weapon": GameApp.WeaponCard,
                    "engine:object/ammo": GameApp.AmmoCard,
                    "engine:object/tool": GameApp.ToolCard,
                    "engine:object/item": GameApp.ItemCard,
                    "engine:object/armor": GameApp.ArmorCard,
                }.get(item.identifier.full())
                self.inventory_scrollable.children.append(
                    card(self, item, x, y, item in equips)
                )
                y += GameApp.GameCard.height + 10
    
    def updateCombat(self, combat=...):
        if combat is not ...:
            self.current_combat = combat
            
        self.enemy_card_scrollable.children.clear()
            
        if self.current_combat is not None:
            y = 25

            for entity in self.current_combat.turn_order:
                card = GameApp.EnemyCard(self, entity, y)
                y += card.height + 25
                self.enemy_card_scrollable.children.append(card)

    def updatePlayer(self, player=...):

        if player is not ...:
            self.player = player

        if self.player is None:
            self.player_name_display.set_text("[Start game to load player info]")
            self.player_location_display.set_text("[location]")
            self.player_money_display.set_text("[money]")
        
        else:
            self._old_health = player.health
            self.player_name_display.set_text(self.player.name)
            self.player_health_bar.max_health = self.player.max_health
            self.player_health_bar.set_current_health(self.player.health)
            self.player_health_bar.set_current_health(self.player.health)
            self.player_location_display.set_text(self.player.location.translate(self.editor.engine._function_memory))
            self.player_money_display.set_text(str(self.player.currency))

    def input_on_enter(self, text_box:MultilineTextBox):
        text = text_box.get_content().strip()
        text_box.set_content("")
        text_box.cursor_location.line = 0
        text_box.cursor_location.col = 0
        self.io_hook.sendInput(self.player_id, text)

    def play_pause_toggle(self, editor):
        # print("Toggling local play/pause")
        if editor.engine.running:
            editor.engine.stop()
            self.play_pause.bg_color = self.play_pause._bg_color = self.play_pause_buttons[0]
            self.play_pause.hover_color = self.play_pause_buttons[1]
            self.play_pause._alt_text = "Start Game"
            self._available_buttons = "both"
            self.updateInventory(None)
            self.updateCombat(None)

        else:
            editor.engine.start()
            editor.engine.handleInput(0, f"engine:ui/get_inventory {self.player_id}")
            editor.engine.handleInput(0, f"engine:ui/get_combat {self.player_id}")
            editor.engine.handleInput(0, f"engine:ui/get_player {self.player_id}")
            self.play_pause.bg_color = self.play_pause._bg_color = self.play_pause_buttons[2]
            self.play_pause.hover_color = self.play_pause_buttons[3]
            self.play_pause._alt_text = "Stop Game"
            self._available_buttons = "local"

    def online_play_click(self, editor):
        # print("Toggling online play/pause")
        if self.online_play_pause._alt_text == "Play Online":
            self.online_play_pause._alt_text = "Disconnect"
            self.online_play_pause.bg_color = self.online_play_pause._bg_color = self.online_play_pause_buttons[2]
            self.online_play_pause.hover_color = self.online_play_pause_buttons[3]
            self._available_buttons = "online"
        else:
            self.online_play_pause._alt_text = "Play Online"
            self.online_play_pause.bg_color = self.online_play_pause._bg_color = self.online_play_pause_buttons[0]
            self.online_play_pause.hover_color = self.online_play_pause_buttons[1]
            self._available_buttons = "both"

    def set_page(self, page:str):

        for name, tab, icons in self.tab_buttons:

            if page == name:
                tab.bg_color = tab._bg_color = tab.hover_color = icons[2]

            else:
                tab.bg_color = tab._bg_color = icons[0]
                tab.hover_color = icons[1]
    
    def page_inv_onclick(self, editor):
        self.editor.engine.handleInput(0, f"engine:ui/get_inventory {self.player_id}")
        self.page = "inv"
        RPCD["state"] = random.choice([
            "Playing strategicaly (maybe? idk lmao)",
            "Having Fun! (hopefully)",
            "¯\\_(ツ)_/¯",
            "<Insert goofy message here>"
        ])
        self.set_page("inv")
    
    def page_combat_onclick(self, editor):
        self.editor.engine.handleInput(0, f"engine:ui/get_combat {self.player_id}")
        self.page = "combat"

        if self.current_combat:
            RPCD["state"]=random.choice([
                "Currently in combat! (don't distract me (or do, I don't care lol))",
                "Fighting uhh...  something! (I might make it actually say what when combat actually works)"
            ])
            RPC.update(**RPCD)

        else:
            RPCD["state"]=random.choice([
                "Staring at the combat page for no reason",
                "\"I'm delirious and think I'm in combat!\" (This message was written by ADHD)",
                "Pikachu! I choose you! (Pikachu isn't in this game (probably))"
            ])
            RPC.update(**RPCD)

        self.set_page("combat")
        
    def page_log_onclick(self, editor):
        self.page = "log"
        RPCD["state"]=random.choice([
            "Debugging",
            "HACKING! (not really)",
            "Analyzing the game logs to see what on earth is going on"
        ])
        RPC.update(**RPCD)
        self.set_page("log")
    
    def _update_layout(self, editor):
        self.main_hud.y = editor.height-106
        self.main_hud.width = editor.width-57
        self.main_hud_line.y = editor.height-107
        self.main_hud_line.width = editor.width - 52
        
        self.main_output.min_width = self.main_out_scrollable.width = editor.width - 504
        self.main_output.min_height = self.main_out_scrollable.height = editor.height - 130
        
        self.page_inv_tab.x = editor.width-(50*3)
        self.page_inv_tab.y = editor.height-107
        
        self.page_combat_tab.x = editor.width-(50*2)
        self.page_combat_tab.y = editor.height-107
        
        self.page_log_tab.x = editor.width-50
        self.page_log_tab.y = editor.height-107
        
        self.page_seperator_line.x = editor.width - 451
        self.page_seperator_line.height = editor.height - (23 + 105)
        
        self.input_marker.y = self.input_box.y = editor.height - 106
        self.input_box.min_width = self.main_out_scrollable.width - self.input_marker.width
        
        self.enemy_card_scrollable.x = self.log_scrollable.x = self.inventory_scrollable.x = editor.width-449
        
        self.log_output.min_height = self.log_scrollable.height = self.enemy_card_scrollable.height = self.inventory_scrollable.height = editor.height-130
        
        
        self.id_input.y = self.id_refresh.y = self.player_name_display.y = self.player_money_display.y = self.player_health_bar.y = editor.height-75
        
        self.player_name_display.x = 70 + self.id_input._text_width + self.id_refresh.width
        self.player_health_bar.x = 80 + self.player_name_display.width + self.id_input._text_width + self.id_refresh.width
        self.player_location_display.y = editor.height - 55
        self.player_money_display.x = editor.width - self.player_money_display.width - 460
        
        self.new_player_button.y = editor.height - 33
        
        if self._available_buttons == "online":
            self.buttons_left_bar.x = self.buttons_bottom_bar_left.x = editor.width-502
            self.online_play_pause.x = (editor.width-501)
        else:
            self.buttons_left_bar.x = self.buttons_bottom_bar_left.x = editor.width-553
            self.online_play_pause.x = (editor.width-552)
        self.play_pause.x = (editor.width-501)
        self.buttons_middle_bar.x = self.buttons_bottom_bar_right.x = editor.width - 502
        
        
        self.no_combat_text.x = (editor.width-224)-(self.no_combat_text.width/2)
        self.no_combat_text.y = self.log_scrollable.y + (self.log_output.min_height/2) - (self.no_combat_text.height/2)

        self.empty_inventory_text.x = (editor.width-224)-(self.empty_inventory_text.width/2)
        self.empty_inventory_text.y = self.log_scrollable.y + (self.log_output.min_height/2) - (self.empty_inventory_text.height/2)

    def _event(self, editor, X, Y):
        if editor._do_layout_update:
            self._update_layout(editor)

        for child in self.children[::-1]:
            child._event(editor, X, Y)
            
        if self.page == "log":
            self.log_scrollable._event(editor, X, Y)

        elif self.page == "combat":

            if self.current_combat is not None:
                self.enemy_card_scrollable._event(editor, X, Y)

            else:
                self.no_combat_text._event(editor, X, Y)

        elif self.page == "inv":

            if self.player_inventory:
                self.inventory_scrollable._event(editor, X, Y)

            else:
                self.empty_inventory_text._event(editor, X, Y)
        
        if (self.player is not None):

            if self.player.health != self._old_health:
                self._old_health = self.player.health
                self.player_health_bar.set_current_health(self._old_health)

            if self._old_location != self.player.location.full():
                self._old_location = self.player.location.full()
                self.player_location_display.content = self.player.location.translate(self.editor.engine._function_memory)

    def _update(self, editor, X, Y):

        for child in self.children:
            if (child in self.play_c1 and self._available_buttons == "local") or (child in self.play_c2 and self._available_buttons == "online"):
                continue
            child._update(editor, X, Y)
            
        if self.page == "log":
            self.log_scrollable._update(editor, X, Y)

        elif self.page == "combat":

            if self.current_combat is not None:
                self.enemy_card_scrollable._update(editor, X, Y)

            else:
                self.no_combat_text._update(editor, X, Y)

        elif self.page == "inv":

            if self.player_inventory:
                self.inventory_scrollable._update(editor, X, Y)

            else:
                self.empty_inventory_text._update(editor, X, Y)
        
        if self.player is not None:
            self.player_health_bar._update(editor, X, Y)

