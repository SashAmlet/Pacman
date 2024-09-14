import pygame
import board
import config as g
from ghost import Ghost

pygame.init()


def draw_board(lvl):
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if lvl[i][j] == 1: # Wall
                pygame.draw.rect(g.screen, g.color, (j * g.pixel_w, i * g.pixel_h, g.pixel_w, g.pixel_h))
            if lvl[i][j] == 2: # Little treat
                pygame.draw.circle(g.screen, 'white', (j * g.pixel_w + (0.5 * g.pixel_w), i * g.pixel_h + (0.5 * g.pixel_h)), 4)
            if lvl[i][j] == 3: # Big treat
                pygame.draw.circle(g.screen, 'white', (j * g.pixel_w + (0.5 * g.pixel_w), i * g.pixel_h + (0.5 * g.pixel_h)), 10)

def draw_player(coords):
    x = coords[0]
    y = coords[1]
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if g.direction == 0:
        g.screen.blit(g.player_images[counter // 5], (x, y))
    elif g.direction == 1:
        g.screen.blit(pygame.transform.flip(g.player_images[counter // 5], True, False), (x, y))
    elif g.direction == 2:
        g.screen.blit(pygame.transform.rotate(g.player_images[counter // 5], 90), (x, y))
    elif g.direction == 3:
        g.screen.blit(pygame.transform.rotate(g.player_images[counter // 5], 270), (x, y))


def draw_miscellaneous():
    score_text = g.font.render(f'Score: {g.score}', True, 'white')
    g.screen.blit(score_text, (10, g.HEIGHT - 35))

    if g.powerup:
        pygame.draw.circle(g.screen, 'blue', (140, g.HEIGHT - 25), g.pixel_h//3)

    for i in range(g.lives):
        g.screen.blit(pygame.transform.scale(g.player_images[0], (g.pixel_w-g.pixel_w//3, g.pixel_h-g.pixel_h//3)), (500 + i*40, g.HEIGHT - 40))

def check_collisions(centerx, centery):
    # R, L, U, D
    turns = [False, False, False, False]
    barriers = [1, 4]

    #print(g.direction, ':', centerx//g.pixel_w, ';', center_y//g.pixel_h)

    if g.pixel_w < centerx < g.WIDTH-g.pixel_w:
        # If we are going to the right, then obviously we can turn left (since that's where we are going). 
        # The check is needed to avoid sliding the walls when we are stuck to the right and quickly press the "left", "right" keys
        if g.direction == 0:
            if g.level[centery // g.pixel_h][(center_x - g.pixel_w) // g.pixel_w] not in barriers:
                turns[1] = True
        if g.direction == 1:
            if g.level[centery // g.pixel_h][(center_x + g.pixel_w) // g.pixel_w] not in barriers:
                turns[0] = True
        if g.direction == 2:
            if g.level[(centery + g.pixel_h) // g.pixel_h][center_x // g.pixel_w] not in barriers:
                turns[3] = True
        if g.direction == 3:
            if g.level[(centery - g.pixel_h) // g.pixel_h][center_x // g.pixel_w] not in barriers:
                turns[2] = True

        pixel_X_center = g.pixel_w // 2
        pixel_Y_center = g.pixel_h // 2

        # If I am already moving Up or Down 
        if g.direction == 2 or g.direction == 3:
            # Can I continue moving in the same direction?
            if pixel_X_center - 3 <= centerx % g.pixel_w <= pixel_X_center + 3: # if the player is in the center of the square relative to the X axis
                if g.level[(centery + g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]  not in barriers:
                    turns[3] = True
                if g.level[(centery - g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]  not in barriers:
                    turns[2] = True

            # Can I turn Left or Right?
            if pixel_Y_center - 3 <= centery % g.pixel_h <= pixel_Y_center + 3: # if the player is in the center of the square relative to the Y axis
                if g.level[centery // g.pixel_h][(centerx - g.pixel_w//2) // g.pixel_w]  not in barriers:
                    turns[1] = True
                if g.level[centery // g.pixel_h][(centerx + g.pixel_w//2) // g.pixel_w]  not in barriers:
                    turns[0] = True

        
        # If I am already moving Left or Right 
        if g.direction == 1 or g.direction == 0:
            # Can I continue moving in the same direction?
            if pixel_Y_center - 3 <= centery % g.pixel_h <= pixel_Y_center + 3: # if the player is in the center of the square relative to the Y axis
                if g.level[centery // g.pixel_h][(centerx + g.pixel_w//2) // g.pixel_w]  not in barriers:
                    turns[0] = True
                if g.level[centery // g.pixel_h][(centerx - g.pixel_w//2) // g.pixel_w]  not in barriers:
                    turns[1] = True

            # Can I turn Up or Down?
            if pixel_X_center - 3 <= centerx % g.pixel_w <= pixel_X_center + 3: # if the player is in the center of the square relative to the X axis
                if g.level[(centery - g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]  not in barriers:
                    turns[2] = True
                if g.level[(centery + g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]  not in barriers:
                    turns[3] = True
    else:
        turns[0] = turns[1] = True

    #print(turns)

    return turns

def move_player(coords):
    # R, L, U, D
    if g.direction == 0 and g.turns_allowed[0]:
        coords[0] += g.player_speed
    elif g.direction == 1 and g.turns_allowed[1]:
        coords[0] -= g.player_speed
    elif g.direction == 2 and g.turns_allowed[2]:
        coords[1] -= g.player_speed
    elif g.direction == 3 and g.turns_allowed[3]:
        coords[1] += g.player_speed

    return coords

def check_score(centerx, centery, lvl, score, power, power_count, eaten_ghost):
    if g.pixel_w < centerx < g.WIDTH-g.pixel_w:
        if lvl[centery // g.pixel_h][centerx // g.pixel_w] == 2:
            score += 1
            lvl[centery // g.pixel_h][centerx // g.pixel_w] = 0
        elif lvl[centery // g.pixel_h][centerx // g.pixel_w] == 3:
            score += 10
            lvl[centery // g.pixel_h][centerx // g.pixel_w] = 0
            power = True
            power_count = 0
            eaten_ghost = [False, False, False, False]

    return score, power, power_count, eaten_ghost

### SETTINGS ###
counter = 0
fps = 60
flicker = False
timer = pygame.time.Clock()
run = True
startup_counter = 0
moving = False

while run:
    timer.tick(fps)
    # Timer part
    if counter < 19:
        counter += 1
        if counter > 1:
            flicker = False
    else:
        counter = 0
        flicker = True

    if startup_counter < 180: # For the first 3 seconds of the game, no one can move.
        startup_counter += 1
    else:
        moving = True
    
    if g.powerup and g.power_counter < 600:
        g.power_counter += 1
    elif g.powerup and g.power_counter >= 600:
        g.powerup = False
        g.power_counter = 0
        g.eaten_ghosts = [False, False, False, False]

    ##
    g.screen.fill('black')
    draw_board(g.level)
    draw_player(g.player_coords)
    red_ghost   = Ghost(0, g.ghosts_coords[0], g.ghosts_targets[0], g.ghost_speed, g.ghosts_images[0], g.ghosts_direction[0], g.ghosts_dead[0], g.ghosts_box[0])
    blue_ghost  = Ghost(1, g.ghosts_coords[1], g.ghosts_targets[1], g.ghost_speed, g.ghosts_images[1], g.ghosts_direction[1], g.ghosts_dead[1], g.ghosts_box[1])
    orange_ghost= Ghost(2, g.ghosts_coords[2], g.ghosts_targets[2], g.ghost_speed, g.ghosts_images[2], g.ghosts_direction[2], g.ghosts_dead[2], g.ghosts_box[2])
    pink_ghost  = Ghost(3, g.ghosts_coords[3], g.ghosts_targets[3], g.ghost_speed, g.ghosts_images[3], g.ghosts_direction[3], g.ghosts_dead[3], g.ghosts_box[3])
    draw_miscellaneous()

    center_x = g.player_coords[0] + g.pixel_w // 2 + 1
    center_y = g.player_coords[1] + g.pixel_h // 2 + 1

    g.turns_allowed = check_collisions(center_x, center_y)
    if moving:
        g.player_coords = move_player(g.player_coords)
    g.score, g.powerup, g.power_counter, g.eaten_ghosts = check_score(center_x, center_y, g.level, g.score, g.powerup, g.power_counter, g.eaten_ghosts)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                g.direction_command = 0
            if event.key == pygame.K_LEFT:
                g.direction_command = 1
            if event.key == pygame.K_UP:
                g.direction_command = 2
            if event.key == pygame.K_DOWN:
                g.direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and g.direction_command == 0:
                g.direction_command = 0
            if event.key == pygame.K_LEFT and g.direction_command == 1:
                g.direction_command = 1
            if event.key == pygame.K_UP and g.direction_command == 2:
                g.direction_command = 2
            if event.key == pygame.K_DOWN and g.direction_command == 3:
                g.direction_command = 3

    for i in range(4):
        if g.direction_command == i and g.turns_allowed[i]:
            g.direction = i

    if g.player_coords[0] > g.WIDTH:
        g.player_coords[0] = -g.pixel_w//2
    elif g.player_coords[0] < -g.pixel_w//2:
        g.player_coords[0] = g.WIDTH

    pygame.display.flip() 

pygame.quit()