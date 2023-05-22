import pygame

class Button:
    def __init__(self, txt, pos, fontSize, screen,clickSound):
        self.text = txt
        self.pos = pos
        self.font =  pygame.font.SysFont('comicsans', fontSize, True)
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (150, 70))
        self.clicksound = clickSound
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, 'white', self.button, 0, 5) 
        pygame.draw.rect(self.screen, 'dark gray', [self.pos[0], self.pos[1], 150, 70], 5, 5)
        text2 = self.font.render(self.text, True,(0,0,100))
        self.screen.blit(text2, (self.pos[0] + 33, self.pos[1] + 4))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.clicksound.play()
            return True
        else:
            return False