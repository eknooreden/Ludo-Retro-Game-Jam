import pygame
import math
import random as rdm
from pygame import image, transform
import sys

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
game_canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) 

pygame.display.set_caption("Ludo Adventures")

screen_color = (255, 255, 255)
PLAYER_MARGIN = 30
stud = 5
block_size = 17 * stud

sound = "assets/sounds"
background = "assets/backgrounds"

red_bg = f"{background}/red_bg.png"
blue_bg = f"{background}/blue_bg.png"
yellow_bg = f"{background}/yellow_bg.png"
green_bg = f"{background}/green_bg.png"

backgrounds = [red_bg, blue_bg, yellow_bg, green_bg]
try:
    chosen_background = rdm.choice(backgrounds)
    full_bg = pygame.transform.scale(pygame.image.load(chosen_background), (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_rect = full_bg.get_rect()
except Exception as e:
    full_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    full_bg.fill((100, 100, 100))
    bg_rect = full_bg.get_rect()

play_button_img = "assets/main_menu/play_button.png"
button_base_w, button_base_h = 58 * stud, 20 * stud
play_button_src = pygame.image.load(play_button_img).convert_alpha()

game_title_img = "assets/main_menu/title.png"
game_title = transform.scale(image.load(game_title_img), (300, 180))
game_title_rect = game_title.get_rect(center=(SCREEN_WIDTH//2, 150))

player_img = "assets/game/player/player_red.png"
player_base_w, player_base_h = 15 * stud, 15 * stud
player_src = pygame.transform.scale(pygame.image.load(player_img).convert_alpha(), (player_base_w, player_base_h))

button_current_scale = 1.0
button_alpha = 255
game_started = False
player_current_scale = 1.0
player_is_clicked = False
target_x, target_y = float(PLAYER_MARGIN), float(PLAYER_MARGIN)
player_rect = player_src.get_rect(topleft=(target_x, target_y))
speed = 250
clock = pygame.time.Clock()

run = True
while run:
    dt = clock.tick(60) / 1000.0
    time_ms = pygame.time.get_ticks()

    window_w, window_h = pygame.display.get_window_size()
    scale = min(window_w / SCREEN_WIDTH, window_h / SCREEN_HEIGHT)
    
    offset_x = (window_w - (SCREEN_WIDTH * scale)) // 2
    offset_y = (window_h - (SCREEN_HEIGHT * scale)) // 2
    
    raw_mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (
        (raw_mouse_pos[0] - offset_x) / scale,
        (raw_mouse_pos[1] - offset_y) / scale
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_hovering_btn: game_started = True
            elif is_hovering_player: player_is_clicked = not player_is_clicked
        elif event.type == pygame.KEYDOWN and game_started:
            if player_rect.x == round(target_x) and player_rect.y == round(target_y):
                moved = False
                if event.key == pygame.K_RIGHT: target_x += block_size; moved = True
                elif event.key == pygame.K_LEFT: target_x -= block_size; moved = True
                elif event.key == pygame.K_UP: target_y -= block_size; moved = True
                elif event.key == pygame.K_DOWN: target_y += block_size; moved = True
                if moved:
                    target_x = max(PLAYER_MARGIN, min(target_x, SCREEN_WIDTH - player_rect.width - PLAYER_MARGIN))
                    target_y = max(PLAYER_MARGIN, min(target_y, SCREEN_HEIGHT - player_rect.height - PLAYER_MARGIN))

    button_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    temp_btn_rect = pygame.Rect(0, 0, button_base_w, button_base_h)
    temp_btn_rect.center = button_center
    
    is_hovering_btn = temp_btn_rect.collidepoint(mouse_pos) and not game_started
    is_hovering_player = player_rect.collidepoint(mouse_pos) and game_started

    game_canvas.fill(screen_color)
    game_canvas.blit(full_bg, bg_rect)

    if game_started:
        if button_alpha > 0: button_alpha = max(0, button_alpha - 400 * dt)
        
        is_moving = player_rect.x != target_x or player_rect.y != target_y
        player_target_scale = 1.4 if is_moving else (1.2 if (is_hovering_player or player_is_clicked) else 1.0)
        player_current_scale += (player_target_scale - player_current_scale) * 12 * dt

        if player_rect.x < target_x: player_rect.x = min(target_x, player_rect.x + speed * dt)
        elif player_rect.x > target_x: player_rect.x = max(target_x, player_rect.x - speed * dt)
        if player_rect.y < target_y: player_rect.y = min(target_y, player_rect.y + speed * dt)
        elif player_rect.y > target_y: player_rect.y = max(target_y, player_rect.y - speed * dt)

        p_w, p_h = int(player_base_w * player_current_scale), int(player_base_h * player_current_scale)
        scaled_player = pygame.transform.scale(player_src, (p_w, p_h))
        game_canvas.blit(scaled_player, scaled_player.get_rect(center=player_rect.center))

    if button_alpha > 0:
        button_target_scale = 1.08 if is_hovering_btn else 1.0
        button_current_scale += (button_target_scale - button_current_scale) * 10 * dt
        sway_angle = math.sin(time_ms * 0.005) * 3
        b_w, b_h = int(button_base_w * button_current_scale), int(button_base_h * button_current_scale)
        scaled_btn = pygame.transform.scale(play_button_src, (b_w, b_h))
        rotated_btn = pygame.transform.rotate(scaled_btn, sway_angle)
        rotated_btn.set_alpha(button_alpha)
        game_canvas.blit(rotated_btn, rotated_btn.get_rect(center=button_center))
        game_canvas.blit(game_title, game_title_rect)

    screen.fill((0, 0, 0))
    new_size = (int(SCREEN_WIDTH * scale), int(SCREEN_HEIGHT * scale))
    scaled_content = pygame.transform.smoothscale(game_canvas, new_size)
    screen.blit(scaled_content, (offset_x, offset_y))
    
    pygame.display.flip()

pygame.quit()
sys.exit()