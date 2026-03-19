import sys
import pygame

from LudoBoardSystem.settings import *
from LudoBoardSystem.helpers import clamp, smooth_approach
from LudoBoardSystem.assets import Assets
from LudoBoardSystem.menu import MainMenu
from LudoBoardSystem.gameplay import Gameplay

BOARD_SIZE = 710

BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_SIZE) // 2

CELL = BOARD_SIZE / 15.0


def cell_center(col, row):
    x = BOARD_X + (col + 0.5) * CELL
    y = BOARD_Y + (row + 0.5) * CELL
    return (round(x), round(y))


def main():
    pygame.init()

    try:
        pygame.mixer.init()
        audio_enabled = True
    except pygame.error:
        audio_enabled = False

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Ludo Adventures")

    game_canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    clock = pygame.time.Clock()

    assets = Assets(audio_enabled)
    menu = MainMenu(assets)
    gameplay = Gameplay(assets)

    game_started = False

    bg_offset_x = 0.0
    bg_offset_y = 0.0
    art_offset_x = 0.0
    art_offset_y = 0.0

    run = True
    while run:
        dt = clock.tick(FPS) / 1000.0
        time_ms = pygame.time.get_ticks()

        window_w, window_h = pygame.display.get_window_size()
        scale = min(window_w / SCREEN_WIDTH, window_h / SCREEN_HEIGHT)
        scale = max(scale, 0.01)

        scaled_w = int(SCREEN_WIDTH * scale)
        scaled_h = int(SCREEN_HEIGHT * scale)
        offset_x = (window_w - scaled_w) // 2
        offset_y = (window_h - scaled_h) // 2

        raw_mouse_x, raw_mouse_y = pygame.mouse.get_pos()
        mx = int((raw_mouse_x - offset_x) / scale)
        my = int((raw_mouse_y - offset_y) / scale)
        mx = clamp(mx, 0, SCREEN_WIDTH)
        my = clamp(my, 0, SCREEN_HEIGHT)
        mouse_pos = (mx, my)

        mouse_dx = (mx - SCREEN_WIDTH / 2) / (SCREEN_WIDTH / 2)
        mouse_dy = (my - SCREEN_HEIGHT / 2) / (SCREEN_HEIGHT / 2)
        mouse_dx = clamp(mouse_dx, -1, 1)
        mouse_dy = clamp(mouse_dy, -1, 1)

        target_bg_offset_x = -mouse_dx * BASE_BG_PARALLAX_STRENGTH
        target_bg_offset_y = -mouse_dy * BASE_BG_PARALLAX_STRENGTH
        target_art_offset_x = -mouse_dx * ART_PARALLAX_STRENGTH
        target_art_offset_y = -mouse_dy * ART_PARALLAX_STRENGTH

        bg_offset_x = smooth_approach(bg_offset_x, target_bg_offset_x, 5.0, dt)
        bg_offset_y = smooth_approach(bg_offset_y, target_bg_offset_y, 5.0, dt)
        art_offset_x = smooth_approach(art_offset_x, target_art_offset_x, 5.0, dt)
        art_offset_y = smooth_approach(art_offset_y, target_art_offset_y, 5.0, dt)

        play_btn_rect = menu.get_play_button_rect()
        adventure_btn_rect = menu.get_adventure_button_rect()

        is_hovering_play = (not game_started) and play_btn_rect.collidepoint(mouse_pos)
        is_hovering_adventure = (not game_started) and adventure_btn_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game_started:
                    if is_hovering_play:
                        game_started = True
                        assets.load_random_game_bg()

                    elif is_hovering_adventure:
                        from rpgEngine.rpgEngine import run_game
                        run_game()
                        return

                elif game_started and not gameplay.move_queue and not gameplay.dice_rolling:
                    clicked_pawn = gameplay.select_pawn_at_mouse(mouse_pos)
                    if not clicked_pawn:
                        gameplay.start_dice_roll(mouse_pos)

        game_canvas.fill(WHITE)

        current_bg = assets.game_bg if (game_started and assets.game_bg) else assets.menu_bg
        bg_w, bg_h = current_bg.get_size()
        bg_draw_x = (SCREEN_WIDTH - bg_w) // 2 + int(bg_offset_x)
        bg_draw_y = (SCREEN_HEIGHT - bg_h) // 2 + int(bg_offset_y)
        game_canvas.blit(current_bg, (bg_draw_x, bg_draw_y))

        if not game_started:
            menu.update(dt, is_hovering_play, is_hovering_adventure)
            menu.draw(game_canvas, time_ms, art_offset_x, art_offset_y)
        else:
            if menu.button_alpha > 0:
                menu.button_alpha = max(0, menu.button_alpha - int(400 * dt))

            gameplay.update_dice(dt)
            gameplay.update_particles(dt)
            scaled_player = gameplay.update_player(dt, mouse_pos)

            gameplay.draw_particles(game_canvas)
            gameplay.draw(game_canvas, scaled_player)

        screen.fill(BLACK)
        scaled_surface = pygame.transform.scale(game_canvas, (scaled_w, scaled_h))
        screen.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()