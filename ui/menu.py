# =============================================================================
# ui/menu.py
# Sistema de menú principal con submenús
# =============================================================================

import pygame
from core.audio.audio_manager import AudioManager


class Menu:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        # Estado del menú
        self.menu_state = "main"

        # Opciones
        self.main_options = ["Niveles", "Configuracion", "Salir"]

        # 🔥 NIVELES ACTUALIZADOS
        self.level_options = [
            "Level 1",
            "Level 2",
            "Level 3",
            "Level 5",
            "Level 6",
            "Volver"
        ]

        self.settings_options = ["Volumen Musica", "Volumen SFX", "Volver"]
        self.selected_option = 0

        # Configuración
        self.music_volume = 0.7
        self.sfx_volume = 0.5

        # Música del menú
        self.menu_music_playing = False
        self.menu_music_loaded = False

        # Colores
        self.bg_color = (20, 20, 40)
        self.title_color = (255, 200, 50)
        self.selected_color = (255, 100, 100)
        self.normal_color = (200, 200, 200)
        self.subtitle_color = (150, 150, 200)

        # Cursor gráfico
        try:
            self.cursor_img = pygame.image.load("assets/hand_cursor0000.png").convert_alpha()
            self.cursor_img = pygame.transform.scale(self.cursor_img, (32, 32))
        except:
            self.cursor_img = None

        # Fuentes
        font_path = "assets/fonts/ARCADECLASSIC.TTF"
        try:
            self.font_title = pygame.font.Font(font_path, 72)
            self.font_subtitle = pygame.font.Font(font_path, 42)
            self.font_option = pygame.font.Font(font_path, 36)
            self.font_small = pygame.font.Font(font_path, 20)
        except:
            self.font_title = pygame.font.SysFont("Arial", 64, bold=True)
            self.font_subtitle = pygame.font.SysFont("Arial", 38, bold=True)
            self.font_option = pygame.font.SysFont("Arial", 32)
            self.font_small = pygame.font.SysFont("Arial", 18)

        # Fondo
        try:
            self.background = pygame.image.load("assets/sprites/menu_bg.png")
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except:
            self.background = None

    # -------------------------------------------------------------------------
    # MÚSICA
    # -------------------------------------------------------------------------
    def start_menu_music(self):
        if self.menu_music_loaded is False:
            try:
                pygame.mixer.music.load("assets/sounds/OrbitalColossus.mp3")
                self.menu_music_loaded = True
            except:
                self.menu_music_loaded = None
                return

        if self.menu_music_loaded and not self.menu_music_playing:
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.menu_music_playing = True

    def stop_menu_music(self):
        pygame.mixer.music.stop()
        self.menu_music_playing = False

    # -------------------------------------------------------------------------
    # INPUT
    # -------------------------------------------------------------------------
    def handle_input(self, eventos):
        current_options = self._get_current_options()

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_UP, pygame.K_w):
                    self.selected_option = (self.selected_option - 1) % len(current_options)
                    self._play_menu_sound()

                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_option = (self.selected_option + 1) % len(current_options)
                    self._play_menu_sound()

                elif evento.key in (pygame.K_LEFT, pygame.K_a):
                    if self.menu_state == "settings":
                        self._adjust_setting(-1)

                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    if self.menu_state == "settings":
                        self._adjust_setting(1)

                elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return self._handle_selection()

                elif evento.key == pygame.K_ESCAPE:
                    if self.menu_state != "main":
                        self.menu_state = "main"
                        self.selected_option = 0
                        self._play_menu_sound()

        return None

    # -------------------------------------------------------------------------
    # MANEJO DE MENÚS
    # -------------------------------------------------------------------------
    def _get_current_options(self):
        if self.menu_state == "main":
            return self.main_options
        if self.menu_state == "levels":
            return self.level_options
        if self.menu_state == "settings":
            return self.settings_options
        return []

    def _handle_selection(self):
        if self.menu_state == "main":
            return self._handle_main_menu()
        if self.menu_state == "levels":
            return self._handle_level_menu()
        if self.menu_state == "settings":
            return self._handle_settings_menu()
        return None

    def _handle_main_menu(self):
        if self.selected_option == 0:
            self.menu_state = "levels"
            self.selected_option = 0
            self._play_menu_sound()
        elif self.selected_option == 1:
            self.menu_state = "settings"
            self.selected_option = 0
            self._play_menu_sound()
        elif self.selected_option == 2:
            return "exit"
        return None

    # 🔥 MENÚ DE NIVELES ACTUALIZADO
    def _handle_level_menu(self):
        if self.selected_option == 0:
            return "level_1"
        if self.selected_option == 1:
            return "level_2"
        if self.selected_option == 2:
            return "level_3"
        if self.selected_option == 3:
            return "level_5"
        if self.selected_option == 4:
            return "level_6"
        if self.selected_option == 5:
            self.menu_state = "main"
            self.selected_option = 0
            self._play_menu_sound()
        return None

    def _handle_settings_menu(self):
        if self.selected_option == 2:
            self.menu_state = "main"
            self.selected_option = 0
            self._play_menu_sound()
        return None

    # -------------------------------------------------------------------------
    # AJUSTES
    # -------------------------------------------------------------------------
    def _adjust_setting(self, direction):
        if self.selected_option == 0:
            self.music_volume = max(0.0, min(1.0, self.music_volume + direction * 0.1))
            AudioManager.set_music_volume(self.music_volume)
            pygame.mixer.music.set_volume(self.music_volume)
            self._play_menu_sound()

        elif self.selected_option == 1:
            self.sfx_volume = max(0.0, min(1.0, self.sfx_volume + direction * 0.1))
            AudioManager.set_sfx_volume(self.sfx_volume)

    # -------------------------------------------------------------------------
    # SONIDO
    # -------------------------------------------------------------------------
    def _play_menu_sound(self):
        try:
            sound = pygame.mixer.Sound("assets/sounds/beep.mp3")
            sound.set_volume(self.sfx_volume)
            sound.play()
        except:
            pass

    # -------------------------------------------------------------------------
    # DIBUJO
    # -------------------------------------------------------------------------
    def draw(self, screen):
        self.start_menu_music()

        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(self.bg_color)

        if self.menu_state == "main":
            self._draw_main_menu(screen)
        elif self.menu_state == "levels":
            self._draw_level_menu(screen)
        elif self.menu_state == "settings":
            self._draw_settings_menu(screen)

    def _draw_main_menu(self, screen):
        title = self.font_title.render("SUPER PANG", True, self.title_color)
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 80))
        self._draw_options(screen, self.main_options, 280)

    def _draw_level_menu(self, screen):
        title = self.font_title.render("SUPER PANG", True, self.title_color)
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 60))

        subtitle = self.font_subtitle.render("Select Level", True, self.subtitle_color)
        screen.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 150))

        self._draw_options(screen, self.level_options, 240)

    def _draw_settings_menu(self, screen):
        title = self.font_title.render("SUPER PANG", True, self.title_color)
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 60))

        subtitle = self.font_subtitle.render("Settings", True, self.subtitle_color)
        screen.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 150))

        start_y = 280
        spacing = 70

        for i, option in enumerate(self.settings_options):
            color = self.selected_color if i == self.selected_option else self.normal_color
            text = option
            if i < 2:
                text = f"{option} {int((self.music_volume if i == 0 else self.sfx_volume) * 100)}"

            surf = self.font_option.render(text, True, color)
            x = self.width // 2 - surf.get_width() // 2
            y = start_y + i * spacing

            if i == self.selected_option:
                if self.cursor_img:
                    screen.blit(self.cursor_img, (x - 40, y - 5))
                else:
                    screen.blit(self.font_option.render(">", True, self.selected_color), (x - 50, y))

            screen.blit(surf, (x, y))

    def _draw_options(self, screen, options, start_y):
        spacing = 70
        for i, option in enumerate(options):
            color = self.selected_color if i == self.selected_option else self.normal_color
            surf = self.font_option.render(option, True, color)
            x = self.width // 2 - surf.get_width() // 2
            y = start_y + i * spacing

            if i == self.selected_option:
                if self.cursor_img:
                    screen.blit(self.cursor_img, (x - 40, y - 5))
                else:
                    screen.blit(self.font_option.render(">", True, self.selected_color), (x - 50, y))

            screen.blit(surf, (x, y))
