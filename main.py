import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ludo Adventures")

screen_color = (255, 255, 255)

PLAYER_MARGIN = 30

stud = 5
block_size = 10 * stud

player_size = (15 * stud, 15 * stud)

player_img = "assets/game/player.png"
player = pygame.transform.scale(
    pygame.image.load(player_img).convert_alpha(),
    player_size
)

clock = pygame.time.Clock()

player_rect = player.get_rect(topleft=(PLAYER_MARGIN, PLAYER_MARGIN))

target_x = float(player_rect.x)
target_y = float(player_rect.y)

speed = 250

run = True
while run:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if player_rect.x == round(target_x) and player_rect.y == round(target_y):
                if event.key == pygame.K_RIGHT:
                    target_x += block_size
                elif event.key == pygame.K_LEFT:
                    target_x -= block_size
                elif event.key == pygame.K_UP:
                    target_y -= block_size
                elif event.key == pygame.K_DOWN:
                    target_y += block_size

                target_x = max(
                    PLAYER_MARGIN,
                    min(target_x, SCREEN_WIDTH - player_rect.width - PLAYER_MARGIN)
                )
                target_y = max(
                    PLAYER_MARGIN,
                    min(target_y, SCREEN_HEIGHT - player_rect.height - PLAYER_MARGIN)
                )

    current_x = float(player_rect.x)
    current_y = float(player_rect.y)

    if current_x < target_x:
        current_x += speed * dt
        if current_x > target_x:
            current_x = target_x
    elif current_x > target_x:
        current_x -= speed * dt
        if current_x < target_x:
            current_x = target_x

    if current_y < target_y:
        current_y += speed * dt
        if current_y > target_y:
            current_y = target_y
    elif current_y > target_y:
        current_y -= speed * dt
        if current_y < target_y:
            current_y = target_y

    player_rect.x = round(current_x)
    player_rect.y = round(current_y)

    screen.fill(screen_color)
    screen.blit(player, player_rect)
    pygame.display.update()

pygame.quit()