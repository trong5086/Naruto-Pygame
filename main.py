import pygame, sys
from pygame.locals import *
from pyvidplayer import Video 
import Draw as dr
import player
import AIplayer as AI
from Button import *
from main_menu import *
# Khởi tạo pygame
pygame.init()

# Khởi tạo kích thước màn hình game
DISPLAYSURF = pygame.display.set_mode((1000, 600))

# Khởi tạo tiêu đề màn hình game
pygame.display.set_caption('Naruto Fighter')

# Khởi tạo nhạc nền
bgm = pygame.mixer.music.load('./assets/musics/themesong.mp3')
# Thiết lập framerate
clock = pygame.time.Clock()
FPS = 60
# Một số biến chung cho game
intro_count = 0 #Biến đếm ngược để đánh nhau
last_count_update = pygame.time.get_ticks() #Biến đánh mốc thời gian khi vừa mở game
score = [0,0] #Điểm thi đấu của từng nhân vật
round_over = False #Cờ đánh dấu kết thúc ván
round_over_cooldown = 2000 #Đếm ngược khi bắt đầu ván đấu thứ 2 trở đi
round_over_time = 0 #Thời điểm kết thúc ván đầu

# Hàm trở về opening lúc vừa vào game + gọi main menu
# Input: Không có
# Outut: Không có
def intro():
    #Khởi tạo video gán vào biến
    vid = Video("./assets/videos/intro.mp4")
    #Set kích thước video
    vid.set_size((1000,600))
    while True:
        #Vẽ video
        vid.draw(DISPLAYSURF,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            # Bắt sự kiện click chuột hay nhập bất kì từ bàn phím
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                # Đóng video
                vid.close()
                # Bật nhạc
                pygame.mixer.music.play(-1) 
                #Chỉnh volume
                pygame.mixer.music.set_volume(0.2)
                main_menu(DISPLAYSURF,main_game)

# Hàm chủ yếu gắn danh sách các input keys và danh sách shurikens vào P1 và P2, Nếu P2 là AI
# thì keys sẽ dựa vào random các case bên class Aiplayer 
# Input: P1, P2, Ai, Tốc độ ném phi tiêu P1, Tốc độ ném phi tiêu P2
# Danh sách shuriken của P1, Danh sách shuriken của P2
# Outut: Không có               
def handle_input(p1, p2, ai, throwSpeed1, throwSpeed2, shurikens1, shurikens2):
        #Bắt sự kiện nhấn nút
        keys = pygame.key.get_pressed()
        p1.move(DISPLAYSURF, p2, round_over, keys)
        p1.shuriken(throwSpeed1,shurikens1,p2, keys)
        #Nếu AI True thì keys input sẽ được ngẫu nhiên random
        if p2.ai == True:
            ai_input = ai.heuristics()
            if ai_input is not None:
                keys = ai_input
        p2.move(DISPLAYSURF, p1, round_over, keys)
        p2.shuriken(throwSpeed2,shurikens2,p1, keys)

# Hàm chủ yếu gọi phần chính của game: gồm khởi tạo nhân vật, hoạt ảnh đánh nhau, chuyển động... 
# Input: danh sách nhân vật tham gia trận chiến, chế độ chơi, danh sách tên nhân vật, địa hình thi đấu
# Outut: Không có  
def main_game(charaters, mode, character_labels, background):
    #Dùng global dể có thể truy xuất, thay đổi biến bên ngoài phạm vi hàm
    global intro_count
    global last_count_update
    global round_over
    global score
    #Danh sách nhân vật
    listCharacters = []
    #Danh sách background
    listBackgrounds=[
        pygame.image.load('./assets/backgrounds/bg1.png'),
        pygame.image.load('./assets/backgrounds/bg2.jpg'),
        pygame.image.load('./assets/backgrounds/bg3.jpg'),
        pygame.image.load('./assets/backgrounds/bg4.jpg'),
    ]
    #Danh sách Icon nhân vật
    listIcons=[
        pygame.image.load('./assets/images/naruto-icon-3.png'),
        pygame.image.load('./assets/images/sasuke-icon.png'),
        pygame.image.load('./assets/images/ninetails-icon.png'),
    ]
    # Tải ảnh cho nhân vật
    naruto_sheet = pygame.image.load('./assets/images/naruto/nrt.png').convert_alpha()
    sasuke_sheet = pygame.image.load('./assets/images/sasuke/ssk.png').convert_alpha()
    ninetails_sheet = pygame.image.load('./assets/images/ninetails/nine.png').convert_alpha()
    # Mảng số bước animation trong ảnh của sasuke và sasuke
    NARUTO_ANIMATION_STEPS = [4, 6, 3, 3, 4 ,4, 4]
    SASUKE_ANIMATION_STEPS = [4, 6, 3, 3, 4 ,4, 4]
    NINETAILS_ANIMATION_STEPS = [6, 6, 3, 4, 4 ,4, 4]
    # Số lần phóng ảnh
    NARUTO_SCALE = 2
    SASUKE_SCALE = 2
    NINETAILS_SCALE = 2
    # Tọa độ dự phòng bù trừ
    NARUTO_OFFSET = [30, 28]
    SASUKE_OFFSET = [33, 28]
    NINETAILS_OFFSET = [40, 28]
    # Kích thước ảnh
    NARUTO_SIZE = 104
    SASUKE_SIZE = 109
    NINETAILS_SIZE = 184
    # Mảng tổng hợp kích thước, độ phóng, tọa độ dự phòng bù trừ
    NARUTO_DATA = [NARUTO_SIZE, NARUTO_SCALE, NARUTO_OFFSET]
    SASUKE_DATA = [SASUKE_SIZE, SASUKE_SCALE, SASUKE_OFFSET]
    NINETAILS_DATA = [NINETAILS_SIZE, NINETAILS_SCALE, NINETAILS_OFFSET]
    
    #Lọc qua danh sách mảng nhân vật đã chọn thi đấu
    for y,i in enumerate(charaters):
        if character_labels[i] == "NARUTO":
            naruto = player.Player(y+1, 200 if y==0 else 700, 475, False if y == 0 else True, NARUTO_DATA , naruto_sheet, NARUTO_ANIMATION_STEPS, True if y==1 and mode != "P1vsP2" else False, "Naruto", listIcons[0])
            listCharacters.append(naruto)
        elif character_labels[i] == "SASUKE":
            sasuke = player.Player(y+1, 700 if y==1 else 200, 475, True if y == 1 else False, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATION_STEPS, True if y==1 and mode != "P1vsP2" else False, "Sasuke", listIcons[1])
            listCharacters.append(sasuke)
        elif character_labels[i] == "NINETAILS":
            ninetails = player.Player(y+1, 700 if y==1 else 200, 475, True if y == 1 else False, NINETAILS_DATA, ninetails_sheet, NINETAILS_ANIMATION_STEPS, True if y==1 and mode != "P1vsP2" else False, "NineTails", listIcons[2])
            listCharacters.append(ninetails)
    ai = AI.Player(listCharacters[1].input_dict,listCharacters[0], listCharacters[1], ai_scheme = 'heuristic') 
    #Khởi tạo mảng shuriken cho 2 nhân vật
    shurikens1 = []
    shurikens2 = []

    running = True
    
    #Khởi tạo tốc độ phóng shuriken
    throwSpeed1 = 0
    throwSpeed2 = 0

   
    while running:
        #Tạo độ trễ
        pygame.time.delay(35)

        #Tốc độ phóng thiết lập trong khoảng [0,3]
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
            #Bắt sự kiện click chuột
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Khi kết thúc round và có player được 2 điểm trước
                if round_over and (score[0] == 2 or score[1] == 2):
                    clicksound.play()
                    #Hiện nút quay về menu
                    if BTN_BACK.checkForInput(MOUSE_POS):
                        round_over = False
                        score[0]=0
                        score[1]=0
                        main_menu(DISPLAYSURF, main_game)
                    #Hiện nút chơi lại
                    elif BTN_PLAY_AGAIN.checkForInput(MOUSE_POS):
                        round_over = False
                        score[0]=0
                        score[1]=0
                        main_game(charaters, mode, character_labels, background) 
                    pygame.display.update()
        #reset màn hình
        DISPLAYSURF.fill((255,255,255))
    
        #Vẽ các thành phần từ module Draw lên main game
        dr.drawGameWithImage(DISPLAYSURF, listCharacters[0], listCharacters[1], listBackgrounds[background], shurikens1, shurikens2)
        #Vị trí chuột
        MOUSE_POS = pygame.mouse.get_pos()
        #Nút Play again
        BTN_PLAY_AGAIN = Button(image=pygame.image.load("./assets/images/Play Rect.png"), pos=(850, 550), 
                            text_input="Play again!", font=get_font(50, None), base_color="#d7fcd4", hovering_color="White")
        # Nút Back to main menu
        BTN_BACK = Button(image=pygame.image.load("./assets/images/Instructions Rect.png"), pos=(250, 550), 
                            text_input="Back to main menu!", font=get_font(50, None), base_color="#d7fcd4", hovering_color="White")
        if round_over and (score[0] == 2 or score[1] == 2):
            # Thiết lập đổi màu và gắn nút play lên màn hình
            BTN_BACK.changeColor(MOUSE_POS)
            BTN_BACK.update(DISPLAYSURF)
            BTN_PLAY_AGAIN.changeColor(MOUSE_POS)
            BTN_PLAY_AGAIN.update(DISPLAYSURF)
        # Vẽ tính điểm cho 2 nhân vật
        dr.draw_text("P1: " + str(score[0]), get_font(32, True), (255, 0, 0), None, 340, 68, DISPLAYSURF)
        dr.draw_text("P2: " + str(score[1]), get_font(32, True), (255, 0, 0), None, 600, 68, DISPLAYSURF)
        #Sau khi hết 3s thì được phép đánh nhau và di chuyển
        if intro_count <= 0:
            handle_input(listCharacters[0],listCharacters[1], ai, throwSpeed1, throwSpeed2, shurikens1, shurikens2)
        else:
            #Vẽ hoạt ảnh đếm ngược
            dr.draw_text(str(intro_count), get_font(100, True), (255, 0, 0), None, 470, 260, DISPLAYSURF)
            #Tiến hành cập nhập đếm ngược
            if pygame.time.get_ticks() - last_count_update >= 1000:
                # Sau 1 giây trừ biến intro_count đi 1 => Đếm ngược
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
        #Cập nhật 2 nhân vật
        listCharacters[0].update()
        listCharacters[1].update()

        #Khi đang diễn ra trận đấu
        if round_over == False:
            #P1 chết
            if listCharacters[0].alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            #P2 chết
            elif listCharacters[1].alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            #P1 có 2 điểm trước sẽ giành thắng lợi
            if score[0] == 2:
                dr.draw_text( "Overall winner: "+ listCharacters[0].name, get_font(100, True), (255,100,10), None, 95, 280, DISPLAYSURF)

            #P2 có 2 điểm trước sẽ giành thắng lợi
            elif score[1] == 2:
                dr.draw_text("Overall winner: "+ listCharacters[1].name, get_font(100, True), (255,100,10), None, 95, 280, DISPLAYSURF)
            
            #Ngược lại không ai giành 2 điểm trước trận đấu tiếp theo sẽ diễn ra
            else:
                #P1 có 1 điểm  
                if score[0] == 1 and score[1] == 0:
                    dr.draw_text( listCharacters[0].name + " win", get_font(100, True), (255,100,10), None, 285, 280, DISPLAYSURF)
                #P2 có 1 điểm                
                elif score[1] == 1:
                    dr.draw_text( listCharacters[1].name + " win", get_font(100, True), (255,100,10), None, 285, 280, DISPLAYSURF)
                if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
                    round_over = False
                    intro_count = 3
                    listCharacters= [] 
                    for y,i in enumerate(charaters):
                        if character_labels[i] == "NARUTO":
                            naruto = player.Player(y+1, 200 if y==0 else 700, 475, False if y == 0 else True, NARUTO_DATA , naruto_sheet, NARUTO_ANIMATION_STEPS, True if y==1 and mode != "P1vsP2" else False, "Naruto", listIcons[0])
                            listCharacters.append(naruto)
                        elif character_labels[i] == "SASUKE":
                            sasuke = player.Player(y+1, 700 if y==1 else 200, 475, True if y == 1 else False, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATION_STEPS, True if (y==1 and mode != "P1vsP2") else False, "Sasuke", listIcons[1])
                            listCharacters.append(sasuke)
                        elif character_labels[i] == "NINETAILS":
                            ninetails = player.Player(y+1, 700 if y==1 else 200, 475, True if y == 1 else False, NINETAILS_DATA, ninetails_sheet, NINETAILS_ANIMATION_STEPS, True if y==1 and mode != "P1vsP2" else False, "NineTails", listIcons[2])
                            listCharacters.append(ninetails)
                    ai = AI.Player(listCharacters[1].input_dict,listCharacters[0], listCharacters[1], ai_scheme = 'heuristic')
        pygame.display.update()
#Gọi intro
intro()

