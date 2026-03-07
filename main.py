import pygame
import math
import random as rdm
from pygame import image, transform
import sys
import os

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
game_canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) 

pygame.display.set_caption("Ludo Adventures")

screen_color = (255, 255, 255)
PLAYER_MARGIN = 30
stud = 5
block_size = 17 * stud

dice_path = "assets/game/dice"
dice_images = []
for i in range(1, 7):
    img_path = f"{dice_path}/{i}_dice.png"
    if os.path.exists(img_path):
        dice_images.append(pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (80, 80)))
    else:
        surf = pygame.Surface((80, 80))
        surf.fill((200, 200, 200))
        dice_images.append(surf)

try:
    move_sound = pygame.mixer.Sound("assets/sounds/move.wav")
    dice_roll_snd = pygame.mixer.Sound("assets/sounds/dice_roll.wav")
    dice_finish_snd = pygame.mixer.Sound("assets/sounds/dice_finish.wav")
except:
    move_sound = dice_roll_snd = dice_finish_snd = None

background = "assets/backgrounds"
backgrounds = [f"{background}/red_bg.png", f"{background}/blue_bg.png", f"{background}/yellow_bg.png", f"{background}/green_bg.png"]
try:
    chosen_background = rdm.choice(backgrounds)
    full_bg = pygame.transform.scale(pygame.image.load(chosen_background), (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_rect = full_bg.get_rect()
except:
    full_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    full_bg.fill((100, 100, 100))
    bg_rect = full_bg.get_rect()

play_button_src = pygame.image.load("assets/main_menu/play_button.png").convert_alpha()
game_title = transform.scale(image.load("assets/main_menu/title.png"), (300, 180))
game_title_rect = game_title.get_rect(center=(SCREEN_WIDTH//2, 150))

background_art = transform.scale(
    image.load("assets/main_menu/background_art.png"),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
bga_rect = background_art.get_rect()

player_colors = ["assets/game/player/player_red.png", "assets/game/player/player_green.png", "assets/game/player/player_blue.png", "assets/game/player/player_yellow.png"]
player_src = pygame.transform.scale(pygame.image.load(rdm.choice(player_colors)).convert_alpha(), (15*stud, 15*stud))

button_current_scale = 1.0
button_alpha = 255
game_started = False
player_current_scale = 1.0
pawn_is_selected = False
current_x, current_y = float(PLAYER_MARGIN), float(PLAYER_MARGIN)
move_queue = []
last_target_x, last_target_y = current_x, current_y
player_rect = player_src.get_rect(topleft=(current_x, current_y))
speed = 180
clock = pygame.time.Clock()
particles = []

dice_rolling = False
dice_roll_duration = 1.2
dice_timer = 0
dice_frame_timer = 0
dice_frame_index = 0
final_dice_val = 1
target_dir = (0, 0)
show_dice = False

run = True
while run:
    dt = clock.tick(60) / 1000.0
    time_ms = pygame.time.get_ticks()

    window_w, window_h = pygame.display.get_window_size()
    scale = min(window_w / SCREEN_WIDTH, window_h / SCREEN_HEIGHT)
    offset_x = (window_w - (SCREEN_WIDTH * scale)) // 2
    offset_y = (window_h - (SCREEN_HEIGHT * scale)) // 2
    
    raw_mouse_pos = pygame.mouse.get_pos()
    mx = (raw_mouse_pos[0] - offset_x) / scale
    my = (raw_mouse_pos[1] - offset_y) / scale
    mouse_pos = (mx, my)

    is_hovering_btn = pygame.Rect(SCREEN_WIDTH//2-145, SCREEN_HEIGHT//2-50, 290, 100).collidepoint(mouse_pos) and not game_started
    is_hovering_player = player_rect.collidepoint(mouse_pos) and game_started

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_hovering_btn: 
                game_started = True
            elif game_started and not move_queue and not dice_rolling:
                if is_hovering_player:
                    pawn_is_selected = not pawn_is_selected
                elif pawn_is_selected:
                    dice_rolling = True
                    show_dice = True
                    dice_timer = dice_roll_duration
                    pawn_is_selected = False
                    target_dir = (mouse_pos[0] - player_rect.centerx, mouse_pos[1] - player_rect.centery)

    game_canvas.fill(screen_color)
    game_canvas.blit(full_bg, bg_rect)

    for p_data in particles[:]:
        p_data[0][0] += p_data[1][0] * dt
        p_data[0][1] += p_data[1][1] * dt
        p_data[2] -= 600 * dt
        if p_data[2] <= 0: particles.remove(p_data)
        else:
            p_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (200, 200, 200, int(p_data[2])), (3, 3), 3)
            game_canvas.blit(p_surf, (p_data[0][0]-3, p_data[0][1]-3))

    if game_started:
        if button_alpha > 0: button_alpha = max(0, button_alpha - 400 * dt)
        
        if dice_rolling:
            dice_timer -= dt
            dice_frame_timer += dt
            if dice_frame_timer >= 0.1:
                dice_frame_index = (dice_frame_index + 1) % 6
                dice_frame_timer = 0
                if dice_roll_snd: dice_roll_snd.play()
            
            if dice_timer <= 0:
                dice_rolling = False
                if dice_finish_snd: dice_finish_snd.play()
                final_dice_val = rdm.randint(1, 6)
                dice_frame_index = final_dice_val - 1
                
                sx, sy = 0, 0
                if abs(target_dir[0]) > abs(target_dir[1]):
                    sx = block_size if target_dir[0] > 0 else -block_size
                else:
                    sy = block_size if target_dir[1] > 0 else -block_size
                
                tx, ty = current_x, current_y
                for _ in range(final_dice_val):
                    nx = max(PLAYER_MARGIN, min(tx + sx, SCREEN_WIDTH - player_rect.width - PLAYER_MARGIN))
                    ny = max(PLAYER_MARGIN, min(ty + sy, SCREEN_HEIGHT - player_rect.height - PLAYER_MARGIN))
                    if (nx, ny) != (tx, ty):
                        move_queue.append((nx, ny))
                        tx, ty = nx, ny

        is_moving = len(move_queue) > 0
        bounce, j_scale = 0, 1.0
        
        if is_moving:
            tx, ty = move_queue[0]
            dx, dy = tx - current_x, ty - current_y
            curr_d = math.sqrt(dx**2 + dy**2)
            prog = 1.0 - (curr_d / block_size if block_size != 0 else 0)
            bounce = math.sin(prog * math.pi) * 12
            j_scale = 1.0 + (math.sin(prog * math.pi) * 0.05)
            
            step = speed * dt
            if curr_d <= step:
                current_x, current_y = move_queue.pop(0)
                last_target_x, last_target_y = current_x, current_y
                if move_sound: move_sound.play()
                for _ in range(8):
                    particles.append([[current_x + 37, current_y + 75], [rdm.uniform(-80, 80), rdm.uniform(-40, 10)], 255])
            else:
                ang = math.atan2(dy, dx)
                current_x += math.cos(ang) * step
                current_y += math.sin(ang) * step

        player_rect.topleft = (current_x, current_y)
        player_target_scale = 1.15 if (is_moving or pawn_is_selected or dice_rolling) else (1.08 if is_hovering_player else 1.0)
        player_current_scale += (player_target_scale - player_current_scale) * 12 * dt

        scaled_p = pygame.transform.scale(player_src, (int(15*stud*player_current_scale*j_scale), int(15*stud*player_current_scale*j_scale)))
        game_canvas.blit(scaled_p, scaled_p.get_rect(center=player_rect.center).move(0, -bounce))

        if show_dice:
            dice_draw_rect = dice_images[dice_frame_index].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
            game_canvas.blit(dice_images[dice_frame_index], dice_draw_rect)

    if button_alpha > 0:
        button_current_scale += ((1.08 if is_hovering_btn else 1.0) - button_current_scale) * 10 * dt
        s_btn = pygame.transform.scale(play_button_src, (int(290*button_current_scale), int(100*button_current_scale)))
        r_btn = pygame.transform.rotate(s_btn, math.sin(time_ms * 0.005) * 3)
        r_btn.set_alpha(button_alpha)
        game_canvas.blit(background_art, bga_rect)
        game_canvas.blit(r_btn, r_btn.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        game_canvas.blit(game_title, game_title_rect)

    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.smoothscale(game_canvas, (int(SCREEN_WIDTH * scale), int(SCREEN_HEIGHT * scale))), (offset_x, offset_y))
    pygame.display.flip()

pygame.quit()
