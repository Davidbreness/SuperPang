# =============================================================================
# main.py
# Punto de entrada del juego Super Pang con sistema de menú mejorado
# =============================================================================

import pygame
from config import ANCHO, ALTO, FPS
from core.level.level1 import Level1
from core.level.level2 import Level2
# from core.level.level3 import Level3  # Descomentar cuando lo crees
from ui.menu import Menu


def main():
    # -------------------------------------------------------------------------
    # Inicialización del motor Pygame
    # -------------------------------------------------------------------------
    try:
        pygame.init()
        pygame.mixer.init()
    except Exception as e:
        print(f" Error inicializando Pygame: {e}")
        return
    
    # Crear ventana principal
    try:
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Super Pang")
    except Exception as e:
        print(f" Error creando ventana: {e}")
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
    clock_tick = 0  # Para debugging
    
    while corriendo:
        # Limitar FPS para evitar sobrecarga
        dt = reloj.tick(60)  # Máximo 60 FPS
        clock_tick += 1
        
        eventos = pygame.event.get()
        
        # Detectar cierre de ventana
        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False
        
        # =====================================================================
        # ESTADO: MENÚ
        # =====================================================================
        if estado == "menu":
            # Manejar input del menú
            accion = menu.handle_input(eventos)

            # Procesar selección del usuario
            if accion == "level_1":
                print(" Cargando Level 1...")
                try:
                    # Detener música del menú
                    menu.stop_menu_music()

                    nivel_actual = Level1(pantalla, ANCHO, ALTO)
                    nivel_actual.load_assets()
                    nivel_actual.spawn_initial_entities()
                    estado = "jugando"

                    # Aplicar configuración de volumen
                    pygame.mixer.music.set_volume(menu.music_volume)
                except Exception as e:
                    print(f" Error cargando Level 1: {e}")

            elif accion == "level_2":
                print("🎮 Cargando Level 2...")
                try:
                    # Detener música del menú
                    menu.stop_menu_music()

                    nivel_actual = Level2(pantalla, ANCHO, ALTO)
                    nivel_actual.load_assets()
                    nivel_actual.spawn_initial_entities()
                    estado = "jugando"

                    # Aplicar configuración de volumen
                    pygame.mixer.music.set_volume(menu.music_volume)
                except Exception as e:
                    print(f" Error cargando Level 2: {e}")

            elif accion == "level_3":
                print("  Level 3 no implementado aún")

            elif accion == "exit":
                print(" Saliendo del juego...")
                corriendo = False

            # Dibujar menú
            menu.draw(pantalla)
            pygame.display.flip()
        
        # =====================================================================
        # ESTADO: JUGANDO
        # =====================================================================
        elif estado == "jugando":
            # Manejar eventos del nivel (movimiento, disparo, ESC)
            should_continue = nivel_actual.handle_events(eventos)
            
            # Si el jugador presiona ESC, volver al menú
            if not should_continue:
                print("🔙 Volviendo al menú...")
                nivel_actual.detener_musica()

                nivel_actual = None

                # LIMPIAR mixer antes de volver al menú
                pygame.mixer.music.stop()
                pygame.mixer.stop()  # detiene TODOS los sonidos
                pygame.mixer.music.unload()  # limpia la música cargada

                # Forzar que el menú crea que no hay música
                menu.menu_music_playing = False
                menu.menu_music_loaded = False

                estado = "menu"
                continue



            
            # Actualizar nivel: jugador, balas, bolas, colisiones, timer
            nivel_actual.update(dt)
            
            # Renderizar: fondo, entidades, HUD
            nivel_actual.draw()
            
            # Actualizar pantalla
            pygame.display.flip()
            
            # ----------------------------------------------------------------
            # OPCIONAL: Detectar fin del nivel (ganar/perder)
            # ----------------------------------------------------------------
            # Volver automáticamente al menú al terminar:
            # if nivel_actual.hud.game_over or nivel_actual.hud.level_won:
            #     pygame.time.wait(3000)  # Espera 3 segundos
            #     nivel_actual.detener_musica()
            #     nivel_actual = None
            #     estado = "menu"
    
    # -------------------------------------------------------------------------
    # Cleanup al salir
    # -------------------------------------------------------------------------
    if nivel_actual:
        nivel_actual.detener_musica()
    
    pygame.quit()
    print(" Juego cerrado correctamente")


if __name__ == "__main__":
    main()