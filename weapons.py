import pygame
class Weapons:
    def __init__(self, X = 50, Y = 400, W = 40, H = 60, F = 1):
        self.x = X
        self.y = Y
        self.width = W 
        self.height = H
        self.facing = F
        self.vel = 23 * self.facing
        self.hitbox = (self.x, self.y , 40, 40)  
        
    def draw(self, DISPLAYSURF):
        DISPLAYSURF.blit(pygame.image.load('./assets/images/—Pngtree—shuriken ninja kunai st.png'),(self.x, self.y))
        self.hitbox = (self.x, self.y, 40, 40)
        