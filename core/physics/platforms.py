import pygame
from core.utils.spritesheet import slice_spritesheet, load_image
from core.entities.ball import Ball   # necesario para bounce_vertical

PLATFORM_TILES = {}

# ================================================================
#region PLATFORM TILE SURFACE BUILDER
# Genera una superficie completa para una plataforma usando tiles
# ================================================================
def build_platform_surface(width, height, tiles):
    cols = width // 16
    rows = height // 16
    
    surf = pygame.Surface((cols * 16, rows * 16), pygame.SRCALPHA)

    for y in range(rows):
        for x in range(cols):

            # Bordes superiores
            if y == 0 and x == 0:
                tile = tiles["top_left"]
            elif y == 0 and x == cols - 1:
                tile = tiles["top_right"]
            elif y == 0:
                tile = tiles["top"]

            # Bordes inferiores
            elif y == rows - 1 and x == 0:
                tile = tiles["bottom_left"]
            elif y == rows - 1 and x == cols - 1:
                tile = tiles["bottom_right"]
            elif y == rows - 1:
                tile = tiles["bottom"]

            # Laterales
            elif x == 0:
                tile = tiles["left"]
            elif x == cols - 1:
                tile = tiles["right"]

            # Centro
            else:
                tile = tiles["fill"]

            surf.blit(tile, (x * 16, y * 16))

    return surf
#endregion
# ================================================================



# ================================================================
#region PLATFORM CLASS
# Maneja cada plataforma individualmente: gráfica, hitbox y colisiones
# ================================================================
class Platform:
    def __init__(self, x, y, width, height, platform_type="normal"):
        # Hitbox principal del bloque
        self.rect = pygame.Rect(x, y, width, height)
        self.type = platform_type

        # Superficie construida con tiles
        self.surface = build_platform_surface(width, height, PLATFORM_TILES)

        # Hitbox recortado para colisiones más suaves
        self.hitbox = self._create_adjusted_hitbox()

    # -------------------------------------------------------------
    def _create_adjusted_hitbox(self):
        """Recorta unos pixeles para evitar colisiones duras."""
        hitbox_padding = 2
        return pygame.Rect(
            self.rect.x + hitbox_padding,
            self.rect.y + hitbox_padding,
            self.rect.width - (hitbox_padding * 2),
            self.rect.height - (hitbox_padding * 2)
        )

    # -------------------------------------------------------------
    def get_bounce_factor(self):
        """Devuelve el factor de rebote según el tipo de plataforma."""
        return {
            "normal": 0.9,
            "bouncy": 1.3,
            "sticky": 0.6,
            "breakable": 0.9,
        }.get(self.type, 0.9)

    # -------------------------------------------------------------
    def check_ball_collision(self, ball):
        """Colisión bola-plataforma usando hitbox reducida."""
        closest_x = max(self.hitbox.left, min(ball.x, self.hitbox.right))
        closest_y = max(self.hitbox.top, min(ball.y, self.hitbox.bottom))
        
        dx = ball.x - closest_x
        dy = ball.y - closest_y
        radius = ball.radius_by_size[ball.size]

        return (dx*dx + dy*dy) <= (radius * radius)

    # -------------------------------------------------------------
    def check_bullet_collision(self, bullet):
        """Rect simple para colisiones bala-plataforma."""
        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
        return bullet_rect.colliderect(self.hitbox)

    # -------------------------------------------------------------
    def draw(self, screen):
        """Dibuja la plataforma con tiles."""
        screen.blit(self.surface, self.rect)
#endregion
# ================================================================



# ================================================================
#region ADVANCED PLATFORM SYSTEM
# Gestor general: agrega plataformas, maneja rebotes y destruibles
# ================================================================
class AdvancedPlatformSystem:
    def __init__(self):
        self.platforms = []
        self.breakable_platforms = set()

    # -------------------------------------------------------------
    # Agregar plataforma normal y devolver referencia
    def add_platform(self, x, y, width, height, platform_type="normal"):
        platform = Platform(x, y, width, height, platform_type)
        self.platforms.append(platform)

        if platform.type == "breakable":
            self.breakable_platforms.add(platform)

        return platform

    # -------------------------------------------------------------
    # Agregar plataforma centrada según posición media
    def add_centered_platform(self, center_x, center_y, width, height, platform_type="normal"):
        x = center_x - width // 2
        y = center_y - height // 2
        return self.add_platform(x, y, width, height, platform_type)

    # -------------------------------------------------------------
    # Detección general de colisiones con bolas
    def process_ball_collisions(self, ball):
        for platform in self.platforms[:]:
            if platform.check_ball_collision(ball):
                self._handle_collision(ball, platform)
                return True
        return False

    # -------------------------------------------------------------
    def _handle_collision(self, ball, platform):
        """Determina el comportamiento según tipo de plataforma."""
        if platform.type == "breakable":
            self._handle_breakable_collision(ball, platform)
        else:
            self._handle_normal_collision(ball, platform)

    # -------------------------------------------------------------
    # Colisión plataforma normal
    def _handle_normal_collision(self, ball, platform):
        bounce_factor = platform.get_bounce_factor()
        r = ball.radius_by_size[ball.size]

        prev_x = ball.x - ball.vx
        prev_y = ball.y - ball.vy

        # COLISIÓN LATERAL
        if prev_x + r <= platform.rect.left or prev_x - r >= platform.rect.right:
            ball.vx = -ball.vx * bounce_factor
            if ball.x < platform.rect.left:
                ball.x = platform.rect.left - r
            else:
                ball.x = platform.rect.right + r
            return

        # COLISIÓN POR ARRIBA (rebote hacia arriba)
        if prev_y < platform.rect.top:
            ball.bounce_vertical(use_min_height=False)
            ball.y = platform.rect.top - r
            return

        # COLISIÓN POR DEBAJO (empujar hacia abajo sin rebotar hacia arriba)
        ball.vy = abs(ball.vy) * 0.8
        ball.y = platform.rect.bottom + r
        ball.just_bounced = 3

    # -------------------------------------------------------------
    # Colisión en plataformas rompibles
    def _handle_breakable_collision(self, ball, platform):
        self._handle_normal_collision(ball, platform)
        if platform in self.platforms:
            self.platforms.remove(platform)
            self.breakable_platforms.discard(platform)

    # -------------------------------------------------------------
    def draw(self, screen):
        """Dibuja TODAS las plataformas del nivel."""
        for platform in self.platforms:
            platform.draw(screen)
#endregion
# ================================================================



