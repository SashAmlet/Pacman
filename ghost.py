import config as g
import pygame
from collections import deque
import random

pygame.init()

class Ghost:
     def __init__(self, id, coords, target, speed, img, direction, dead, box):
          self.id = id
          self.coords = coords
          self.center = [coords[0] + g.pixel_w // 2 + 1, coords[1] + g.pixel_h // 2 + 1]
          self.target = target
          self.speed = speed
          self.img = img
          self.direction = direction
          self.dead = dead
          self.in_box = box   
          self.turns, self.in_box = self.check_collisions()
          self.rect = self.draw()

          # self.move_chaser()
          self.move_patrol()
          
          # if self.path is not None:
          #      self.draw_path()

     def draw(self):
          #print(g.powerup)
          if not self.dead and ((not g.powerup) or (g.powerup and g.eaten_ghosts[self.id])):
               g.screen.blit(self.img, (self.coords[0], self.coords[1]))
          elif g.powerup and not self.dead and not g.eaten_ghosts[self.id]: # powerup
               g.screen.blit(g.ghosts_images[4], (self.coords[0], self.coords[1]))
          else: # dead
               g.screen.blit(g.ghosts_images[5], (self.coords[0], self.coords[1]))

          ghost_rect = pygame.rect.Rect((self.center[0] - 18, self.center[1] - 18), (36, 36))
          return ghost_rect
               
     def draw_path(self):
          for coord in self.path:
               pygame.draw.circle(g.screen, 'red', (coord[0] * g.pixel_w + (0.5 * g.pixel_w), coord[1] * g.pixel_h + (0.5 * g.pixel_h)), 3)


     def check_collisions(self):
          # R, L, U, D
          turns = [False, False, False, False]
          centerx = self.center[0]
          centery = self.center[1]
          boarders = [1, 5]
          # In this case he is allowed to be in the box
          additional_condition = self.in_box or self.dead

          if g.pixel_w < centerx < g.WIDTH-g.pixel_w:
               # If we are going to the right, then obviously we can turn left (since that's where we are going). 
               # The check is needed to avoid sliding the walls when we are stuck to the right and quickly press the "left", "right" keys
               if self.direction == 0:
                    index_value = g.level[centery // g.pixel_h][(centerx - g.pixel_w) // g.pixel_w]
                    if  index_value not in boarders or index_value == 4 and additional_condition:
                              turns[1] = True
               if g.direction == 1:
                    index_value = g.level[centery // g.pixel_h][(centerx + g.pixel_w) // g.pixel_w]
                    if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[0] = True
               if g.direction == 2:
                    index_value = g.level[(centery + g.pixel_h) // g.pixel_h][centerx // g.pixel_w]
                    if index_value not in boarders or index_value == 4 and additional_condition:
                         turns[3] = True
               if g.direction == 3:
                    index_value = g.level[(centery - g.pixel_h) // g.pixel_h][centerx // g.pixel_w]
                    if index_value not in boarders or index_value == 4 and additional_condition:
                         turns[2] = True

               pixel_X_center = g.pixel_w // 2
               pixel_Y_center = g.pixel_h // 2

               # If I am already moving Up or Down 
               if g.direction == 2 or g.direction == 3:
                    # Can I continue moving in the same direction?
                    if pixel_X_center - 3 <= centerx % g.pixel_w <= pixel_X_center + 3: # if the player is in the center of the square relative to the X axis
                         index_value = g.level[(centery + g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]
                         if index_value not in boarders  or index_value == 4 and additional_condition:
                              turns[3] = True
                         index_value = g.level[(centery - g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[2] = True

                    # Can I turn Left or Right?
                    if pixel_Y_center - 3 <= centery % g.pixel_h <= pixel_Y_center + 3: # if the player is in the center of the square relative to the Y axis
                         index_value = g.level[centery // g.pixel_h][(centerx - g.pixel_w//2) // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[1] = True
                         index_value = g.level[centery // g.pixel_h][(centerx + g.pixel_w//2) // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[0] = True

               
               # If I am already moving Left or Right 
               if g.direction == 1 or g.direction == 0:
                    # Can I continue moving in the same direction?
                    if pixel_Y_center - 3 <= centery % g.pixel_h <= pixel_Y_center + 3: # if the player is in the center of the square relative to the Y axis
                         index_value = g.level[centery // g.pixel_h][(centerx + g.pixel_w//2) // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[0] = True
                         index_value = g.level[centery // g.pixel_h][(centerx - g.pixel_w//2) // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[1] = True

                    # Can I turn Up or Down?
                    if pixel_X_center - 3 <= centerx % g.pixel_w <= pixel_X_center + 3: # if the player is in the center of the square relative to the X axis
                         index_value = g.level[(centery - g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[2] = True
                         index_value = g.level[(centery + g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[3] = True
          else:
               turns[0] = turns[1] = True

          # Is the ghost still in the box?
          if (g.ROWS // 2 - 1)*g.pixel_w < self.coords[0] < (g.ROWS // 2)*g.pixel_w and \
               (g.COLS // 2 - 1)*g.pixel_h < self.coords[1] < (g.COLS // 2)*g.pixel_h:
               self.in_box = True
          else:
               self.in_box = False

          return turns, self.in_box
     


     def move_chaser(self):
          # R, L, U, D, LU, RU, LD, RD
          full_directions = [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

          def is_valid_move(x, y):
               rows, cols = len(g.level), len(g.level[0])
               return 0 <= x < rows and 0 <= y < cols and g.level[y][x] in {0, 2, 3, 4}
          
          def bfs(start, end):
               # R, L, U, D
               directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

               # Queue for BFS: each element is (x, y, path_to_this_point)
               queue = deque([(start[0], start[1], [])])
               visited = set()  # set of visited cells
               visited.add((start[0], start[1]))
               
               while queue:
                    x, y, path = queue.popleft()
                    
                    # If we have reached the end point, we return the path
                    if (x, y) == end:
                         return path + [(x, y)]
                    
                    # Check all the neighbors
                    for dx, dy in directions:
                         nx, ny = x + dx, y + dy
                         
                         if is_valid_move(nx, ny) and (nx, ny) not in visited:
                              queue.append((nx, ny, path + [(x, y)]))
                              visited.add((nx, ny))
               
               return None  # If there is no way

          # Coordinates of the center of the ghost and the player
          maze_g_coords = (self.center[0]//g.pixel_h, self.center[1]//g.pixel_w)
          maze_p_coords = ((g.player_coords[0] + g.pixel_h // 2 + 1)//g.pixel_h, (g.player_coords[1] + g.pixel_w // 2 + 1)//g.pixel_w)
          maze_r_coords = (0, 0)

          x, y = g.COLS-maze_p_coords[0]-1, g.ROWS-maze_p_coords[1]-1
          if is_valid_move(x, y):
               maze_r_coords = (x, y)
          else:
               for dx, dy in full_directions:
                    nx, ny = x + dx, y + dy
                         
                    if is_valid_move(nx, ny):
                         maze_r_coords = (nx, ny)
                         break

          if g.powerup:
               self.path = bfs(maze_g_coords, maze_r_coords)
          else:
               self.path = bfs(maze_g_coords, maze_p_coords)

          pixel_X_center = g.pixel_w // 2
          pixel_Y_center = g.pixel_h // 2

          # I change direction only if there is a path and a ghost in the middle of the cell
          if self.path is not None and len(self.path) > 1 and \
               (pixel_X_center - 3 <= self.center[0] % g.pixel_w <= pixel_X_center + 3) and \
                    (pixel_Y_center - 3 <= self.center[1] % g.pixel_h <= pixel_Y_center + 3):
               
               # R, L, U, D 
               direction = (self.path[1][0] - g.ghosts_coords[self.id][0]//g.pixel_w, self.path[1][1] - g.ghosts_coords[self.id][1]//g.pixel_h)
               if direction == (1, 0):
                    g.ghosts_direction[self.id] = 0
               elif direction == (-1, 0):
                    g.ghosts_direction[self.id] = 1
               elif direction == (0, -1):
                    g.ghosts_direction[self.id] = 2
               elif direction == (0, 1):
                    g.ghosts_direction[self.id] = 3

          if g.moving == True:
               if g.ghosts_direction[self.id] == 0:
                    g.ghosts_coords[self.id][0] += g.ghost_speed
               elif g.ghosts_direction[self.id] == 1:
                    g.ghosts_coords[self.id][0] -= g.ghost_speed
               elif g.ghosts_direction[self.id] == 2:
                    g.ghosts_coords[self.id][1] -= g.ghost_speed
               elif g.ghosts_direction[self.id] == 3:
                    g.ghosts_coords[self.id][1] += g.ghost_speed
     
     def move_patrol(self):

          pixel_X_center = g.pixel_w // 2
          pixel_Y_center = g.pixel_h // 2

          def random_true_index(turns):
               true_indices = [index for index, value in enumerate(turns) if value]
               if not true_indices:
                    return None  # If there are no True values, return None
               return random.choice(true_indices)

          def decision(probability):
               if 1 <= random.randint(1, 100) <= probability:
                    return True
               else:
                    return False

          # I change direction only if the ghost is in the middle of the cell and 
          # either there is a wall in front of it or a decision is made to turn.
          if (pixel_X_center - 3 <= self.center[0] % g.pixel_w <= pixel_X_center + 3) and \
               (pixel_Y_center - 3 <= self.center[1] % g.pixel_h <= pixel_Y_center + 3) and \
                    (self.turns[g.ghosts_direction[self.id]] == False or decision(10)):

               g.ghosts_direction[self.id] = random_true_index(self.turns)
               


          if g.moving == True:
               if g.ghosts_direction[self.id] == 0:
                    g.ghosts_coords[self.id][0] += g.ghost_speed
               elif g.ghosts_direction[self.id] == 1:
                    g.ghosts_coords[self.id][0] -= g.ghost_speed
               elif g.ghosts_direction[self.id] == 2:
                    g.ghosts_coords[self.id][1] -= g.ghost_speed
               elif g.ghosts_direction[self.id] == 3:
                    g.ghosts_coords[self.id][1] += g.ghost_speed

     
     