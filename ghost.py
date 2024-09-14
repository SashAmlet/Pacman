import config as g
import pygame

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
        self.box = box   
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        print(g.powerup)
        if not self.dead and ((not g.powerup) or (g.powerup and g.eaten_ghosts[self.id])):
             g.screen.blit(self.img, (self.coords[0], self.coords[1]))
        elif g.powerup and not self.dead and not g.eaten_ghosts[self.id]: # powerup
             g.screen.blit(g.ghosts_images[4], (self.coords[0], self.coords[1]))
        else: # dead
             g.screen.blit(g.ghosts_images[5], (self.coords[0], self.coords[1]))

        ghost_rect = pygame.rect.Rect((self.center[0] - 18, self.center[1] - 18), (36, 36))
        return ghost_rect
        
    def check_collisions(self):
         self.turns = [False, False, False, False]
         self.in_box = True
         return self.turns, self.in_box