import pygame

from core.level.level import BaseLevel
from core.entities.ball import Ball

from core.utils.spritesheet import load_image, slice_spritesheet
from core.physics.platforms import PLATFORM_TILES
from core.physics.moving_platform import MovingPlatform

from core.entities.player import Player
from core.entities.bullet import Bullet

from ui.hud import HUD


class Level2(BaseLevel):

    def __init__(self, pantalla, ANCHO, ALTO):
        super().__init__(pantalla, ANCHO, ALTO)

        # ---------------------------------------------------------
        # CONFIGURACIÓN BÁSICA
        # ---------------------------------------------------------
        self.tile_w = 16
        self.tile_h = 16

        self.time_remaining = 80

        # Límites + HUD
        self.setup_level_boundaries(hud_height=50, floor_offset=48)
        self.hud = HUD(ANCHO, self.hud_height, hud_y_start=0)

        # Plataformas móviles
        self.moving_platforms = []

        # ---------------------------------------------------------
        # SPAWN PROGRESIVO DE BOLAS
        # ---------------------------------------------------------
        self.max_balls = 5
        self.spawned_balls = 0

        self.ball_spawn_delay = 2500 # aca lo puedo ajystar segun que tan rapido quiero quesalgan
        self.last_ball_spawn_time = pygame.time.get_ticks()

        self.double_spawn_triggered = False
        self.spawning_finished = False

        # Cargar recursos
        self.load_assets()

        # Plataformas y entidades
        self.setup_platforms()
        self.spawn_initial_entities()

    # -------------------------------------------------------------
    def load_assets(self):

        self._load_tiles()

        Player.load_assets()
        Bullet.load_assets()
        self.setup_player()

        # Fondo
        try:
            bg = pygame.image.load("assets/mapa2.png").convert()
            game_area_height = self.ALTO - self.game_area_y_start
            bg_scaled = pygame.transform.scale(bg, (self.ANCHO, game_area_height))

            self.background = pygame.Surface((self.ANCHO, self.ALTO))
            self.background.fill((18, 18, 30))
            self.background.blit(bg_scaled, (0, self.game_area_y_start))
        except:
            self.background = None

        # Música
        try:
            pygame.mixer.music.load("assets/sounds/lvl2.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            pass

    # -------------------------------------------------------------
    def _load_tiles(self):
        sheet = load_image("assets/blocks/block.png")
        raw_tiles = slice_spritesheet(sheet, 16, 16)

        PLATFORM_TILES.update({
            "top_left": raw_tiles[0],
            "top": raw_tiles[1],
            "top_right": raw_tiles[11],

            "left": raw_tiles[12],
            "fill": raw_tiles[24],
            "right": raw_tiles[23],

            "bottom_left": raw_tiles[96],
            "bottom": raw_tiles[97],
            "bottom_right": raw_tiles[107],
        })

    # -------------------------------------------------------------
    def setup_platforms(self):

        self.add_centered_platform(
            self.ANCHO // 2,
            int(self.ALTO * 0.82),
            220,
            30
        )

        platform_configs = [
            (self.ANCHO * 0.20, int(self.ALTO * 0.45), 160, 24, 160, 2, 1),
            (self.ANCHO * 0.70, int(self.ALTO * 0.32), 160, 24, 180, 2, -1),
            (self.ANCHO * 0.45, int(self.ALTO * 0.20), 180, 24, 200, 3, 1),
        ]

        for x, y, w, h, move_range, speed, direction in platform_configs:
            platform = MovingPlatform(
                x=int(x),
                y=y,
                width=w,
                height=h,
                move_range=move_range,
                speed=speed
            )
            platform.direction = direction

            self.moving_platforms.append(platform)
            self.platform_system.platforms.append(platform)

    # -------------------------------------------------------------
    def spawn_initial_entities(self):
        self.balls.clear()
        self.spawned_balls = 0
        self.spawning_finished = False
        self.last_ball_spawn_time = pygame.time.get_ticks()
        self.double_spawn_triggered = False

    # -------------------------------------------------------------
    def update_ball_spawning(self):

        if self.spawned_balls >= self.max_balls:
            self.spawning_finished = True
            return

        now = pygame.time.get_ticks()
        spawn_amount = 1

        if self.player and self.player.lives == 1 and not self.double_spawn_triggered:
            spawn_amount = 2
            self.double_spawn_triggered = True

        if now - self.last_ball_spawn_time >= self.ball_spawn_delay:

            x_positions = [
                self.ANCHO // 6,
                self.ANCHO // 3,
                self.ANCHO // 2,
                self.ANCHO * 2 // 3,
                self.ANCHO * 5 // 6
            ]

            velocities = [-4, -2, 2, 3, -3]

            for _ in range(spawn_amount):
                if self.spawned_balls >= self.max_balls:
                    break

                self.balls.append(
                    Ball(
                        x_positions[self.spawned_balls],
                        self.game_area_y_start + 20,
                        "medium",
                        vx=velocities[self.spawned_balls],
                        vy=0
                    )
                )

                self.spawned_balls += 1

            self.last_ball_spawn_time = now

    # -------------------------------------------------------------
    def setup_player(self):
        sprites = Player._player_sprites
        self.player = Player(
            self.ANCHO // 2 - sprites[0].get_width() // 2,
            self.floor_y - sprites[0].get_height()
        )

    # -------------------------------------------------------------
    def update(self, dt):

        for platform in self.moving_platforms:
            platform.update()

        super().update(dt)

        #  EVITAR VICTORIA ANTES DE TIEMPO
        if not self.spawning_finished:
            self.level_won = False

        self.update_ball_spawning()

        # Victoria REAL
        if self.spawning_finished and not self.balls:
            self.level_won = True

    # -------------------------------------------------------------
    def draw(self):
        super().draw()

        self.hud.update(
            lives=self.player.lives if self.player else 3,
            score=self.score,
            time=self.time_remaining,
            game_over=self.game_over,
            level_won=self.level_won
        )
        self.hud.draw(self.pantalla)

    # -------------------------------------------------------------
    def detener_musica(self):
        pygame.mixer.music.stop()
