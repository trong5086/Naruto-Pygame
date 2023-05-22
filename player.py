import pygame
import math
import weapons as wp
pygame.init()
font = pygame.font.SysFont('comicsans', 60, True)
bgmenu = pygame.image.load('./assets/backgrounds/menubg.png')
bgm = pygame.mixer.music.load('./assets/musics/themesong.mp3')
hitsong = pygame.mixer.Sound('./assets/musics/hit.wav')
clicksound = pygame.mixer.Sound('./assets/musics/clickSound.wav')
shurikensong = pygame.mixer.Sound('./assets/musics/shuriken.wav')

class Player:
     def __init__(self, PLAYER ,X, Y, FLIP, DATA, SPRITES_SHEET, ANIMATION_STEPS, AI):
          self.player = PLAYER
          self.size = DATA[0]
          self.offset = DATA[2]
          self.image_scale = DATA[1]
          self.rect = pygame.Rect((X,Y,80,115))
          self.animation_list = self.loadimg(SPRITES_SHEET, ANIMATION_STEPS)
          self.action = 0
          self.frame_index = 0
          self.image = self.animation_list[self.action][self.frame_index]
          self.speed = 10
          self.running = False
          self.right = False
          self.walkCount = 0
          self.isJump = False
          self.shooting = False
          self.jumpHeight = 7.5
          self.isStanding = True
          self.attack_type = 0
          self.hit = False
          self.flip = FLIP
          self.update_time = pygame.time.get_ticks()
          self.attacking = False
          self.hitbox = (self.rect.x + 10, self.rect.y + 10, 60, 90)
          self.health = 320
          self.alive = True
          self.attack_cooldown = 0
          self.input_dict = {
                'jump': pygame.K_UP,
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'down': pygame.K_DOWN,
                'attack1': pygame.K_h,
                'attack2': pygame.K_j,
                'attack3': pygame.K_k,
                'shurikens': pygame.K_l,
            }
          self.ai = AI
     def draw(self, DISPLAYSURF):
          img = pygame.transform.flip(self.image, self.flip, False)
          pygame.draw.rect(DISPLAYSURF,(255,255,0), self.hitbox)
          # pygame.draw.rect(DISPLAYSURF,(255,0,0), self.rect)
          DISPLAYSURF.blit(img,(self.rect.x - (self.offset[0] * self.image_scale),self.rect.y-(self.offset[1] * self.image_scale)))
          # if self.health > 0:
          #      if self.shooting == True:
          #           if self.right or self.left:
          #                self.isStanding = False
          #           else:        
          #                DISPLAYSURF.blit(jumpRight,(self.rect.x, self.rect.y))
          #                self.isStanding = False
          #      if self.walkCount + 1 > 12:
          #           self.walkCount = 0
          #      if not(self.isStanding):
          #           if self.right:
          #               DISPLAYSURF.blit(moveRight[self.walkCount//2],(self.rect.x, self.rect.y))
          #               self.walkCount+=1
          #               self.hitbox = (self.rect.x + 1, self.rect.y + 3, 100, 90) 
          #           elif self.left:
          #               DISPLAYSURF.blit(moveLeft[self.walkCount//2],(self.rect.x, self.rect.y))
          #               self.walkCount+=1
          #               self.hitbox = (self.rect.x + 1, self.rect.y + 3, 100, 90) 
          #           else:
          #                DISPLAYSURF.blit(jumpRight,(self.rect.x,self.rect.y))
          #      else:
          #           if self.right:
          #                if self.isJump:
          #                     DISPLAYSURF.blit(jumpRight,(self.rect.x, self.rect.y))
          #                else:
          #                     DISPLAYSURF.blit(rstand,(self.rect.x,self.rect.y))
          #           elif self.left:
          #                if self.isJump:
          #                     DISPLAYSURF.blit(jumpLeft,(self.rect.x, self.rect.y))
          #                else:
          #                     DISPLAYSURF.blit(lstand,(self.rect.x,self.rect.y))
          #           else:
          #                DISPLAYSURF.blit(rstand,(self.rect.x,self.rect.y))
          #                self.shooting = False
          #           self.hitbox = (self.rect.x + 1, self.rect.y + 3, 60, 90)
          #      # Ibar = pygame.draw.rect(DISPLAYSURF, (255, 0, 0),(50,40,280,25))
          #      # Ibar2 = pygame.draw.rect(DISPLAYSURF, (255, 255, 0),(55,45,self.health,15))
          # else:
          #      self.speed = 0
          #      text = font.render('Naruto Wins', True, (255,100,10),(0,0,100))
          #      DISPLAYSURF.blit(text,(240,210))
          #      DISPLAYSURF.blit(pygame.image.load('./assets/images/DAMAGE 2_3.png'),(self.rect.x,self.rect.y))
     def move(self, DISPLAYSURF, target, round_over, keys): 
          BoundLeft = self.speed # Biên trái 
          BoundRight = 1000 - 80 - self.speed - 2 # Biên phải
          self.running = False
          self.attack_type = 0
          if self.alive == True and round_over == False:
               if self.player == 2 and self.ai == True:
                    if keys[self.input_dict['attack1']] or keys[self.input_dict['attack2']] or keys[self.input_dict['attack3']] :
                         self.attack(DISPLAYSURF, target) 
                    # Khi nhấn nút r    
                    if keys[self.input_dict['attack1']] :
                         self.attack_type = 1
                    elif keys[self.input_dict['attack2']] :
                         self.attack_type = 2
                    elif keys[self.input_dict['attack3']] :
                         self.attack_type = 3
                    # Khi người dùng chọn nút di di chuyển trái
                    if keys[self.input_dict['left']]  and self.rect.x > BoundLeft:
                         self.rect.x -= self.speed
                         self.left = True
                         self.right = False
                         self.running = True
                         self.isStanding = False
                    # Khi người dùng chọn nút di di chuyển phải
                    elif keys[self.input_dict['right']]  and self.rect.x < BoundRight: 
                         self.rect.x += self.speed
                         self.left = False
                         self.right = True
                         self.running = True
                         self.isStanding = False
                    else:
                         self.walkCount = 0
                         self.isStanding = True
                    # Khi người dùng chọn nút cách (Space)
                    if self.isJump == False:
                         if keys[self.input_dict['jump']] :
                              self.isJump = True
                              self.left = False
                              self.right = False
                              self.walkCount = 0
                    else:
                         if self.jumpHeight >= -7.5:
                              temp = 2.5
                              if self.jumpHeight < 0:
                                   temp = -2.5
                              self.rect.y -= (self.jumpHeight ** 2) * 0.5 * temp
                              self.jumpHeight -= 1
                         else:
                              self.isJump = False 
                              self.jumpHeight = 7.5
               else:
                    # Kiểm tra người chơi thứ nhất chế độ người với người
                    if self.player == 1:
                         # Khi người chơi nhấn nút r và t để tấn công
                         if keys[pygame.K_r] or keys[pygame.K_t] or keys[pygame.K_y]:
                              self.attack(DISPLAYSURF, target) 
                              # Khi nhấn nút r    
                              if keys[pygame.K_r]:
                                   self.attack_type = 1
                              if keys[pygame.K_t]:
                                   self.attack_type = 2
                              if keys[pygame.K_y]:
                                   self.attack_type = 3
                         # Khi người dùng chọn nút di di chuyển trái
                         if keys[pygame.K_a] and self.rect.x > BoundLeft:
                              self.rect.x -= self.speed
                              self.left = True
                              self.right = False
                              self.running = True
                              self.isStanding = False
                         # Khi người dùng chọn nút di di chuyển phải
                         elif keys[pygame.K_d] and self.rect.x < BoundRight: 
                              self.rect.x += self.speed
                              self.left = False
                              self.right = True
                              self.running = True
                              self.isStanding = False
                         else:
                              self.walkCount = 0
                              self.isStanding = True
                         # Khi người dùng chọn nút cách (Space)
                         if self.isJump == False:
                              if keys[pygame.K_w]:
                                   self.isJump = True
                                   self.left = False
                                   self.right = False
                                   self.walkCount = 0
                         else:
                              if self.jumpHeight >= -7.5:
                                   temp = 2.5
                                   if self.jumpHeight < 0:
                                        temp = -2.5
                                   self.rect.y -= (self.jumpHeight ** 2) * 0.5 * temp
                                   self.jumpHeight -= 1
                              else:
                                   self.isJump = False 
                                   self.jumpHeight = 7.5
                    # Kiểm tra người chơi thứ hai chế độ người với người
                    if self.player == 2:
                         # Khi người chơi nhấn nút r và t để tấn công
                         if keys[pygame.K_h] or keys[pygame.K_j] or keys[pygame.K_k]:
                              self.attack(DISPLAYSURF, target) 
                              # Khi nhấn nút r    
                              if keys[pygame.K_h]:
                                   self.attack_type = 1
                              if keys[pygame.K_j]:
                                   self.attack_type = 2
                              if keys[pygame.K_k]:
                                   self.attack_type = 3
                         # Khi người dùng chọn nút di di chuyển trái
                         if keys[pygame.K_LEFT] and self.rect.x > BoundLeft:
                              self.rect.x -= self.speed
                              self.left = True
                              self.right = False
                              self.running = True
                              self.isStanding = False
                         # Khi người dùng chọn nút di di chuyển phải
                         elif keys[pygame.K_RIGHT] and self.rect.x < BoundRight: 
                              self.rect.x += self.speed
                              self.left = False
                              self.right = True
                              self.running = True
                              self.isStanding = False
                         else:
                              self.walkCount = 0
                              self.isStanding = True
                         # Khi người dùng chọn nút cách (Space)
                         if self.isJump == False:
                              if keys[pygame.K_UP]:
                                   self.isJump = True
                                   self.left = False
                                   self.right = False
                                   self.walkCount = 0
                         else:
                              if self.jumpHeight >= -7.5:
                                   temp = 2.5
                                   if self.jumpHeight < 0:
                                        temp = -2.5
                                   self.rect.y -= (self.jumpHeight ** 2) * 0.5 * temp
                                   self.jumpHeight -= 1
                              else:
                                   self.isJump = False 
                                   self.jumpHeight = 7.5     
               if self.player == 1:
                    self.hitbox = (self.rect.x + 8, self.rect.y + 2, 68, 109)
               else:
                    self.hitbox = (self.rect.x + 12, self.rect.y + 2, 60, 115)
               # Đảm bảo nhân vật đối diện nhau
               if target.rect.centerx > self.rect.centerx:
                    self.flip = False
               else:
                    self.flip = True
               if self.attack_cooldown > 0:
                    self.attack_cooldown -= 1
               
     def shuriken(self,throwSpeed, shurikens, target, keys):
          if self.ai == False:
               #Phóng shuriken của người chơi thứ nhất
               if self.player == 1:
                    if self.health > 0 and target.health > 0:
                         if keys[pygame.K_SPACE] and throwSpeed == 0:
                              if self.speed > 0:
                                   self.shooting = True
                                   self.isStanding = False
                                   if self.flip:
                                        facing = -1
                                   else:
                                        facing = 1
                                   if len(shurikens) < 5:
                                        shurikens.append(wp.Weapons(round(self.rect.x + 60),round(self.rect.y + 30),40, 40, facing))
                    for shuriken in shurikens:
                         self.shooting = False
                         if target.health > 0:
                              if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > target.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < target.hitbox[1] + target.hitbox[3]:
                                   if shuriken.hitbox[0] + shuriken.hitbox[2] > target.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < target.hitbox[0] + target.hitbox[2]:    
                                        target.Hit()
                                        target.hit = True
                                        hitsong.play()
                                        shurikens.pop(shurikens.index(shuriken))
                         else:
                              target.speed = 0
                         if shuriken.x < 1000 and shuriken.x > 0:
                              shuriken.x += shuriken.vel
                         else:
                              shurikens.pop(shurikens.index(shuriken))
               #Phóng shuriken của người chơi thứ hai
               if self.player == 2:
                    if self.health > 0 and target.health > 0:
                         if keys[pygame.K_l] and throwSpeed == 0:
                              if self.speed > 0:
                                   self.shooting = True
                                   self.isStanding = False
                                   if self.flip:
                                        facing = -1
                                   else:
                                        facing = 1
                                   if len(shurikens) < 5:
                                        shurikens.append(wp.Weapons(round(self.rect.x + 60),round(self.rect.y + 30),40, 40, facing))
                    for shuriken in shurikens:
                         self.shooting = False
                         if target.health > 0:
                              if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > target.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < target.hitbox[1] + target.hitbox[3]:
                                   if shuriken.hitbox[0] + shuriken.hitbox[2] > target.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < target.hitbox[0] + target.hitbox[2]:    
                                        target.Hit()
                                        target.hit = True
                                        hitsong.play()
                                        shurikens.pop(shurikens.index(shuriken))
                         else:
                              target.speed = 0
                         if shuriken.x < 1000 and shuriken.x > 0:
                              shuriken.x += shuriken.vel
                         else:
                              shurikens.pop(shurikens.index(shuriken))
          else:
               if self.health > 0 and target.health > 0:
                    if keys[self.input_dict['right']] and throwSpeed == 0:
                         if self.speed > 0:
                              self.shooting = True
                              self.isStanding = False
                              if self.flip:
                                   facing = -1
                              else:
                                   facing = 1
                              if len(shurikens) < 5:
                                   shurikens.append(wp.Weapons(round(self.rect.x + 60),round(self.rect.y + 30),40, 40, facing))
               for shuriken in shurikens:
                    self.shooting = False
                    if target.health > 0:
                         if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > target.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < target.hitbox[1] + target.hitbox[3]:
                              if shuriken.hitbox[0] + shuriken.hitbox[2] > target.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < target.hitbox[0] + target.hitbox[2]:
                                   target.Hit()
                                   target.hit = True
                                   hitsong.play()
                                   shurikens.pop(shurikens.index(shuriken))
                    else:
                         target.speed = 0
                    if shuriken.x < 1000 and shuriken.x > 0:
                         shuriken.x += shuriken.vel
                    else:
                         shurikens.pop(shurikens.index(shuriken))

     def loadimg(self, sprites_sheet, animation_steps):
          animation_list = []
          for y, animation in enumerate(animation_steps):
               temp_img_list = []
               for i in range (animation):
                    temp_img = sprites_sheet.subsurface(i * self.size, y * self.size, self.size, self.size)
                    temp_img_list.append(pygame.transform.scale(temp_img,(self.size * self.image_scale, self.size * self.image_scale)))
               animation_list.append(temp_img_list)
          return animation_list
     def scale(self, val):
        # divide by 60 is so I can pass same values as before scaling was implemented
          monitor_size = (pygame.display.Info().current_w,pygame.display.Info().current_h)
          self.screen_ratio = (16,9)
          horiz = monitor_size[0]/self.screen_ratio[0]
          vert = monitor_size[1]/self.screen_ratio[1]
          self.scale_factor = min(horiz,vert)
          if isinstance(val,(int,float)):
               return math.floor((val/60)*self.scale_factor)
          if isinstance(val,(list,tuple)):
               return [math.floor((i/60)*self.scale_factor) for i in val]
     def attack(self,DISPLAYSURF, target):
         if self.attack_cooldown == 0:
              self.attacking = True
         if self.alive == True:
               self.attacking = True
               attacking_rect = pygame.Rect(self.rect.centerx - (1.6 * self.rect.width * self.flip),self.rect.y, 1.2 * self.rect.width,self.rect.height)
               pygame.draw.rect(DISPLAYSURF,(0,255,0),attacking_rect)
               if attacking_rect.colliderect(target.rect):
                    target.health -= 10
                    if target.alive == True:
                         target.hit = True
                    else:
                         target.hit = False
               # pygame.display.update()
     def update (self): 
          if self.health <=0:
               self.health = 0
               self.alive = False
               self.update_action(3) 
               self.offset[1] = 1
          elif self.hit == True:
               hitsong.play()
               self.update_action(2)
               self.offset[1] = 8
          elif self.attacking == True:
               if self.attack_type == 1:
                    self.update_action(4)
                    self.offset[1] = 8
               elif self.attack_type == 2:
                    self.update_action(5)
                    self.offset[1] = 10
               elif self.attack_type == 3:
                    self.update_action(6)
                    self.offset[1] = 22
          elif self.running == True:
               self.update_action(1)
               self.offset[1] = 18
          else:
               self.offset[1] = 28
               self.update_action(0)
          animation_cooldown = 50
          self.image = self.animation_list[self.action][self.frame_index]
          if pygame.time.get_ticks() - self.update_time > animation_cooldown:
               self.frame_index += 1
               self.update_time = pygame.time.get_ticks()
          if self.frame_index >= len(self.animation_list[self.action]):
               if self.alive == False:
                    self.frame_index = len(self.animation_list[self.action]) - 1
               else:
                    self.frame_index = 0
                    if self.action == 4 or self.action == 5 or self.action == 6:
                         self.attacking = False
                         self.attack_cooldown = 50
                    if self.action == 2:
                         self.hit = False
                         self.attacking = False
                    if self.action == 3:
                         self.hit = False
                         self.attacking = False
                         self.alive = False
          
     def update_action(self, new_action):
          if new_action != self.action:
               self.action = new_action
               self.frame_index = 0
               self.update_time = pygame.time.get_ticks()

     def Hit(self):
          if self.health > 0:
               self.health -= 10
          else:
               print("Itachi died")
     