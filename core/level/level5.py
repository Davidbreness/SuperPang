import pygame
from core.level.level1 import Level1
from core.entities.ball import Ball
from core.utils.spritesheet import load_image


class Level5(Level1):
    """
    Nivel 5 – Dificultad Alta
    Más bolas y mayor velocidad que niveles anteriores.
    Fondo propio para diferenciar el nivel.
    """

    def __init__(self, pantalla, ANCHO, ALTO):
        super().__init__(pantalla, ANCHO, ALTO)

    # ==========================================================================
    #  FONDO DIFERENTE DEL NIVEL 5
    # ==========================================================================
    def _load_background(self):
        """
        Carga el fondo específico del nivel 5
        """
        try:
            bg = load_image("assets/level5_bg.png")
            game_area_height = self.ALTO - self.game_area_y_start
            bg_scaled = pygame.transform.scale(bg, (self.ANCHO, game_area_height))

            self.background = pygame.Surface((self.ANCHO, self.ALTO))
            self.background.fill((18, 18, 30))
            self.background.blit(bg_scaled, (0, self.game_area_y_start))

        except Exception as e:
            print("Error cargando fondo Level 5:", e)
            self.background = None

    # ==========================================================================
    #  BOLAS INICIALES – NIVEL 5
    # ==========================================================================
    def spawn_initial_entities(self):
        """
        Genera:
        - 2 bolas grandes en la plataforma superior
        - 2 bolas medianas en plataformas laterales
        - Velocidad aumentada
        """

        self.balls = []

        r_big = 40
        r_med = 25

        # -------------------------
        # Dos bolas grandes arriba
        # -------------------------
        cx = self.top_platform.rect.centerx
        cy = self.top_platform.rect.top - r_big

        self.balls.append(Ball(cx - 60, cy, "big", vx=4, vy=-9))
        self.balls.append(Ball(cx + 60, cy, "big", vx=-4, vy=-9))

        # -------------------------
        # Bola mediana izquierda
        # -------------------------
        lx = self.left_platform.rect.centerx
        ly = self.left_platform.rect.top - r_med
        self.balls.append(Ball(lx, ly, "medium", vx=4, vy=-8))

        # -------------------------
        # Bola mediana derecha
        # -------------------------
        rx = self.right_platform.rect.centerx
        ry = self.right_platform.rect.top - r_med
        self.balls.append(Ball(rx, ry, "medium", vx=-4, vy=-8))
