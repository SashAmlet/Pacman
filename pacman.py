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
print(level)
color = 'blue'

# direction command - command coming from the user, 
# direction - actual movement of pacman
direction = 0
direction_command = 0
player_x = 0
player_y = pixel_h
player_speed = 2
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

def check_collisions(centerx, centery):
    # R, L, U, D
    turns = [False, False, False, False]

    print(direction, ':', centerx//pixel_w, ';', center_y//pixel_h)

    if pixel_w < centerx < WIDTH-pixel_w:
        # If we are going to the right, then obviously we can turn left (since that's where we are going). 
        # The check is needed to avoid sliding the walls when we are stuck to the right and quickly press the "left", "right" keys
        if direction == 0:
            if level[centery // pixel_h][(center_x - pixel_w) // pixel_w] != 1:
                turns[1] = True
        if direction == 1:
            if level[centery // pixel_h][(center_x + pixel_w) // pixel_w] != 1:
                turns[0] = True
        if direction == 2:
            if level[(centery + pixel_h) // pixel_h][center_x // pixel_w] != 1:
                turns[3] = True
        if direction == 3:
            if level[(centery - pixel_h) // pixel_h][center_x // pixel_w] != 1:
                turns[2] = True

        pixel_X_center = pixel_w // 2
        pixel_Y_center = pixel_h // 2

        # If I am already moving Up or Down 
        if direction == 2 or direction == 3:
            # Can I continue moving in the same direction?
            if pixel_X_center - 3 <= centerx % pixel_w <= pixel_X_center + 3: # if the player is in the center of the square relative to the X axis
                if level[(centery + pixel_h//2) // pixel_h][centerx // pixel_w]  != 1:
                    turns[3] = True
                if level[(centery - pixel_h//2) // pixel_h][centerx // pixel_w]  != 1:
                    turns[2] = True

            # Can I turn Left or Right?
            if pixel_Y_center - 3 <= centery % pixel_h <= pixel_Y_center + 3: # if the player is in the center of the square relative to the Y axis
                if level[centery // pixel_h][(centerx - pixel_w//2) // pixel_w]  != 1:
                    turns[1] = True
                if level[centery // pixel_h][(centerx + pixel_w//2) // pixel_w]  != 1:
                    turns[0] = True

        
        # If I am already moving Left or Right 
        if direction == 1 or direction == 0:
            # Can I continue moving in the same direction?
            if pixel_Y_center - 3 <= centery % pixel_h <= pixel_Y_center + 3: # if the player is in the center of the square relative to the Y axis
                if level[centery // pixel_h][(centerx + pixel_w//2) // pixel_w]  != 1:
                    turns[0] = True
                if level[centery // pixel_h][(centerx - pixel_w//2) // pixel_w]  != 1:
                    turns[1] = True

            # Can I turn Up or Down?
            if pixel_X_center - 3 <= centerx % pixel_w <= pixel_X_center + 3: # if the player is in the center of the square relative to the X axis
                if level[(centery - pixel_h//2) // pixel_h][centerx // pixel_w]  != 1:
                    turns[2] = True
                if level[(centery + pixel_h//2) // pixel_h][centerx // pixel_w]  != 1:
                    turns[3] = True
    else:
        turns[0] = turns[1] = True

    print(turns)

    return turns

def move_player(play_x, play_y):
    # R, L, U, D
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    elif direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed

    return play_x, play_y



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
    center_x = player_x + pixel_w // 2 + 1
    center_y = player_y + pixel_h // 2 + 1
    # pygame.draw.circle(screen, 'white', (center_x, center_y), 2)
    turns_allowed = check_collisions(center_x, center_y)
    player_x, player_y = move_player(player_x, player_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = 0
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = 1
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = 2
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = 3

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i

    if player_x > WIDTH:
        player_x = -pixel_w//2
    elif player_x < -pixel_w//2:
        player_x = WIDTH

    pygame.display.flip() 

pygame.quit()