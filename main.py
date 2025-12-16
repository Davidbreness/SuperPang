# =============================================================================
# main.py
# Punto de entrada del juego Super Pang con sistema de menú mejorado
# =============================================================================

import pygame
from config import ANCHO, ALTO, FPS

from core.level.level1 import Level1
from core.level.level5 import Level5
from core.level.level6 import Level6

from ui.menu import Menu


def main():
    # -------------------------------------------------------------------------
    # Inicialización del motor Pygame
    # -------------------------------------------------------------------------
    try:
        pygame.init()
        pygame.mixer.init()
    except Exception as e:
        print(f"Error inicializando Pygame: {e}")
        return

    # Crear ventana principal
    try:
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Super Pang")
    except Exception as e:
        print(f"Error creando ventana: {e}")
        pygame.quit()
        return

    reloj = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Estado del juego y menú
    # -------------------------------------------------------------------------
    estado = "menu"  # Estados posibles: "menu", "jugando"
    nivel_actual = None
    menu = Menu(ANCHO, ALTO)

    # -------------------------------------------------------------------------
    # Loop principal del juego
    # -------------------------------------------------------------------------
    corriendo = True

    while corriendo:
        dt = reloj.tick(FPS)
        eventos = pygame.event.get()

        # Detectar cierre de ventana
        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False

        # =====================================================================
        # ESTADO: MENÚ
        # =====================================================================
        if estado == "menu":
            accion = menu.handle_input(eventos)

            if accion == "level_1":
                print("🎮 Cargando Level 1...")
                try:
                    menu.stop_menu_music()
                    nivel_actual = Level1(pantalla, ANCHO, ALTO)
                    nivel_actual.load_assets()
                    estado = "jugando"
                    pygame.mixer.music.set_volume(menu.music_volume)
                except Exception as e:
                    print(f"Error cargando Level 1: {e}")

            elif accion == "level_5":
                print("🎮 Cargando Level 5...")
                try:
                    menu.stop_menu_music()
                    nivel_actual = Level5(pantalla, ANCHO, ALTO)
                    nivel_actual.load_assets()
                    estado = "jugando"
                    pygame.mixer.music.set_volume(menu.music_volume)
                except Exception as e:
                    print(f"Error cargando Level 5: {e}")

            elif accion == "level_6":
                print("🎮 Cargando Level 6...")
                try:
                    menu.stop_menu_music()
                    nivel_actual = Level6(pantalla, ANCHO, ALTO)
                    nivel_actual.load_assets()
                    estado = "jugando"
                    pygame.mixer.music.set_volume(menu.music_volume)
                except Exception as e:
                    print(f"Error cargando Level 6: {e}")

            elif accion == "exit":
                print("Saliendo del juego...")
                corriendo = False

            # Dibujar menú
            menu.draw(pantalla)
            pygame.display.flip()

        # =====================================================================
        # ESTADO: JUGANDO
        # =====================================================================
        elif estado == "jugando":
            should_continue = nivel_actual.handle_events(eventos)

            # Volver al menú con ESC
            if not should_continue:
                print("🔙 Volviendo al menú...")
                nivel_actual.detener_musica()
                nivel_actual = None

                pygame.mixer.music.stop()
                pygame.mixer.stop()
                pygame.mixer.music.unload()

                menu.menu_music_playing = False
                menu.menu_music_loaded = False

                estado = "menu"
                continue

            # Actualizar y dibujar nivel
            nivel_actual.update(dt)
            nivel_actual.draw()
            pygame.display.flip()

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------
    if nivel_actual:
        nivel_actual.detener_musica()

    pygame.quit()
    print("Juego cerrado correctamente")


if __name__ == "__main__":
    main()
