import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smooth Movement")

screen_color = (255, 255, 255)

PLAYER_MARGIN = 30

stud = 5
block_size = 10 * stud

player_size = (10 * stud, 10 * stud)

player_img = "assets/player.png"
player = pygame.transform.scale(
    pygame.image.load(player_img).convert_alpha(),
    player_size
)

clock = pygame.time.Clock()

p_x = 0.0
p_y = 0.0

target_x = 0.0
target_y = 0.0

speed = 250

run = True
while run:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if p_x == target_x and p_y == target_y:
                if event.key == pygame.K_RIGHT:
                    target_x += block_size
                elif event.key == pygame.K_LEFT:
                    target_x -= block_size
                elif event.key == pygame.K_UP:
                    target_y -= block_size
                elif event.key == pygame.K_DOWN:
                    target_y += block_size

                target_x = max(0, min(target_x, SCREEN_WIDTH - player_size[0]))
                target_y = max(0, min(target_y, SCREEN_HEIGHT - player_size[1]))


    if p_x < target_x:
        p_x += speed * dt
        if p_x > target_x:
            p_x = target_x
    elif p_x > target_x:
        p_x -= speed * dt
        if p_x < target_x:
            p_x = target_x

    if p_y < target_y:
        p_y += speed * dt
        if p_y > target_y:
            p_y = target_y
    elif p_y > target_y:
        p_y -= speed * dt
        if p_y < target_y:
            p_y = target_y

    screen.fill(screen_color)
    screen.blit(player, (round(p_x), round(p_y)))
    pygame.display.update()

pygame.quit()