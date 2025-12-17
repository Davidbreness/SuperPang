import pygame
from core.physics.platforms import Platform


class MovingPlatform(Platform):
    """
    Plataforma móvil horizontal.
    Se mueve en el eje X entre dos límites.
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        move_range=120,
        speed=2,
        platform_type="normal"
    ):
        super().__init__(x, y, width, height, platform_type)

        # Posición base
        self.start_x = x

        # Movimiento
        self.move_range = move_range
        self.speed = speed
        self.direction = 1  # 1 = derecha, -1 = izquierda

    # -------------------------------------------------------------
    def update(self):
        """Actualiza el movimiento horizontal"""

        self.rect.x += self.speed * self.direction
        self.hitbox.x = self.rect.x + 2  # mantener hitbox alineada

        # Límite derecho
        if self.rect.x >= self.start_x + self.move_range:
            self.rect.x = self.start_x + self.move_range
            self.direction = -1

        # Límite izquierdo
        elif self.rect.x <= self.start_x - self.move_range:
            self.rect.x = self.start_x - self.move_range
            self.direction = 1
