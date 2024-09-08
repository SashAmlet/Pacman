import pygame
import board

pygame.init()

WIDTH = 700
HEIGHT = 750

ROWS = COLS = 20

counter = 0
flicker = False

pixel_w = (WIDTH // COLS)
pixel_h = ((HEIGHT - 50) // ROWS)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)

level = board.get_maze(COLS, ROWS)
color = 'blue'

direction = 0
player_x = 0
player_y = pixel_h
# R, L, U, D
turns_allowed = [False, False, False, False]
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (pixel_w, pixel_h)))

def draw_board():
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.rect(screen, color, (j * pixel_w, i * pixel_h, pixel_w, pixel_h))
            if level[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * pixel_w + (0.5 * pixel_w), i * pixel_h + (0.5 * pixel_h)), 4)
            if level[i][j] == 3:
                pygame.draw.circle(screen, 'white', (j * pixel_w + (0.5 * pixel_w), i * pixel_h + (0.5 * pixel_h)), 10)

def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


run = True
while run:
    timer.tick(fps)

    if counter < 19:
        counter += 1
        if counter > 1:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill('black')
    draw_board()
    draw_player()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 1
            if event.key == pygame.K_UP:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3

    pygame.display.flip() 

pygame.quit()