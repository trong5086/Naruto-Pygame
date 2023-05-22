import pygame, sys
from pygame.locals import *
from pyvidplayer import Video 
import Button as btn
import Draw as dr
import player
import AIplayer as AI
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('sasuke')
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
clicksound = pygame.mixer.Sound('./assets/musics/clickSound.wav')
shurikensong = pygame.mixer.Sound('./assets/musics/shuriken.wav')
rstand = pygame.image.load('./assets/images/RSTAND.png')
lstand = pygame.image.load('./assets/images/LSTAND.png')
# Khai báo font
font = pygame.font.SysFont('comicsans', 80, True)
font30 = pygame.font.SysFont('comicsans', 30, True)

# Thiết lập framerate
clock = pygame.time.Clock()
FPS = 60
menu = True
# Một số biến chung cho game
intro_count = 0 #Biến đếm ngược để đánh nhau
last_count_update = pygame.time.get_ticks() #Biến đánh mốc thời gian khi vừa mở game
score = [0,0]
round_over = False
round_over_cooldown = 2000
# Tải ảnh cho nhân vật
naruto_sheet = pygame.image.load('./assets/images/naruto/nrt.png').convert_alpha()
sasuke_sheet = pygame.image.load('./assets/images/sasuke/ssk.png').convert_alpha()
# Mảng số bước animation trong ảnh của sasuke và sasuke
NARUTO_ANIMATION_STEPS = [4, 6, 3, 3, 4 ,4, 4]
SASUKE_ANIMATION_STEPS = [4, 6, 3, 3, 4 ,4, 4]
# Khai báo biến liên quan tới kích thước ảnh
NARUTO_SCALE = 2
NARUTO_OFFSET = [36, 28]
NARUTO_SIZE = 104
NARUTO_DATA = [NARUTO_SIZE, NARUTO_SCALE, NARUTO_OFFSET]
SASUKE_SIZE = 109
SASUKE_SCALE = 2
SASUKE_OFFSET = [38, 28]
SASUKE_DATA = [SASUKE_SIZE, SASUKE_SCALE, SASUKE_OFFSET]
round_over_time = 0
def intro():
    global menu
    vid = Video("./assets/videos/intro.mp4")
    vid.set_size((1000,600))
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
                        menu_command = dr.draw_menu(DISPLAYSURF, bgmenu, clicksound)
                        if menu_command != -1:
                            menu = False
                            main_game()
                        
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                    pygame.display.flip()
                

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
            # Nbar2 = pygame.draw.rect(DISPLAYSURF, (255, 0, 0),(440,40,280,25))
            # Nbar = pygame.draw.rect(DISPLAYSURF, (255, 255, 0),(445,45,self.health,15))
        else:
            self.speed = 0
            text = font.render('naruto Wins', True, (255,255,255),(0,0,100))
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
            print("sasuke died")


def handle_input(naruto, sasuke, ai, throwSpeed1, throwSpeed2, shurikens1, shurikens2):
        keys = pygame.key.get_pressed()
        naruto.move(DISPLAYSURF, sasuke, round_over, keys)
        naruto.shuriken(throwSpeed1,shurikens1,sasuke, keys)
        if sasuke.ai == True:
            ai_input = ai.get_input()
            if ai_input is not None:
                keys = ai_input
        sasuke.move(DISPLAYSURF, naruto, round_over, keys)
        sasuke.shuriken(throwSpeed2,shurikens2,naruto, keys)


def main_game():
    global intro_count
    global last_count_update
    global round_over
    naruto = player.Player(1, 200, 475, False, NARUTO_DATA, naruto_sheet, NARUTO_ANIMATION_STEPS, False)
    sasuke = player.Player(2, 700, 475, True, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATION_STEPS, False)
    ai = AI.Player(sasuke.input_dict,naruto, sasuke, ai_scheme = 'heuristic')
    shurikens1 = []
    shurikens2 = []
    running = True
    throwSpeed1 = 0
    throwSpeed2 = 0
    while running:
        pygame.time.delay(30)
        if throwSpeed1 >= 0:
            throwSpeed1 += 1
        if throwSpeed1 > 3:
            throwSpeed1 = 0
        if throwSpeed2 >= 0:
            throwSpeed2 += 1
        if throwSpeed2 > 3:
            throwSpeed2 = 0
        # Bắt sự kiện trong game
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
        dr.drawGameWithImage(DISPLAYSURF, naruto, sasuke, bg, shurikens1, shurikens2)
        # Vẽ tính điểm cho 2 nhân vật
        dr.draw_text("P1: " + str(score[0]), font30, (255, 0, 0), 64, 60, DISPLAYSURF)
        dr.draw_text("P2: " + str(score[1]), font30, (255, 0, 0), 614, 60, DISPLAYSURF)
        #Sau khi hết 3s thì được phép đánh nhau và di chuyển
        if intro_count <= 0:
            handle_input(naruto,sasuke,ai, throwSpeed1, throwSpeed2, shurikens1, shurikens2)
            # naruto.move(DISPLAYSURF, sasuke, round_over)
            # sasuke.move(DISPLAYSURF, naruto, round_over)
            
        else:
            #Vẽ hoạt ảnh đếm ngược
            dr.draw_text(str(intro_count), font, (255, 0, 0), 500, 200, DISPLAYSURF)
            #Tiến hành cập nhập đếm ngược
            if pygame.time.get_ticks() - last_count_update >= 1000:
                # Sau 1 giây trừ biến intro_count đi 1 => Đếm ngược
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
        naruto.update()
        sasuke.update()
        if round_over == False:
            if naruto.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif sasuke.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            if score[0] == 2 and naruto.player == 1:
                print("Player 1 win")
            elif score[1] == 2 and sasuke.player == 2:
                print("Player 2 win")
            else:
                if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
                    round_over = False
                    intro_count = 3
                    naruto = player.Player(1, 200, 475, False, NARUTO_DATA, naruto_sheet, NARUTO_ANIMATION_STEPS, False)
                    sasuke = player.Player(2, 700, 475, True, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATION_STEPS, False)
                    ai = AI.Player(sasuke.input_dict,naruto, sasuke, ai_scheme = 'heuristic')
        pygame.display.update()
intro()
