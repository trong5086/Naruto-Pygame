import pygame
import Button as btn
Iicon = pygame.image.load('./assets/images/itachiAva.png')
Nicon = pygame.image.load('./assets/images/naruto-icon-3.png')
RED = (255,0,0)
YELLOW = (255,255,0)
def draw_health_bar(health, x, y, screen):
    pygame.draw.rect(screen,RED,(x - 5, y - 5, 330, 25))
    pygame.draw.rect(screen,YELLOW,(x, y , health, 15))
    screen.blit(Iicon,(10,10))
    screen.blit(Nicon,(900,10))

def drawGameWithImage(screen, player, enemy, bg, shurikens1, shurikens2):
    screen.blit(bg,(0,0))
    draw_health_bar(player.health, 70, 45, screen)
    draw_health_bar(enemy.health, 620, 45, screen)
    player.draw(screen)
    enemy.draw(screen)
    for shuriken in shurikens1:
        shuriken.draw(screen)
    for shuriken in shurikens2:
        shuriken.draw(screen)
    
def draw_menu(screen, bgmenu, clicksound):
    command = -1
    screen.blit(bgmenu, (0, 0))
    button1 = btn.Button('Play!', (125, 285), 40, screen, clicksound)
    button1.draw()
    if button1.check_clicked():
        command = 1
    return command
def draw_text(text, font, text_color, x, y, screen):
    img = font.render(text, True, text_color)
    screen.blit(img,(x, y))
    
    

