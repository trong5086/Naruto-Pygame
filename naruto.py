import pygame, sys
from pygame.locals import *
from pyvidplayer import Video 

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
bgmenu = pygame.image.load('./assets/backgrounds/menubg.png')
bgm = pygame.mixer.music.load('./assets/musics/themesong.mp3')
hitsong = pygame.mixer.Sound('./assets/musics/hit.wav')
clicksong = pygame.mixer.Sound('./assets/musics/clickSound.wav')
shurikensong = pygame.mixer.Sound('./assets/musics/shuriken.wav')
rstand = pygame.image.load('./assets/images/RSTAND.png')
lstand = pygame.image.load('./assets/images/LSTAND.png')
Iicon = pygame.image.load('./assets/images/itachiAva.png')
Nicon = pygame.image.load('./assets/images/naruto-icon-3.png')
Clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 60, True)
font40px = pygame.font.SysFont('comicsans', 40, True)
menu = True
class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (125, 65))

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, 'white', self.button, 0, 5)
        pygame.draw.rect(DISPLAYSURF, 'dark gray', [self.pos[0], self.pos[1], 125, 65], 5, 5)
        text2 = font40px.render(self.text, True,(0,0,100))
        DISPLAYSURF.blit(text2, (self.pos[0] + 18, self.pos[1] + 2))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            clicksong.play()
            return True
        else:
            return False
def draw_menu():
    command = -1
    DISPLAYSURF.blit(bgmenu, (-220, 0))
    button1 = Button('Play!', (50, 240))
    button1.draw()
    if button1.check_clicked():
        command = 1
    return command

def intro():
    global menu
    vid = Video("./assets/videos/intro.mp4")
    vid.set_size((800,600))
    while True:
        vid.draw(DISPLAYSURF,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.4)
                menu_command = 0
                run = True
                while run:
                    DISPLAYSURF.fill('light blue')
                    if menu:
                        menu_command = draw_menu()

                        if menu_command != -1:
                            menu = False
                            main_game()
                        
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                    pygame.display.flip()
                

class Player:
    def __init__(self, X = 30, Y = 500, W = 100, H = 100):
        self.x = X
        self.y = Y
        self.width = W 
        self.height = H
        self.speed = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.isJump = False
        self.shooting = False
        self.jumpHeight = 7.5
        self.isStanding = True
        self.hitbox = (self.x + 1, self.y + 3, 60, 90)
        self.health = 270    
    def draw(self, DISPLAYSURF):
        if self.health > 0:
            if self.shooting == True:
                if self.right or self.left:
                    self.isStanding = False
                else:        
                    DISPLAYSURF.blit(jumpRight,(self.x, self.y))
                    self.isStanding = False
            if self.walkCount + 1 > 12:
                self.walkCount = 0
            if not(self.isStanding):
                if self.right:
                    # if self.isGuard == False:
                        DISPLAYSURF.blit(moveRight[self.walkCount//2],(self.x, self.y))
                        self.walkCount+=1
                        self.hitbox = (self.x + 1, self.y + 3, 100, 90) 
                    # else:
                        # DISPLAYSURF.blit(guardRight,(self.x, self.y))  
                elif self.left:
                    # if self.isGuard == False:
                        DISPLAYSURF.blit(moveLeft[self.walkCount//2],(self.x, self.y))
                        self.walkCount+=1
                        self.hitbox = (self.x + 1, self.y + 3, 100, 90) 
                    # else:
                        # DISPLAYSURF.blit(guardLeft,(self.x, self.y))
                else:
                    DISPLAYSURF.blit(jumpRight,(self.x,self.y))
            else:
                if self.right:
                    if self.isJump:
                        DISPLAYSURF.blit(jumpRight,(self.x, self.y))
                    else:
                        DISPLAYSURF.blit(rstand,(self.x,self.y))
                elif self.left:
                    if self.isJump:
                        DISPLAYSURF.blit(jumpLeft,(self.x, self.y))
                    else:
                        DISPLAYSURF.blit(lstand,(self.x,self.y))
                else:
                    DISPLAYSURF.blit(rstand,(self.x,self.y))
                    self.shooting = False
                # if self.isGuard == True:
                #     DISPLAYSURF.blit(guardRight,(self.x, self.y))
                # else:
                #     DISPLAYSURF.blit(stand,(self.x,self.y))
                self.hitbox = (self.x + 1, self.y + 3, 60, 90)
            Ibar = pygame.draw.rect(DISPLAYSURF, (255, 0, 0),(50,40,280,25))
            Ibar2 = pygame.draw.rect(DISPLAYSURF, (255, 255, 0),(55,45,self.health,15))
        else:
            self.speed = 0
            text = font.render('Naruto Wins', True, (255,100,10),(0,0,100))
            DISPLAYSURF.blit(text,(240,210))
            DISPLAYSURF.blit(pygame.image.load('./assets/images/DAMAGE 2_3.png'),(self.x,self.y))
    def Hit(self):
        if self.health > 0:
            self.health -= 10
        else:
            print("Itachi died")
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
        

class enemy:
    def __init__(self, X = 100, Y = 500, W = 100, H = 100, END = 600):
        self.x = X
        self.y = Y
        self.width = W
        self.height = H
        self.end = END
        self.path = [self.x, self.end]
        self.speed = 8
        self.walkCount = 0
        self.hitbox = (self.x + 1, self.y + 3, 60, 90) 
        self.health = 270

    def draw(self, DISPLAYSURF):
        self.move()
        if self.health > 0:
            if self.walkCount + 1 >=6:
                self.walkCount = 0

            if self.speed > 0:
                DISPLAYSURF.blit(moveRight[self.walkCount//2],(self.x,self.y))
                self.walkCount += 1
                self.hitbox = (self.x + 1, self.y + 3, 100, 90) 
            else:
                DISPLAYSURF.blit(moveLeft[self.walkCount//2],(self.x,self.y))
                self.walkCount += 1
                self.hitbox = (self.x + 1, self.y + 3, 100, 90) 
            Nbar2 = pygame.draw.rect(DISPLAYSURF, (255, 0, 0),(440,40,280,25))
            Nbar = pygame.draw.rect(DISPLAYSURF, (255, 255, 0),(445,45,self.health,15))
        else:
            self.speed = 0
            text = font.render('Itachi Wins', True, (255,255,255),(0,0,100))
            DISPLAYSURF.blit(text,(240,210))
            DISPLAYSURF.blit(pygame.image.load('./assets/images/DAMAGE 2_3.png'),(self.x,self.y))

    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0
        else: 
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0
    def Hit (self):
        if self.health > 0:
            self.health -= 10
        else:
            print("Naruto died")

# Hàm dùng để gắn background cũng như tạo loạt ảnh di chuyển cho nhân vật
def drawGameWithImage():
    DISPLAYSURF.blit(bg,(0,0))
    itachi.draw(DISPLAYSURF)
    naruto.draw(DISPLAYSURF)
    DISPLAYSURF.blit(Iicon,(10,10))
    DISPLAYSURF.blit(Nicon,(706,10))
    for shuriken in shurikens:
        shuriken.draw(DISPLAYSURF)
    pygame.display.update()
itachi = Player()
naruto = enemy()
shurikens = []

def main_game():
    BoundLeft = itachi.speed # Biên trái 
    BoundRight = 750 - itachi.width - itachi.speed - 2 # Biên phải
    running = True
    throwSpeed = 0
    while running:
        pygame.time.delay(50)
        if throwSpeed >= 0:
            throwSpeed += 1
        if throwSpeed > 3:
            throwSpeed = 0
        # Bắt sự kiện trong game
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
        if itachi.health > 0 and naruto.health > 0:
            if itachi.hitbox[1] < naruto.hitbox[1] + naruto.hitbox[3] and itachi.hitbox[1] + itachi.hitbox[3] > naruto.hitbox[1]:
                if itachi.hitbox[0] + itachi.hitbox[2] > naruto.hitbox[0] and itachi.hitbox[0] < naruto.hitbox[0] + naruto.hitbox[2]:
                    itachi.Hit()
                    hitsong.play()
        else:
            if itachi.health == 0:
                itachi.speed = 0
        for shuriken in shurikens:
            itachi.shooting = False
            if naruto.health > 0:
                if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > naruto.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < naruto.hitbox[1] + naruto.hitbox[3]:
                    if shuriken.hitbox[0] + shuriken.hitbox[2] > naruto.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < naruto.hitbox[0] + naruto.hitbox[2]:    
                        naruto.Hit()
                        hitsong.play()
                        shurikens.pop(shurikens.index(shuriken))
            else:
                naruto.speed = 0
            if shuriken.x < 750 and shuriken.x > 0:
                shuriken.x += shuriken.vel
            else:
                shurikens.pop(shurikens.index(shuriken))
        # Bắt nút đang được nhấn bởi người dùng
        keys = pygame.key.get_pressed()
        # Phóng shuriken
        if keys[pygame.K_SPACE] and throwSpeed == 0:
            itachi.shooting = True
            itachi.isStanding = False
            if itachi.left == True:
                facing = -1
            else:
                facing = 1
            if len(shurikens) < 5:
                shurikens.append(Weapons(round(itachi.x + 60),round(itachi.y + 30),40, 40, facing))
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
            if keys[pygame.K_UP]:
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
        drawGameWithImage()
intro()