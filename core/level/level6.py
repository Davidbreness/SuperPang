import pygame
from core.level.level1 import Level1
from core.entities.ball import Ball
from core.utils.spritesheet import load_image


class Level6(Level1):
    """
    Nivel 6 – NIVEL FINAL
    Reutiliza Level1, aumenta la dificultad
    y utiliza un fondo propio.
    """

    def __init__(self, pantalla, ANCHO, ALTO):
        super().__init__(pantalla, ANCHO, ALTO)

    # ==========================================================================
    #  FONDO DIFERENTE DEL NIVEL 6
    # ==========================================================================
    def _load_background(self):
        """
        Carga el fondo específico del nivel 6
        """
        try:
            bg = load_image("assets/level6_bg.png")
            game_area_height = self.ALTO - self.game_area_y_start
            bg_scaled = pygame.transform.scale(bg, (self.ANCHO, game_area_height))

            self.background = pygame.Surface((self.ANCHO, self.ALTO))
            self.background.fill((10, 10, 25))
            self.background.blit(bg_scaled, (0, self.game_area_y_start))

        except Exception as e:
            print("Error cargando fondo Level 6:", e)
            self.background = None

    # ==========================================================================
    #  BOLAS INICIALES – NIVEL 6
    # ==========================================================================
    def spawn_initial_entities(self):
        """
        Genera:
        - 3 bolas grandes
        - 2 bolas medianas
        - Velocidad alta (nivel final)
        """

        self.balls = []

        r_big = 40
        r_med = 25

        # -------------------------
        # Bolas grandes (plataforma superior)
        # -------------------------
        cx = self.top_platform.rect.centerx
        cy = self.top_platform.rect.top - r_big

        self.balls.append(Ball(cx - 100, cy, "big", vx=5, vy=-10))
        self.balls.append(Ball(cx,        cy, "big", vx=-5, vy=-10))
        self.balls.append(Ball(cx + 100,  cy, "big", vx=6, vy=-10))

        # -------------------------
        # Bolas medianas laterales
        # -------------------------
        lx = self.left_platform.rect.centerx
        ly = self.left_platform.rect.top - r_med
        self.balls.append(Ball(lx, ly, "medium", vx=5, vy=-9))

        rx = self.right_platform.rect.centerx
        ry = self.right_platform.rect.top - r_med
        self.balls.append(Ball(rx, ry, "medium", vx=-5, vy=-9))
