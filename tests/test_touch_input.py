"""
Pruebas headless de la entrada táctil (FINGER*) y de la adaptación a Android.

Se ejecutan sin pantalla ni audio reales:
    SDL_VIDEODRIVER=offscreen SDL_AUDIODRIVER=dummy ARKANOID_TOUCH=1 \
        .venv/bin/python tests/test_touch_input.py

Cada caso simula eventos FINGERDOWN/FINGERMOTION/FINGERUP de SDL2 (coordenadas
normalizadas 0..1 sobre la superficie lógica) y comprueba el efecto esperado.
"""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "offscreen")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("ARKANOID_TOUCH", "1")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402

import main  # noqa: E402
from main import (  # noqa: E402
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TOUCH_BUTTONS,
    Game,
)


def finger_event(event_type, finger_id, x_screen, y_screen):
    """Crea un evento FINGER* como los emite SDL2 (x, y normalizadas 0..1)."""
    return pygame.event.Event(
        event_type,
        touch_id=1,
        finger_id=finger_id,
        x=x_screen / SCREEN_WIDTH,
        y=y_screen / SCREEN_HEIGHT,
        dx=0.0,
        dy=0.0,
    )


def tap(game, finger_id, x, y):
    """Simula un toque rápido (FINGERDOWN + FINGERUP sin desplazamiento)."""
    game.handle_finger_event(finger_event(main.FINGERDOWN_EVENT, finger_id, x, y))
    game.handle_finger_event(finger_event(main.FINGERUP_EVENT, finger_id, x, y))


def drag(game, finger_id, x0, y0, x1, y1):
    """Simula un arrastre (FINGERDOWN + FINGERMOTION + FINGERUP)."""
    game.handle_finger_event(finger_event(main.FINGERDOWN_EVENT, finger_id, x0, y0))
    game.handle_finger_event(finger_event(main.FINGERMOTION_EVENT, finger_id, x1, y1))
    game.handle_finger_event(finger_event(main.FINGERUP_EVENT, finger_id, x1, y1))


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"  ok: {message}")


def test_finger_to_screen():
    game = Game()
    ev = finger_event(main.FINGERDOWN_EVENT, 1, 320, 240)
    x, y = game.finger_to_screen(ev)
    check(abs(x - 320) < 0.01 and abs(y - 240) < 0.01, "finger_to_screen escala 0..1 a píxeles lógicos")


def test_tap_menu_starts_game():
    game = Game()
    check(game.game_state == "menu", "arranca en el menú")
    tap(game, 1, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    check(game.game_state == "playing", "un toque en el menú empieza la partida")


def test_tap_releases_stuck_ball():
    game = Game()
    game.game_state = "playing"
    check(game.waiting_for_ball_release, "la pelota empieza pegada")
    tap(game, 1, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    check(not game.waiting_for_ball_release, "un toque libera la pelota pegada")
    check(not any(b.stuck_to_paddle for b in game.balls), "ninguna pelota sigue pegada")


def test_drag_moves_paddle():
    game = Game()
    game.game_state = "playing"
    game.release_stuck_ball()
    target_x = 500  # coordenada lógica de pantalla (dentro de la zona de juego)
    drag(game, 1, SCREEN_WIDTH // 2, 600, target_x, 600)
    expected = target_x - main.PLAY_OFFSET_X - game.paddle.width // 2
    expected = max(0, min(expected, main.WINDOW_WIDTH - game.paddle.width))
    check(
        abs(game.paddle.x - expected) <= 1,
        f"el arrastre mueve la paleta a x={game.paddle.x} (esperado {expected})",
    )


def test_touch_button_sound_toggles():
    game = Game()
    game.game_state = "playing"
    before = game.sound_manager.enabled
    rect = TOUCH_BUTTONS["sound"]
    tap(game, 1, rect.centerx, rect.centery)
    check(game.sound_manager.enabled != before, "el botón ♪ alterna el sonido")


def test_touch_button_pause_toggles():
    game = Game()
    game.game_state = "playing"
    rect = TOUCH_BUTTONS["pause"]
    tap(game, 1, rect.centerx, rect.centery)
    check(game.paused, "el botón II pausa la partida")
    tap(game, 2, rect.centerx, rect.centery)
    check(not game.paused, "el botón II reanuda la partida")


def test_touch_button_freeplay_adds_ball():
    game = Game()
    game.game_state = "playing"
    game.release_stuck_ball()
    n_before = len(game.balls)
    rect = TOUCH_BUTTONS["freeplay"]
    tap(game, 1, rect.centerx, rect.centery)
    check(len(game.balls) == n_before + 1, "el botón +BOLA EXTRA añade una pelota")


def test_emulated_mouse_events_are_ignored():
    """Los MOUSE* emulados por SDL2 desde toques (touch=True) no deben actuar dos veces."""
    game = Game()
    game.game_state = "playing"
    game.release_stuck_ball()
    n_before = len(game.balls)
    rect = TOUCH_BUTTONS["freeplay"]
    pygame.event.clear()
    pygame.event.post(
        pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            pos=(rect.centerx, rect.centery),
            button=1,
            touch=True,
        )
    )
    game.handle_events()
    check(len(game.balls) == n_before, "el ratón emulado por toque no ejecuta la acción")


def test_real_mouse_click_still_works():
    game = Game()
    game.game_state = "playing"
    game.release_stuck_ball()
    n_before = len(game.balls)
    rect = TOUCH_BUTTONS["freeplay"]
    ev = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, pos=(rect.centerx, rect.centery), button=1, touch=False
    )
    game._on_click(ev.pos)
    check(len(game.balls) == n_before + 1, "el clic de ratón real sigue funcionando")


def test_tap_on_result_screen_advances():
    game = Game()
    game.game_state = "victory"
    level_before = game.level
    tap(game, 1, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    check(game.level == level_before + 1, "un toque en victoria avanza de nivel")
    check(game.game_state == "playing", "y vuelve a estar jugando")


def test_multitouch_paddle_and_fire():
    """Un dedo mueve la paleta y otro mantenido dispara (como el botón del ratón)."""
    game = Game()
    game.game_state = "playing"
    game.release_stuck_ball()
    # Dedo 1: arrastra la paleta (queda como dedo de la paleta)
    game.handle_finger_event(finger_event(main.FINGERDOWN_EVENT, 1, 400, 600))
    game.handle_finger_event(finger_event(main.FINGERMOTION_EVENT, 1, 300, 600))
    check(game.paddle_finger_id == 1, "el dedo 1 controla la paleta")
    check(game.touch_firing, "un dedo no-UI mantenido activa el fuego continuo")
    # Dedo 2: se mantiene pulsado -> sigue el fuego
    game.handle_finger_event(finger_event(main.FINGERDOWN_EVENT, 2, 700, 400))
    check(game.touch_firing, "el segundo dedo mantiene el fuego continuo")
    game.handle_finger_event(finger_event(main.FINGERUP_EVENT, 2, 700, 400))
    check(game.touch_firing, "con el dedo 1 aún pulsado sigue el fuego continuo")
    game.handle_finger_event(finger_event(main.FINGERUP_EVENT, 1, 300, 600))
    check(not game.touch_firing, "al levantar todos los dedos cesa el fuego continuo")


def main_test():
    tests = [
        test_finger_to_screen,
        test_tap_menu_starts_game,
        test_tap_releases_stuck_ball,
        test_drag_moves_paddle,
        test_touch_button_sound_toggles,
        test_touch_button_pause_toggles,
        test_touch_button_freeplay_adds_ball,
        test_emulated_mouse_events_are_ignored,
        test_real_mouse_click_still_works,
        test_tap_on_result_screen_advances,
        test_multitouch_paddle_and_fire,
    ]
    failures = 0
    for test in tests:
        print(f"[test] {test.__name__}")
        try:
            test()
        except AssertionError as exc:
            failures += 1
            print(f"  FALLO: {exc}")
        pygame.event.clear()
    print()
    if failures:
        print(f"{failures} prueba(s) fallida(s)")
        sys.exit(1)
    print(f"Las {len(tests)} pruebas pasaron correctamente")


if __name__ == "__main__":
    main_test()