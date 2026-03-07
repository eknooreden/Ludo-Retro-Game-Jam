import pygame
import math

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ludo Adventures")

screen_color = (255, 255, 255)
PLAYER_MARGIN = 30
stud = 5
block_size = 17 * stud

hover_sound = pygame.mixer.Sound("assets/sounds/hover.wav")
move_sound = pygame.mixer.Sound("assets/sounds/pawn_move.wav")
was_hovering = False

play_button_img = "assets/main_menu/play_button.png"
button_base_w, button_base_h = 58 * stud, 20 * stud
play_button_src = pygame.image.load(play_button_img).convert_alpha()

button_current_scale = 1.0
button_target_scale = 1.0
button_alpha = 255
game_started = False

player_img = "assets/game/player/player_red.png"
player_base_w, player_base_h = 15 * stud, 15 * stud
player_src = pygame.transform.scale(
    pygame.image.load(player_img).convert_alpha(),
    (player_base_w, player_base_h)
)

player_current_scale = 1.0
player_target_scale = 1.0
player_is_clicked = False

clock = pygame.time.Clock()
player_rect = player_src.get_rect(topleft=(PLAYER_MARGIN, PLAYER_MARGIN))

target_x = float(player_rect.x)
target_y = float(player_rect.y)
speed = 250

run = True
while run:
    dt = clock.tick(60) / 1000.0
    time_ms = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    button_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    temp_btn_rect = pygame.Rect(0, 0, button_base_w, button_base_h)
    temp_btn_rect.center = button_center
    
    is_hovering_btn = temp_btn_rect.collidepoint(mouse_pos) and not game_started
    is_hovering_player = player_rect.collidepoint(mouse_pos) and game_started

    if is_hovering_btn and not was_hovering:
        hover_sound.play()
        was_hovering = True
    elif not is_hovering_btn:
        was_hovering = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_hovering_btn:
                game_started = True
            elif is_hovering_player:
                player_is_clicked = not player_is_clicked
        elif event.type == pygame.KEYDOWN and game_started:
            if player_rect.x == round(target_x) and player_rect.y == round(target_y):
                moved = False
                if event.key == pygame.K_RIGHT: target_x += block_size; moved = True
                elif event.key == pygame.K_LEFT: target_x -= block_size; moved = True
                elif event.key == pygame.K_UP: target_y -= block_size; moved = True
                elif event.key == pygame.K_DOWN: target_y += block_size; moved = True
                
                if moved:
                    move_sound.play()
                    target_x = max(PLAYER_MARGIN, min(target_x, SCREEN_WIDTH - player_rect.width - PLAYER_MARGIN))
                    target_y = max(PLAYER_MARGIN, min(target_y, SCREEN_HEIGHT - player_rect.height - PLAYER_MARGIN))

    screen.fill(screen_color)

    if game_started:
        if button_alpha > 0:
            button_alpha = max(0, button_alpha - 400 * dt)
        
        is_moving = player_rect.x != target_x or player_rect.y != target_y
        player_target_scale = 1.4 if is_moving else (1.2 if (is_hovering_player or player_is_clicked) else 1.0)
        player_current_scale += (player_target_scale - player_current_scale) * 12 * dt

        if player_rect.x < target_x: player_rect.x = min(target_x, player_rect.x + speed * dt)
        elif player_rect.x > target_x: player_rect.x = max(target_x, player_rect.x - speed * dt)
        if player_rect.y < target_y: player_rect.y = min(target_y, player_rect.y + speed * dt)
        elif player_rect.y > target_y: player_rect.y = max(target_y, player_rect.y - speed * dt)

        p_w = int(player_base_w * player_current_scale)
        p_h = int(player_base_h * player_current_scale)
        scaled_player = pygame.transform.scale(player_src, (p_w, p_h))
        screen.blit(scaled_player, scaled_player.get_rect(center=player_rect.center))

    if button_alpha > 0:
        button_target_scale = 1.08 if is_hovering_btn else 1.0
        button_current_scale += (button_target_scale - button_current_scale) * 10 * dt
        
        sway_angle = math.sin(time_ms * 0.005) * 3
        b_w = int(button_base_w * button_current_scale)
        b_h = int(button_base_h * button_current_scale)
        
        scaled_btn = pygame.transform.scale(play_button_src, (b_w, b_h))
        rotated_btn = pygame.transform.rotate(scaled_btn, sway_angle)
        rotated_btn.set_alpha(button_alpha)
        screen.blit(rotated_btn, rotated_btn.get_rect(center=button_center))
    
    pygame.display.update()

pygame.quit()
