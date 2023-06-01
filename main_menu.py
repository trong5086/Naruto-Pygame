#Import thư viện, module
import pygame, sys
from pygame.locals import *
from Button import Button
import random

#Khởi tạo pygame
pygame.init()

#Background cho phần chọn menu và âm thanh click chuột
bgmenu = pygame.image.load('./assets/backgrounds/menubg.png')
clicksound = pygame.mixer.Sound('./assets/musics/clickSound.wav')

#Biến phát theme song
isplaying = True

#Hàm tạo font
#Input: Size chữ, Có in đậm True ngược lại None
#Output: Trả về font cùng các thuộc tính sau khi khởi tạo
def get_font(size, bold):
    return pygame.font.SysFont("comicomicsans", size, bold)

#Hàm random bot ngoại trừ nhân vật của P1
#Input: index của nhân vật mà P1 đã chọn
#Output: Trả về index của bot ngẫu nhiên
def randomBot(x):
    choices = [0, 1, 2]
    choices.remove(x)
    return random.choice(choices)

#Hàm vẽ màn hình chọn địa hình thi đấu
#Input: màn hình game, hàm main_game, danh sách 2 nhân vật dẵ chọn, danh sách tên 2 nhân vật
#Output: Không có
def choose_background(screen,main_game, selected_character,mode, character_labels):
     # Danh sách background để chọn
     choosebackground_images = [
     pygame.image.load("./assets/backgrounds/bg1-300.jpg"),
     pygame.image.load("./assets/backgrounds/bg2-300.jpg"),
     pygame.image.load("./assets/backgrounds/bg3-300.jpg"),
     pygame.image.load("./assets/backgrounds/bg4-300.jpg"),
]
     # Danh sách tọa độ, kích thước của ảnh
     background_rects = [
     pygame.Rect(145, 100, 300, 169),
     pygame.Rect(570, 100, 300, 169),
     pygame.Rect(145, 310, 300, 169),
     pygame.Rect(570, 310, 300, 169),
]
     # Danh sách ảnh nền review
     background_images = [
    pygame.image.load('./assets/backgrounds/bg1.png'),
    pygame.image.load('./assets/backgrounds/bg2.jpg'),
    pygame.image.load('./assets/backgrounds/bg3.jpg'),
    pygame.image.load('./assets/backgrounds/bg4.jpg'), 
]
     # Tên của từng background
     background_labels = [
    "BACKGROUND 1",
    "BACKGROUND 2",
    "BACKGROUND 3",
    "BACKGROUND 4",
]
     #Biến lưu background được chọn
     selected_background = None
     running = True
     while running:
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
               #Bắt sự kiện click chuột
               elif event.type == MOUSEBUTTONDOWN:
                    #Âm thanh click
                    clicksound.play()
                    if selected_background is not None:
                         if BTN_PLAY.checkForInput(PLAY_MOUSE_POS):
                              main_game(selected_character, mode, character_labels, selected_background)
                              screen.fill((0, 0, 0))
                    #Bắt sự kiện click chuột vào nút Back
                    if BTN_BACK.checkForInput(PLAY_MOUSE_POS):
                         play(screen,main_game)
                    for i, rect in enumerate(background_rects):
                         #Click chọn background
                         if rect.collidepoint(event.pos):
                              #Lưu background được chọn vào biến
                              selected_background = i
          #Reset màn hình 
          screen.fill((0, 0, 0))
          
          #Show review background
          if selected_background is not None:
               #Thiết lập background nằm giữa khung hình
               background_image = background_images[selected_background]
               screen_center = screen.get_rect().center
               background_rect = background_image.get_rect(center=screen_center)
               screen.blit(background_image, background_rect)

          #Gắn danh sách và tên background
          for i, rect in enumerate(background_rects):
               pygame.draw.rect(screen, (255, 255, 255), rect, 4)
               background_image = choosebackground_images[i]
               image_rect = background_image.get_rect(center=rect.center)
               screen.blit(background_image, image_rect)
               #Gắn nhãn tên background
               label_font = pygame.font.SysFont(None, 20)
               label_text = label_font.render(background_labels[i], True, (255, 255, 255))
               label_rect = label_text.get_rect(center=(rect.centerx, rect.bottom + 20))
               screen.blit(label_text, label_rect)
              
          # Gắn ảnh   
          if selected_background is not None:
               pygame.draw.rect(screen, (255, 0, 0), background_rects[selected_background], 4) 
               
          #Lấy vị trị chuột
          PLAY_MOUSE_POS = pygame.mouse.get_pos()
          #Nút Play
          BTN_PLAY = Button(image=pygame.image.load("./assets/images/Play Rect.png"), pos=(850, 550), 
                            text_input="PLAY!", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          
          #Nút Back
          BTN_BACK = Button(image=pygame.image.load("./assets/images/Play Rect.png"), pos=(150, 550), 
                            text_input="BACK!", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          #Thiết lập đổi màu và gắn nút vào màn hình cho 2 nút
          BTN_BACK.changeColor(PLAY_MOUSE_POS)
          BTN_BACK.update(screen)
          BTN_PLAY.changeColor(PLAY_MOUSE_POS)
          BTN_PLAY.update(screen)
          pygame.display.update()

#Hàm vẽ màn hình chọn các options: Play P1vsP2, P1vsBot, Back to main menu
#Input: màn hình game, hàm main_game
#Output: Không có
def play(screen,main_game):
    while True:
          #Lấy vị trí chuột
          PLAY_MOUSE_POS = pygame.mouse.get_pos()
          #Gắn ảnh vào menu
          screen.blit(bgmenu,(0,0))

          #Gắn nút Play P1 vs P2
          PLAY_P1_P2 = Button(image=pygame.image.load("./assets/images/Mode Rect.png"), pos=(240, 190), 
                            text_input="P1 VS P2", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          
          #Gắn nút Play P1 vs Bot
          PLAY_P1_BOT = Button(image=pygame.image.load("./assets/images/Mode Rect.png"), pos=(240, 290), 
                            text_input="P1 VS BOT", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")

          #Gắn nút Back
          PLAY_BACK = Button(image=None, pos=(240, 390), 
                            text_input="BACK", font=get_font(60, None), base_color="White", hovering_color="Green")
          #Thiết lập đổi màu và gắn nút vào màn hình cho 3 nút
          for button in [PLAY_P1_P2, PLAY_P1_BOT, PLAY_BACK]:
               button.changeColor(PLAY_MOUSE_POS)
               button.update(screen)

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    #Thoát game
                    pygame.quit()
                    sys.exit()
               if event.type == pygame.MOUSEBUTTONDOWN:
                    clicksound.play()
                    #Direct hướng click nút back
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                         main_menu(screen,main_game)

                    #Direct hướng click nút Play P1 Vs P2     
                    elif PLAY_P1_P2.checkForInput(PLAY_MOUSE_POS):
                         choose_P1_P2(screen, main_game)

                    #Direct hướng click nút Play P1 vs Bot
                    elif PLAY_P1_BOT.checkForInput(PLAY_MOUSE_POS):
                         choose_P1_BOT(screen, main_game)

          #Cập nhật hoạt ảnh
          pygame.display.update()

#Hàm vẽ màn hình hướng dẫn
#Input: màn hình game, hàm main_game
#Output: Không có
def instructions(screen,main_game):
    while True:
        #Lấy vị trí chuột
        INSTRUCTIONS_MOUSE_POS = pygame.mouse.get_pos()
        # fill màn hình trắng
        screen.fill("white")

        # Tạo text hướng dẫn
        INSTRUCTIONS_TEXT = get_font(60, None).render("INSTRUCTION TO PLAY GAME", True, "Black")
        INSTRUCTIONS_CONTENT1 = get_font(34, None).render("Players will have 3 games to decide if the player who gets 2 points first will be the winner", True, "Black")
        INSTRUCTIONS_CONTENT2 = get_font(34, None).render("If you choose P1 VS P2 mode, the movement keys of each character:", True, "Black")
        INSTRUCTIONS_CONTENT3 = get_font(34, None).render("The first player is:", True, "Black")
        INSTRUCTIONS_CONTENT4 = get_font(34, None).render("W - Up, D - Right, A - Left, R - Attack 1, T - Attack 2, Y - Attack 3", True, "Black")     
        INSTRUCTIONS_CONTENT5 = get_font(34, None).render("SPACE - Throw Shuriken.", True, "Black")   
        INSTRUCTIONS_CONTENT6 = get_font(34, None).render("The second player is:", True, "Black") 
        INSTRUCTIONS_CONTENT7 = get_font(34, None).render("Up Key - Up, Right Key - Right, Left Key - Left", True, "Black")
        INSTRUCTIONS_CONTENT8 = get_font(34, None).render("H - Attack 1, J - Attack 2, K - Attack 3 and L - Throw Shuriken.", True, "Black")
        INSTRUCTIONS_CONTENT9 = get_font(34, None).render("In the match press ESC to QUIT ", True, "Black")            
     
        # Tạo tọa độ của text
        INSTRUCTIONS_RECT = INSTRUCTIONS_TEXT.get_rect(center=(510, 80))
        INSTRUCTIONS_CONTENT1_RECT = INSTRUCTIONS_CONTENT1.get_rect(center=(500, 155))
        INSTRUCTIONS_CONTENT2_RECT = INSTRUCTIONS_CONTENT2.get_rect(center=(500, 210))
        INSTRUCTIONS_CONTENT3_RECT = INSTRUCTIONS_CONTENT3.get_rect(center=(500, 250))
        INSTRUCTIONS_CONTENT4_RECT = INSTRUCTIONS_CONTENT4.get_rect(center=(500, 290))
        INSTRUCTIONS_CONTENT5_RECT = INSTRUCTIONS_CONTENT5.get_rect(center=(500, 330))
        INSTRUCTIONS_CONTENT6_RECT = INSTRUCTIONS_CONTENT6.get_rect(center=(500, 370))
        INSTRUCTIONS_CONTENT7_RECT = INSTRUCTIONS_CONTENT7.get_rect(center=(500, 410))
        INSTRUCTIONS_CONTENT8_RECT = INSTRUCTIONS_CONTENT8.get_rect(center=(500, 450))
        INSTRUCTIONS_CONTENT9_RECT = INSTRUCTIONS_CONTENT9.get_rect(center=(500, 490))

        # Gắn chữ vào màn hình
        screen.blit(INSTRUCTIONS_TEXT, INSTRUCTIONS_RECT)
        screen.blit(INSTRUCTIONS_CONTENT1, INSTRUCTIONS_CONTENT1_RECT)
        screen.blit(INSTRUCTIONS_CONTENT2, INSTRUCTIONS_CONTENT2_RECT)
        screen.blit(INSTRUCTIONS_CONTENT3, INSTRUCTIONS_CONTENT3_RECT)
        screen.blit(INSTRUCTIONS_CONTENT4, INSTRUCTIONS_CONTENT4_RECT)
        screen.blit(INSTRUCTIONS_CONTENT5, INSTRUCTIONS_CONTENT5_RECT)
        screen.blit(INSTRUCTIONS_CONTENT6, INSTRUCTIONS_CONTENT6_RECT)
        screen.blit(INSTRUCTIONS_CONTENT7, INSTRUCTIONS_CONTENT7_RECT)
        screen.blit(INSTRUCTIONS_CONTENT8, INSTRUCTIONS_CONTENT8_RECT)
        screen.blit(INSTRUCTIONS_CONTENT9, INSTRUCTIONS_CONTENT9_RECT)
        # Nút Back
        INSTRUCTIONS_BACK = Button(image=None, pos=(900, 550), 
                            text_input="BACK", font=get_font(75, None), base_color="Black", hovering_color="Green")
        # Thiết lập đổi màu và cập nhật nút Back lên screen
        INSTRUCTIONS_BACK.changeColor(INSTRUCTIONS_MOUSE_POS)
        INSTRUCTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
               #Âm thanh click
               clicksound.play()
               if INSTRUCTIONS_BACK.checkForInput(INSTRUCTIONS_MOUSE_POS):
                    main_menu(screen,main_game)

        pygame.display.update()
#Hàm vẽ màn hình chọn nhân vật cho chế độ P1 vs P2
#Input: màn hình game, hàm main_game
#Output: Không có
def choose_P1_P2(screen, main_game):
     # Danh sách ảnh nhân vật để chọn
     character_images = [
     pygame.image.load("./assets/images/naruto/naruto-200.png"),
     pygame.image.load("./assets/images/sasuke/sasuke-200.png"),
     pygame.image.load("./assets/images/ninetails/ninetails-200.png"),
]
     # Danh sách tọa độ, kích thước của ảnh nhân vật
     character_rects = [
     pygame.Rect(240, 375, 130, 130),
     pygame.Rect(440, 375, 130, 130),
     pygame.Rect(640, 375, 130, 130),
]
     # Danh sách ảnh nhân vật review
     background_images = [
    pygame.image.load('./assets/images/naruto/naruto.jpg'),
    pygame.image.load('./assets/images/sasuke/sasuke.jpg'),
    pygame.image.load('./assets/images/ninetails/ninetails.jpg'),
]
     # Danh sách tên nhân vật
     character_labels = [
    "NARUTO",
    "SASUKE",
    "NINETAILS"
]
     #Mảng nhân vật được chọn
     selected_characters = [None, None]
     current_player = 1
     running = True
     while running:
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
               #Bắt sự kiến click chuột
               elif event.type == MOUSEBUTTONDOWN:
                    #Âm thanh khi click
                    clicksound.play()
                    #Nút Play chỉ dược click khi nhân vật đã được chọn cho P1 và P2
                    if selected_characters[0] is not None and selected_characters[1] is not None:
                         if BTN_PLAY.checkForInput(PLAY_MOUSE_POS):
                              choose_background(screen,main_game, selected_characters,"P1vsP2", character_labels)
                    # Direct nút Play khi click
                    if BTN_BACK.checkForInput(PLAY_MOUSE_POS):
                         play(screen,main_game)
                    for i, rect in enumerate(character_rects):
                         #Bắt sự kiến khi click chọn nhân vật
                         if rect.collidepoint(event.pos):
                              if selected_characters[0] == i or selected_characters[1] == i:
                                   if selected_characters[0] == i:
                                        selected_characters[0] = None
                                        current_player = 1
                                   elif selected_characters[1] == i :
                                        selected_characters[1] = None
                                        current_player = 2
                              elif selected_characters[0] is None:
                                   selected_characters[0] = i
                                   current_player = 2
                              elif current_player == 1 and selected_characters[0] is None:
                                   selected_characters[0] = i
                                   current_player = 2
                              elif current_player == 2 and selected_characters[1] is None:
                                   selected_characters[1] = i
                                   current_player = 1
                              elif current_player == 1 and selected_characters[0] is not None:
                                   selected_characters[0] = i
                                   current_player = 2
                              elif current_player == 2 and selected_characters[1] is not None:
                                   selected_characters[1] = i
                                   current_player = 1
                              
          #Reset màn hình           
          screen.fill((0, 0, 0))
          #Lặp qua danh sách nhân vật đã chọn
          for i, character in enumerate(selected_characters):
               if character is not None:
                    background_image = background_images[character]
                    background_rect = background_image.get_rect()
                    #Nhân vật P1 ảnh background được gắn 50% bên trái
                    if i == 0:
                         background_rect.left = 0
                         background_rect.top = 0
                         background_rect.width = screen.get_width() // 2
                         background_image = pygame.transform.scale(background_image, (background_rect.width, background_rect.height))
                         screen.blit(background_image, background_rect)
                    #Nhân vật P2 ảnh background được gắn 50% bên phải
                    elif i == 1:
                         background_rect.left = screen.get_width() // 2
                         background_rect.top = 0
                         background_rect.width = screen.get_width() // 2
                         background_image = pygame.transform.flip(background_image, True, False)
                         background_image = pygame.transform.scale(background_image, (background_rect.width, background_rect.height))
                         screen.blit(background_image, background_rect)

          for i, rect in enumerate(character_rects):
               # Vẽ ảnh nhân vật gắn lên màn hình game
               pygame.draw.rect(screen, (255, 255, 255), rect, 2)
               character_image = character_images[i]
               image_rect = character_image.get_rect(center=(rect.centerx, rect.centery))
               screen.blit(character_image, image_rect)
              #Gắn tên cho nhân vật
               label_font = pygame.font.SysFont(None, 20)
               label_text = label_font.render(character_labels[i], True, (255, 255, 255))
               label_rect = label_text.get_rect(center=(rect.centerx, rect.bottom + 20))
               screen.blit(label_text, label_rect)

               #Nhân vật được chọn ở đầu danh sách sẽ được viền xanh lá và có chữ P1
               if selected_characters[0] == i:
                    pygame.draw.rect(screen, (0, 255, 0), rect, 2)
                    label_text = get_font(40, None).render("P1", True, (0, 255, 0))
                    label_rect = label_text.get_rect(center=(rect.centerx + 55, rect.centery - 90))
                    screen.blit(label_text, label_rect)
                    character_image = character_images[i]

               #Nhân vật được chọn ở đầu danh sách sẽ được viền xanh biển và có chữ P1  
               elif selected_characters[1] == i:
                    pygame.draw.rect(screen, (0, 0, 255), rect, 2)
                    label_text = get_font(40, None).render("P2", True, (0, 0, 255))
                    label_rect = label_text.get_rect(center=(rect.centerx + 55, rect.centery - 90))
                    screen.blit(label_text, label_rect)
                    character_image = character_images[i]

          #Vị trí chuột
          PLAY_MOUSE_POS = pygame.mouse.get_pos()

          #Nút Play
          BTN_PLAY = Button(image=pygame.image.load("./assets/images/Play Rect.png"), pos=(850, 550), 
                              text_input="PLAY!", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          #Nút Back
          BTN_BACK = Button(image=pygame.image.load("./assets/images/Play Rect.png"), pos=(150, 550), 
                              text_input="BACK!", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          
          # Thiết lập đổi màu và gắn nút play lên màn hình
          BTN_BACK.changeColor(PLAY_MOUSE_POS)
          BTN_BACK.update(screen)
          BTN_PLAY.changeColor(PLAY_MOUSE_POS)
          BTN_PLAY.update(screen)
          
               
          pygame.display.update()
          
#Hàm vẽ màn hình chọn nhân vật cho chế độ P1 vs Bot
#Input: màn hình game, hàm main_game
#Output: Không có
def choose_P1_BOT(screen, main_game):
     #Danh sách ảnh chọn nhân vật
     character_images = [
     pygame.image.load("./assets/images/naruto/naruto-200.png"),
     pygame.image.load("./assets/images/sasuke/sasuke-200.png"),
     pygame.image.load("./assets/images/ninetails/ninetails-200.png"),
]

     #Danh sách tọa độ, kích thước ảnh nhân vật
     character_rects = [
     pygame.Rect(240, 375, 130, 130),
     pygame.Rect(440, 375, 130, 130),
     pygame.Rect(640, 375, 130, 130),
]
     #Danh sách background ảnh nhân vật
     background_images = [
    pygame.image.load('./assets/images/naruto/naruto.jpg'),
    pygame.image.load('./assets/images/sasuke/sasuke.jpg'),
    pygame.image.load('./assets/images/ninetails/ninetails.jpg'),
]
     #Danh sách tên nhân vật
     character_labels = [
    "NARUTO",
    "SASUKE",
    "NINETAILS"
]
     #Nhân vật đã chọn
     selected_character = None
     running = True
     while running:
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
               elif event.type == MOUSEBUTTONDOWN:
                    clicksound.play()
                    if selected_character is not None:
                         if BTN_PLAY.checkForInput(PLAY_MOUSE_POS):
                              choose_background(screen,main_game, [selected_character, randomBot(selected_character)],"P1vsBOT", character_labels)
                    if BTN_BACK.checkForInput(PLAY_MOUSE_POS):
                         play(screen,main_game)
                    for i, rect in enumerate(character_rects):
                         if rect.collidepoint(event.pos):
                              selected_character = i
          screen.fill((0, 0, 0))
          
          if selected_character is not None:
               background_image = background_images[selected_character]
               screen_center = screen.get_rect().center
               background_rect = background_image.get_rect(center=screen_center)
               screen.blit(background_image, background_rect)

          for i, rect in enumerate(character_rects):
               pygame.draw.rect(screen, (255, 255, 255), rect, 4)
               character_image = character_images[i]
               image_rect = character_image.get_rect(center=rect.center)
               screen.blit(character_image, image_rect)
               label_font = pygame.font.SysFont(None, 20)
               label_text = label_font.render(character_labels[i], True, (255, 255, 255))
               label_rect = label_text.get_rect(center=(rect.centerx, rect.bottom + 20))
               screen.blit(label_text, label_rect)
               if selected_character == i:
                    choose_text = get_font(40, None).render("P1", True, (255, 0, 0))
                    choose_rect = choose_text.get_rect(center=(rect.centerx + 55, rect.centery - 90))
                    screen.blit(choose_text, choose_rect)
               
          if selected_character is not None:
               pygame.draw.rect(screen, (255, 0, 0), character_rects[selected_character], 4) 
               

          PLAY_MOUSE_POS = pygame.mouse.get_pos()
          BTN_PLAY = Button(image=pygame.image.load("./assets/images/Play Rect.png"), pos=(850, 550), 
                            text_input="PLAY!", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          BTN_BACK = Button(image=pygame.image.load("./assets/images/Play Rect.png"), pos=(150, 550), 
                            text_input="BACK!", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          BTN_BACK.changeColor(PLAY_MOUSE_POS)
          BTN_BACK.update(screen)
          BTN_PLAY.changeColor(PLAY_MOUSE_POS)
          BTN_PLAY.update(screen)
          pygame.display.update()
#Hàm vẽ màn hình main menu sau khi hết opening gồm các options: Play, Instruction, Music, Quit
#Input: màn hình game, hàm main_game
#Output: Không có
def main_menu(screen,main_game):
     global isplaying
     if isplaying:
          music = "ON"
     else:
          music = "OFF"
     while True:
          #Gắn ảnh background cho menu
          screen.blit(bgmenu, (0, 0))

          MENU_MOUSE_POS = pygame.mouse.get_pos()

          PLAY_BUTTON = Button(image=pygame.image.load("./assets/images/Play Rect.png"), pos=(240, 150), 
                              text_input="PLAY!", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          INSTRUCTIONS_BUTTON = Button(image=pygame.image.load("./assets/images/instructions Rect.png"), pos=(240, 250), 
                              text_input="INSTRUCTIONS", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          
          MUSIC_BUTTON = Button(image=pygame.image.load("./assets/images/instructions Rect.png"), pos=(240, 350), 
                              text_input="MUSIC IS: " + music, font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")
          
          QUIT_BUTTON = Button(image=pygame.image.load("./assets/images/Quit Rect.png"), pos=(240, 450), 
                              text_input="QUIT", font=get_font(60, None), base_color="#d7fcd4", hovering_color="White")

          for button in [PLAY_BUTTON, INSTRUCTIONS_BUTTON, QUIT_BUTTON, MUSIC_BUTTON]:
               button.changeColor(MENU_MOUSE_POS)
               button.update(screen)
          
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
               if event.type == pygame.MOUSEBUTTONDOWN:
                    clicksound.play()
                    #Direct nút Play
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                         play(screen,main_game)
                    #Direct nút Instructions
                    if INSTRUCTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                         instructions(screen,main_game)
                    #Bật, tắt nhạc
                    if MUSIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                         if isplaying == True:
                              pygame.mixer.music.stop()
                              isplaying = False
                              music = "OFF" 
                         else:
                              pygame.mixer.music.play(-1)
                              music = "ON"
                              isplaying = True
                    #Direct nút Quit
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                         pygame.quit()
                         sys.exit()

          pygame.display.update()
