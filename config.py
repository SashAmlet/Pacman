import pygame
import board

pygame.init()

WIDTH = 700
HEIGHT = 750

ROWS = COLS = 20


pixel_w = (WIDTH // COLS)
pixel_h = ((HEIGHT - 50) // ROWS)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font('freesansbold.ttf', 20)

level = board.get_maze(COLS, ROWS)
print(level)
color = 'blue'

### PLAYER ###

direction = 0 # Actual movement of pacman
direction_command = 0 # Command coming from the user
player_coords = [0, pixel_h] # x, y
# R, L, U, D
turns_allowed = [False, False, False, False]
player_speed = 2
score = 0
lives = 3

player_images = []
for i in range(1, 5):
    image_path = f'assets/player_images/{i}.png'
    player_images.append(pygame.transform.scale(pygame.image.load(image_path), (pixel_w, pixel_h)))




### GHOSTS ###

# red, blue, orange, pink
ghosts_coords = [
    [(ROWS // 2)*pixel_w, (COLS // 2)*pixel_h],
    [(ROWS // 2-1)*pixel_w, (COLS // 2)*pixel_h],
    [(ROWS // 2)*pixel_w, (COLS // 2-1)*pixel_h],
    [(ROWS // 2-1)*pixel_w, (COLS // 2-1)*pixel_h]
]
ghosts_direction = [2, 2, 2, 2]
ghosts_targets = [player_coords, player_coords, player_coords, player_coords]
ghosts_dead = [False, False, False, False]
ghosts_box = [True, True, True, True]
ghost_speed = 2

ghosts_images = []
for i in range(0, 6):
    image_path = f'assets/ghost_images/{i}.png'
    scaled_image = pygame.transform.scale(pygame.image.load(image_path), (pixel_w, pixel_h))
    ghosts_images.append(scaled_image)



### General settings ###

powerup = False
power_counter = 0
eaten_ghosts = [False, False, False, False]
moving = False

he_sees_you = 0