import config as g
import pygame
from collections import deque
import random

pygame.init()

class Ghost:
     def __init__(self, id, coords, speed, img, direction, dead, box):
          self.id = id
          self.coords = coords
          self.center = [coords[0] + g.pixel_w // 2 + 1, coords[1] + g.pixel_h // 2 + 1]
          self.img = img
          self.direction = direction
          self.dead = dead
          self.in_box = box   

          if g.powerup and not g.eaten_ghosts[self.id]:
               self.speed = speed // 2
          else:
               self.speed = speed

          self.turns, self.in_box = self.check_collisions()
          self.rect = self.draw()

          if not self.dead:
               self.move()
          elif self.dead and self.in_box:
               g.ghosts_box[self.id] = True
               g.ghosts_dead[self.id] = False
               g.gh_moving[self.id] = False
               g.gh_stop_timer[self.id] = 3*60
               g.eaten_ghosts[self.id] = True
               g.ghosts_direction[self.id] = 2
          else:
               g.ghosts_coords[self.id] = g.init_ghosts_coords()[self.id]

     def draw(self):
          #print(g.powerup)
          if not self.dead and ((not g.powerup) or (g.powerup and g.eaten_ghosts[self.id])):
               g.screen.blit(self.img, (self.coords[0], self.coords[1]))
          elif g.powerup and not self.dead and not g.eaten_ghosts[self.id]: # powerup
               g.screen.blit(g.ghosts_images[4], (self.coords[0], self.coords[1]))
          else: # dead
               g.screen.blit(g.ghosts_images[5], (self.coords[0], self.coords[1]))

          ghost_rect = pygame.rect.Rect((self.coords[0], self.coords[1]), (g.pixel_w, g.pixel_h))
          return ghost_rect
               
     def draw_path(self):
          for coord in self.path:
               pygame.draw.circle(g.screen, 'red', (coord[0] * g.pixel_w + (0.5 * g.pixel_w), coord[1] * g.pixel_h + (0.5 * g.pixel_h)), 3)


     def check_collisions(self):
          # R, L, U, D
          turns = [False, False, False, False]
          centerx = self.center[0]
          centery = self.center[1]
          boarders = [1, 5, 4]

               
          # In this case he is allowed to be in the box
          additional_condition = self.in_box or self.dead
          # print(self.in_box, ' ', self.dead, ' ', additional_condition)

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
                    if g.in_the_middle_of_the_cell(self.coords, by_X=True): # if the player is in the center of the square relative to the X axis
                         index_value = g.level[(centery + g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]
                         if index_value not in boarders  or index_value == 4 and additional_condition:
                              turns[3] = True
                         index_value = g.level[(centery - g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[2] = True

                    # Can I turn Left or Right?
                    if g.in_the_middle_of_the_cell(self.coords, by_Y=True): # if the player is in the center of the square relative to the Y axis
                         index_value = g.level[centery // g.pixel_h][(centerx - g.pixel_w//2) // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[1] = True
                         index_value = g.level[centery // g.pixel_h][(centerx + g.pixel_w//2) // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[0] = True

               
               # If I am already moving Left or Right 
               if g.direction == 1 or g.direction == 0:
                    # Can I continue moving in the same direction?
                    if g.in_the_middle_of_the_cell(self.coords, by_Y=True): # if the player is in the center of the square relative to the Y axis
                         index_value = g.level[centery // g.pixel_h][(centerx + g.pixel_w//2) // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[0] = True
                         index_value = g.level[centery // g.pixel_h][(centerx - g.pixel_w//2) // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[1] = True

                    # Can I turn Up or Down?
                    if g.in_the_middle_of_the_cell(self.coords, by_X=True): # if the player is in the center of the square relative to the X axis
                         index_value = g.level[(centery - g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[2] = True
                         index_value = g.level[(centery + g.pixel_h//2) // g.pixel_h][centerx // g.pixel_w]
                         if index_value not in boarders or index_value == 4 and additional_condition:
                              turns[3] = True
          else:
               turns[0] = turns[1] = True


          # Is the ghost still in the box?

          maze_coords = g.coords_to_maze(self.coords)
          center_row = g.ROWS // 2
          center_col = g.COLS // 2
          if maze_coords[0] in range(center_row-1, center_row+1) and \
               maze_coords[1] in range(center_col-2, center_col+1):
               g.ghosts_box[self.id] = True
          else:
               g.ghosts_box[self.id] = False

          


          return turns, g.ghosts_box[self.id]
     
     

     def random_true_index(self):
          true_indices = [index for index, value in enumerate(self.turns) if value]
          if not true_indices:
               return None  # If there are no True values, return None
          return random.choice(true_indices)

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
          maze_p_coords = (0, 0)
          maze_r_coords = (0, 0)

          # If the ghost died, the center of the the player will be its spawn point.
          
          maze_p_coords = ((g.player_coords[0] + g.pixel_h // 2 + 1)//g.pixel_h, (g.player_coords[1] + g.pixel_w // 2 + 1)//g.pixel_w)

          x, y = g.COLS-maze_p_coords[0]-1, g.ROWS-maze_p_coords[1]-1
          if is_valid_move(x, y):
               maze_r_coords = (x, y)
          else:
               for dx, dy in full_directions:
                    nx, ny = x + dx, y + dy
                         
                    if is_valid_move(nx, ny):
                         maze_r_coords = (nx, ny)
                         break

          if g.powerup and not g.eaten_ghosts[self.id]:
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


          if g.gh_moving[self.id] == True:
               # print('Direction: ', g.ghosts_direction[self.id])
               # print('Allowed turns:', self.turns)
               if not self.turns[g.ghosts_direction[self.id]]: # If it is not possible to travel in this direction, then we choose a new permitted direction
                    g.ghosts_direction[self.id] = self.random_true_index()
                    
                    
               if g.ghosts_direction[self.id] == 0:
                    g.ghosts_coords[self.id][0] += self.speed
               elif g.ghosts_direction[self.id] == 1:
                    g.ghosts_coords[self.id][0] -= self.speed
               elif g.ghosts_direction[self.id] == 2:
                    g.ghosts_coords[self.id][1] -= self.speed
               elif g.ghosts_direction[self.id] == 3:
                    g.ghosts_coords[self.id][1] += self.speed


     
     def move_patrol(self):

          def decision(probability):
               if 1 <= random.randint(1, 100) <= probability:
                    return True
               else:
                    return False

          # I change direction only if the ghost is in the middle of the cell and 
          # either there is a wall in front of it or a decision is made to turn.
          # print(self.id)
          # print(g.ghosts_direction)
          if self.in_box:
               decision_ = False
          else:
               decision_ = decision(10)

          if g.in_the_middle_of_the_cell(self.coords, by_X=True, by_Y=True) and \
                    (self.turns[g.ghosts_direction[self.id]] == False or decision_):

               g.ghosts_direction[self.id] = self.random_true_index()
               

          if g.gh_moving[self.id] == True:
               if g.ghosts_direction[self.id] == 0:
                    g.ghosts_coords[self.id][0] += self.speed
               elif g.ghosts_direction[self.id] == 1:
                    g.ghosts_coords[self.id][0] -= self.speed
               elif g.ghosts_direction[self.id] == 2:
                    g.ghosts_coords[self.id][1] -= self.speed
               elif g.ghosts_direction[self.id] == 3:
                    g.ghosts_coords[self.id][1] += self.speed

     
     def move(self):
          def bresenham_line(coords1, coords2):
               x1 = coords1[0]
               y1 = coords1[1]
               x2 = coords2[0]
               y2 = coords2[1]
               
               points = []
               dx = abs(x2 - x1)
               dy = abs(y2 - y1)
               sx = 1 if x1 < x2 else -1
               sy = 1 if y1 < y2 else -1
               err = dx - dy
               
               while True:
                    points.append((x1, y1))
                    if x1 == x2 and y1 == y2:
                         break
                    e2 = 2 * err
                    if e2 > -dy:
                         err -= dy
                         x1 += sx
                    if e2 < dx:
                         err += dx
                         y1 += sy
               
               return points

          def can_see(matrix, coords1, coords2):               
               x1 = coords1[0]
               y1 = coords1[1]
               x2 = coords2[0]
               y2 = coords2[1]

               line_of_sight = bresenham_line(coords1, coords2)
               
               for (x, y) in line_of_sight:
                    # Проверяем, является ли клетка стеной
                    if matrix[y][x] == 1:
                         return False  # Видимость блокирована стеной
               
               return True  # Если нет стен на пути, объект виден
          
          maze_g_coords = (g.coords_to_maze(self.coords))
          maze_p_coords = (g.coords_to_maze(g.player_coords))
          
          if 0 <= maze_p_coords[0] < g.ROWS and 0 <= maze_p_coords[1] < g.COLS:
               see = can_see(g.level, maze_g_coords, maze_p_coords)
          else:
               see = False

          if see:
               g.he_sees_you[self.id] = 3*60
          elif g.he_sees_you[self.id] > 0:
               g.he_sees_you[self.id] -= 1

          if g.he_sees_you[self.id] == 0:
               self.move_patrol()
          else:
               self.move_chaser()
               if self.path is not None and g.show_path:
                    self.draw_path()