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
p_moving = False

player_images = []
for i in range(1, 5):
    image_path = f'assets/player_images/{i}.png'
    player_images.append(pygame.transform.scale(pygame.image.load(image_path), (pixel_w, pixel_h)))




### GHOSTS ###

# red, blue, orange, pink
def init_ghosts_coords():
    ghosts_coords = [
        [(ROWS // 2)*pixel_w, (COLS // 2)*pixel_h],
        [(ROWS // 2-1)*pixel_w, (COLS // 2)*pixel_h],
        [(ROWS // 2)*pixel_w, (COLS // 2-1)*pixel_h],
        [(ROWS // 2-1)*pixel_w, (COLS // 2-1)*pixel_h]
    ]
    return ghosts_coords

ghosts_coords = init_ghosts_coords()

ghosts_direction = [2, 2, 2, 2]
ghosts_dead = [False, False, False, False]
ghosts_box = [True, True, True, True]
ghost_speed = 2
gh_moving = [False, False, False, False]
gh_stop_timer = [0, 0, 0, 0]

ghosts_images = []
for i in range(0, 6):
    image_path = f'assets/ghost_images/{i}.png'
    scaled_image = pygame.transform.scale(pygame.image.load(image_path), (pixel_w, pixel_h))
    ghosts_images.append(scaled_image)



### General settings ###

powerup = False
power_counter = 0
eaten_ghosts = [False, False, False, False]
startup_counter = 0

he_sees_you = [0, 0, 0, 0]

show_path = True


# takes the coordinate of the object, returns its position on the map.
# including the left and upper borders.
def coords_to_maze(coords):
    center_x = coords[0] + pixel_w // 2 + 1
    center_y = coords[1] + pixel_h // 2 + 1

    return center_x//pixel_h, center_y//pixel_w

def in_the_middle_of_the_cell(coords, by_X = False, by_Y = False, fluff = 3):
    center_x = coords[0] + pixel_w // 2 + 1
    center_y = coords[1] + pixel_h // 2 + 1
    
    pixel_X_center = pixel_w // 2
    pixel_Y_center = pixel_h // 2

    if by_X and by_Y:
        response =  (pixel_X_center - fluff <= center_x % pixel_w <= pixel_X_center + fluff) and \
                    (pixel_Y_center - fluff <= center_y % pixel_h <= pixel_Y_center + fluff)
    elif by_X:
        response =  (pixel_X_center - fluff <= center_x % pixel_w <= pixel_X_center + fluff)
    elif by_Y:
        response =  (pixel_Y_center - fluff <= center_y % pixel_h <= pixel_Y_center + fluff)
    else:
        return None

    
    return response
