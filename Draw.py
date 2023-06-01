#Import thư viện
import pygame
from Button import *
from main_menu import *
# Khởi tạo màu
RED = (255,0,0)
YELLOW = (255,255,0)

#Gắn thanh máu lên màn hình chính
#Input: Máu nhân vật, tọa độ x,y của thanh máu trên màn hình game, màn hình chính của gane
#Output: Không có
def draw_health_bar(health, x, y, screen):
    pygame.draw.rect(screen,RED,(x - 5, y - 5, 330, 25))
    pygame.draw.rect(screen,YELLOW,(x, y , health, 15))

#Vẽ nhân vật, vẽ thanh máu, vẽ shurikens
#Input: Máu nhân vật, tọa độ x,y của thanh máu trên màn hình game, màn hình chính của gane
#Output: Không có
def drawGameWithImage(screen, player, enemy, bg, shurikens1, shurikens2):
    #Vẽ background
    screen.blit(bg,(0,0))
    #Vẽ thanh máu
    draw_health_bar(player.health, 70, 45, screen)
    draw_health_bar(enemy.health, 605, 45, screen)
    #Vẽ nhân vật
    player.draw(screen)
    enemy.draw(screen)
    #Vẽ shuriken
    for shuriken in shurikens1:
        shuriken.draw(screen)
    for shuriken in shurikens2:
        shuriken.draw(screen)

#Vẽ chữ
#Input: chữ cần vẽ, loại font, màu, màu phông chữ, tọa độ x,y, màn hình chính
#Output: Không có
def draw_text(text, font, text_color, bg_color, x, y, screen):
    img = font.render(text, True, text_color, bg_color)
    screen.blit(img,(x, y))
    
    

