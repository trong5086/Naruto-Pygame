import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Naruto')
moveRight = [pygame.image.load('./assets/images/RRUN_1.png'),pygame.image.load('./assets/images/RRUN_2.png'),pygame.image.load('./assets/images/RRUN_3.png'),pygame.image.load('./assets/images/RRUN_4.png'),pygame.image.load('./assets/images/RRUN_5.png'),pygame.image.load('./assets/images/RRUN_6.png')]
moveLeft = [pygame.image.load('./assets/images/LRUN_1.png'),pygame.image.load('./assets/images/LRUN_2.png'),pygame.image.load('./assets/images/LRUN_3.png'),pygame.image.load('./assets/images/LRUN_4.png'),pygame.image.load('./assets/images/LRUN_5.png'),pygame.image.load('./assets/images/LRUN_6.png')]
jumpLeft = pygame.image.load('./assets/images/LJUMP.png')
jumpRight = pygame.image.load('./assets/images/RJUMP.png')
guardLeft = pygame.image.load('./assets/images/LGUARD.png')
guardRight = pygame.image.load('./assets/images/RGUARD.png')
bg = pygame.image.load('./assets/backgrounds/background.png')
stand = pygame.image.load('./assets/images/STAND.png')
Clock = pygame.time.Clock()
class Player():
    def __init__(self, X = 50, Y = 500, W = 40, H = 60):
        self.x = X
        self.y = Y
        self.width = W 
        self.height = H
        self.speed = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.isJump = False
        self.jumpHeight = 7.5
        # self.isGuard = False
        self.isStanding = True
    def draw(self, DISPLAYSURF):
        if self.walkCount + 1 > 12:
            self.walkCount = 0
        if not(self.isStanding):
            if self.right:
                # if self.isGuard == False:
                    DISPLAYSURF.blit(moveRight[self.walkCount//2],(self.x, self.y))
                    self.walkCount+=1
                # else:
                    # DISPLAYSURF.blit(guardRight,(self.x, self.y))  
            elif self.left:
                # if self.isGuard == False:
                    DISPLAYSURF.blit(moveLeft[self.walkCount//2],(self.x, self.y))
                    self.walkCount+=1
                # else:
                    # DISPLAYSURF.blit(guardLeft,(self.x, self.y))
        else:
            if self.right:
                if self.isJump:
                    DISPLAYSURF.blit(jumpRight,(self.x, self.y))
                else:
                    DISPLAYSURF.blit(stand,(self.x,self.y))
            else:
                if self.isJump:
                    DISPLAYSURF.blit(jumpLeft,(self.x, self.y))
                else:
                    DISPLAYSURF.blit(stand,(self.x,self.y))
            # if self.isGuard == True:
            #     DISPLAYSURF.blit(guardRight,(self.x, self.y))
            # else:
            #     DISPLAYSURF.blit(stand,(self.x,self.y))
       
# class Weapons():
#     def __init__(self, X = 50, Y = 500, W = 40, H = 60):
#         self.x = X
#         self.y = Y
#         self.width = W 
#         self.height = H
#     def draw(self, DISPLAYSURF):

# Hàm dùng để gắn background cũng như tạo loạt ảnh di chuyển cho nhân vật
def drawGameWithImage():
    DISPLAYSURF.blit(bg,(0,0))
    itachi.draw(DISPLAYSURF)
    pygame.display.update()
itachi = Player()
BoundLeft = itachi.speed # Biên trái 
BoundRight = 750 - itachi.width - itachi.speed - 2 # Biên phải
running = True
while running:
    pygame.time.delay(50)
    # Bắt sự kiện trong game
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
   
    # Bắt nút đang được nhấn bởi người dùng
    keys = pygame.key.get_pressed()
    # Khi người dùng chọn nút di di chuyển trái
    if keys[pygame.K_LEFT] and itachi.x > BoundLeft:
        itachi.x -= itachi.speed
        itachi.left = True
        itachi.right = False
        itachi.isStanding = False
    # Khi người dùng chọn nút di di chuyển phải
    elif keys[pygame.K_RIGHT] and itachi.x < BoundRight: 
        itachi.x += itachi.speed
        itachi.left = False
        itachi.right = True
        itachi.isStanding = False
    else:
        itachi.walkCount = 0
        itachi.isStanding = True
    # Khi người dùng chọn nút cách (Space)
    if itachi.isJump == False :
        if keys[pygame.K_SPACE]:
            itachi.isJump = True
            itachi.left = False
            itachi.right = False
            itachi.walkCount = 0
    else:
        if itachi.jumpHeight >= -7.5:
            temp = 2.5
            if itachi.jumpHeight < 0:
                temp = -2.5
            itachi.y -= (itachi.jumpHeight ** 2) * 0.5 * temp
            itachi.jumpHeight -= 1
        else:
            itachi.isJump = False
            itachi.jumpHeight = 7.5
    # if itachi.isGuard == False :
    #     if keys[pygame.K_f]:
    #         itachi.isGuard = True
    # else:
    #     if keys[pygame.K_f]:
    #         itachi.isGuard = True
    #         itachi.walkCount = 0
    #     else:
    #         itachi.isGuard = False
    print(itachi.right,itachi.isJump)
    drawGameWithImage()
pygame.quit()
sys.exit()