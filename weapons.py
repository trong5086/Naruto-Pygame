#Import thư viện
import pygame
#Lớp shuriken
class Weapons:
    #Hàm khởi tạo
    #Input: Tọa độ x,y, Kích thước WxH của shuriken, phía mà shuriken sẽ bay tới
    #Output: Không có
    def __init__(self, X = 50, Y = 400, W = 40, H = 60, F = 1):
        self.x = X
        self.y = Y
        self.width = W 
        self.height = H
        self.facing = F
        #Vận tốc bay của shuriken
        self.vel = 23 * self.facing
        self.hitbox = (self.x, self.y , 40, 40)  

    #Hàm vẽ shuriken
    #Input: Màn hình game chính
    #Output: Không có  
    def draw(self, DISPLAYSURF):
        DISPLAYSURF.blit(pygame.image.load('./assets/images/—Pngtree—shuriken ninja kunai st.png'),(self.x, self.y))
        self.hitbox = (self.x, self.y, 40, 40)
        