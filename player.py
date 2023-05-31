#Import thư viện, module
import pygame
import math
import weapons as wp
# Khởi tạo pygame
pygame.init()

#Khởi tạo âm thanh
hitsound = pygame.mixer.Sound('./assets/musics/hit.wav')
shurikensong = pygame.mixer.Sound('./assets/musics/shuriken.wav')

#Lớp nhân vật
class Player:

     #Hàm khởi tạo nhân vật
     #Input: loại player, tọa độ, hướng quay, kích thước, phần bù trừ tọa độ, ảnh, số bước di chuyển của mỗi action, có phải bot hay không, tên nhân vật, icon nhân vật
     #Ouput: Không có
     def __init__(self, PLAYER ,X, Y, FLIP, DATA, SPRITES_SHEET, ANIMATION_STEPS, AI, NAME, ICON):
          self.name = NAME
          self.icon = ICON
          #P1 hay P2
          self.player = PLAYER
          #Kích thước
          self.size = DATA[0]
          self.offset = DATA[2]
          #Độ phóng ảnh
          self.image_scale = DATA[1]
          self.rect = pygame.Rect((X,Y,80,115))
          #Danh sách hoạt ảnh
          self.animation_list = self.loadimg(SPRITES_SHEET, ANIMATION_STEPS)
          self.action = 0 #0 đứng ,1 chạy, 2 bị gây dame, 3 chết, 4 loại tấn công thứ 1, 5 loại tấn công thứ 2, 6 loại tấn công thứ 3
          self.frame_index = 0 #index hoạt ảnh của action
          self.image = self.animation_list[self.action][self.frame_index]
          self.speed = 10 # Tốc độ di chuyển
          self.running = False
          self.isJump = False 
          self.shooting = False
          self.jumpHeight = 7.5 #Chiều cao nhảy
          self.attack_type = 0 # Loại attack
          self.hit = False
          self.flip = FLIP
          self.update_time = pygame.time.get_ticks()
          self.attacking = False
          self.hitbox = (self.rect.x + 16, self.rect.y, 55, 116)
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
          #Cờ kiểm tra AI
          self.ai = AI
     #Hàm vẽ icon, vẽ ảnh nhân vật
     #Input: Màn hình chính
     #Output: Không có
     def draw(self, DISPLAYSURF):
          img = pygame.transform.flip(self.image, self.flip, False)
          # pygame.draw.rect(DISPLAYSURF,(255,255,0), self.hitbox, 2)
          if self.player == 1:
               DISPLAYSURF.blit(self.icon,(10,10))
          else:
               DISPLAYSURF.blit(self.icon,(900,10))
          # pygame.draw.rect(DISPLAYSURF,(255,0,0), self.rect)
          DISPLAYSURF.blit(img,(self.rect.x - (self.offset[0] * self.image_scale),self.rect.y-(self.offset[1] * self.image_scale)))
     #Hàm xử lý, cập nhật hoạt ảnh của nhân vật
     #Input: Màn hình chính, target của nhân vật, cờ kết thúc 1 round, các keys input
     #Output: Không có
     def move(self, DISPLAYSURF, target, round_over, keys): 
          BoundLeft = self.speed # Biên trái 
          BoundRight = 1000 - 80 - self.speed - 2 # Biên phải
          self.running = False
          self.attack_type = 0 #Loại tấn công
          if self.alive == True and round_over == False:
               if self.player == 2 and self.ai == True:
                    if keys[self.input_dict['attack1']] or keys[self.input_dict['attack2']] or keys[self.input_dict['attack3']] :
                         if keys[self.input_dict['attack1']] :
                              if self.name == "NineTails":
                                   if self.flip:
                                        self.attack(DISPLAYSURF, target, 1.7, 1.7) 
                                   else:
                                        self.attack(DISPLAYSURF, target, 1.7, 0.4)
                              else: 
                                   if self.flip:
                                        self.attack(DISPLAYSURF, target, 1.25, 1.2) 
                                   else:
                                        self.attack(DISPLAYSURF, target, 1.07, 1.2) 
                              self.attack_type = 1
                         elif keys[self.input_dict['attack2']] :
                              if self.name == "NineTails":
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 1.4, 1.2) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1.4, 1.2)
                              else: 
                                   if self.flip:
                                        self.attack(DISPLAYSURF, target, 1, 0.95) 
                                   else:
                                        self.attack(DISPLAYSURF, target, 0.8, 0.95)
                              self.attack_type = 2
                         elif keys[self.input_dict['attack3']] :
                              if self.name == "NineTails":
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 2, 2.2) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 2, 2.2)
                              else: 
                                   if self.flip:
                                        self.attack(DISPLAYSURF, target, 1.2, 1.15) 
                                   else:
                                        self.attack(DISPLAYSURF, target, 1, 0.95)
                              self.attack_type = 3
                    # Khi người dùng chọn nút di di chuyển trái
                    if keys[self.input_dict['left']]  and self.rect.x > BoundLeft:
                         self.rect.x -= self.speed
                         self.left = True
                         self.running = True
                    # Khi người dùng chọn nút di di chuyển phải
                    elif keys[self.input_dict['right']]  and self.rect.x < BoundRight: 
                         self.rect.x += self.speed
                         self.left = False
                         self.running = True
                    
     
                    if self.isJump == False:
                         #Nhảy
                         if keys[self.input_dict['jump']] :
                              self.isJump = True
                              self.left = False
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
                         # Khi người chơi nhấn nút r và t, y để tấn công
                         if keys[pygame.K_r] or keys[pygame.K_t] or keys[pygame.K_y]:
                              # Khi nhấn nút r    
                              if keys[pygame.K_r]:
                                   if self.name == "NineTails":
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 1.7, 1.7) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1.7, 0.4)
                                   else: 
                                        if self.flip == False:
                                             self.attack(DISPLAYSURF, target, 1.18, 1.6) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1.25, 1.35) 
                                   self.attack_type = 1
                              # Khi nhấn nút t
                              if keys[pygame.K_t]:
                                   if self.name == "NineTails":
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 1.4, 1.4) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1.4, 1.4)
                                   else: 
                                        if self.flip == False:
                                             self.attack(DISPLAYSURF, target, 0.93, 1.6) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1, 1.08) 
                                   self.attack_type = 2
                              # Khi nhấn nút y
                              if keys[pygame.K_y]:
                                   if self.name == "NineTails":
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 2, 2.2) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 2, 2.2)
                                   else: 
                                        if self.flip == False:
                                             self.attack(DISPLAYSURF, target, 0.65, 1.6) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 0.65, 0.83)
                                   self.attack_type = 3

                         # Khi người dùng chọn nút di di chuyển trái
                         if keys[pygame.K_a] and self.rect.x > BoundLeft:
                              self.rect.x -= self.speed
                              self.left = True
                              self.running = True

                         # Khi người dùng chọn nút di di chuyển phải
                         elif keys[pygame.K_d] and self.rect.x < BoundRight: 
                              self.rect.x += self.speed
                              self.left = False
                              self.running = True
                         
                         # Khi người dùng chọn nút cách (Space)
                         if self.isJump == False:
                              #Nhấn phím w với P1 để nhảy
                              if keys[pygame.K_w]:
                                   self.isJump = True
                                   self.left = False
                         else:
                              # Tạo độ rơi khi nhảy của nhân vật
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
                         # Khi người chơi nhấn nút h và j, k để tấn công
                         if keys[pygame.K_h] or keys[pygame.K_j] or keys[pygame.K_k]:
                              # Khi nhấn nút h    
                              if keys[pygame.K_h]:
                                   if self.name == "NineTails":
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 1.7, 1.7) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1.7, 0.4)
                                   else: 
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 1.25, 1.2) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1.07, 1.2) 
                                   self.attack_type = 1
                              # Khi nhấn nút j
                              if keys[pygame.K_j]:
                                   if self.name == "NineTails":
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 1.4, 1.2) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1.4, 1.2)
                                   else: 
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 1, 0.95) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 0.8, 0.95) 
                                   self.attack_type = 2
                              # Khi nhấn nút k
                              if keys[pygame.K_k]:
                                   if self.name == "NineTails":
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 2, 2.2) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 2, 2.2)
                                   else: 
                                        if self.flip:
                                             self.attack(DISPLAYSURF, target, 1.2, 1.15) 
                                        else:
                                             self.attack(DISPLAYSURF, target, 1, 0.95) 
                                   self.attack_type = 3
                         # Khi người dùng chọn nút di di chuyển trái
                         if keys[pygame.K_LEFT] and self.rect.x > BoundLeft:
                              self.rect.x -= self.speed
                              self.left = True
                              self.running = True
                         # Khi người dùng chọn nút di di chuyển phải
                         elif keys[pygame.K_RIGHT] and self.rect.x < BoundRight: 
                              self.rect.x += self.speed
                              self.left = False
                              self.running = True
                         
                         # Khi người dùng chọn nút cách (Space)
                         if self.isJump == False:
                              if keys[pygame.K_UP]:
                                   self.isJump = True
                                   self.left = False
                         else:
                              # Tạo độ rơi khi nhảy của nhân vật
                              if self.jumpHeight >= -7.5:
                                   temp = 2.5
                                   if self.jumpHeight < 0:
                                        temp = -2.5
                                   self.rect.y -= (self.jumpHeight ** 2) * 0.5 * temp
                                   self.jumpHeight -= 1
                              else:
                                   self.isJump = False 
                                   self.jumpHeight = 7.5  
               #Cập nhật hitbox   
               self.hitbox = (self.rect.x + 16, self.rect.y, 55, 116)     
               # Đảm bảo nhân vật đối diện nhau
               if target.rect.centerx > self.rect.centerx:
                    self.flip = False
               else:
                    self.flip = True
               if self.name == "NineTails":
                    self.hitbox = (self.rect.x + 13, self.rect.y, 70, 116)    
                    if self.flip == True:
                         self.offset[0] = 105
                    else:
                         self.offset[0] = 40
               #Nếu biết cooldown lớn hơn 0 sẽ trừ 1 -> Đảm bảo nhân vật không spam skill liên tục
               if self.attack_cooldown > 0:
                    self.attack_cooldown -= 1
     #Hàm xử lý, cập nhật liên quan tới hoạt ảnh phóng shuriken
     #Input: tốc độ phóng, danh sách các shurikens, đối thủ, danh sách keys người dùng nhập
     #Output: Không có        
     def shuriken(self,throwSpeed, shurikens, target, keys):
          if self.ai == False:
               #Phóng shuriken của người chơi thứ nhất
               if self.player == 1:
                    if self.health > 0 and target.health > 0:
                         #Phóng phi tiêu nếu người chơi P1 nhấn nút "Space"
                         if keys[pygame.K_SPACE] and throwSpeed == 0:
                              shurikensong.play()
                              if self.speed > 0:
                                   self.shooting = True
                                   if self.flip:
                                        facing = -1
                                   else:
                                        facing = 1
                                   if len(shurikens) < 5:
                                        shurikens.append(wp.Weapons(round(self.rect.x + 60),round(self.rect.y + 30),40, 40, facing))
                    for shuriken in shurikens:
                         self.shooting = False
                         if target.health > 0:
                              #Tính toán va chạm của hitbox shuriken với hitbox người chơi
                              if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > target.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < target.hitbox[1] + target.hitbox[3]:
                                   if shuriken.hitbox[0] + shuriken.hitbox[2] > target.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < target.hitbox[0] + target.hitbox[2]:    
                                        target.Hit()
                                        target.hit = True
                                        hitsound.play()
                                        shurikens.pop(shurikens.index(shuriken))
                         else:
                              target.speed = 0 #Chết không cho nhân vật chạy hay làm gì khác
                         if shuriken.x < 1000 and shuriken.x > 0:
                              shuriken.x += shuriken.vel
                         else:
                              shurikens.pop(shurikens.index(shuriken))
               #Phóng shuriken của người chơi thứ hai
               if self.player == 2:
                    if self.health > 0 and target.health > 0:
                         #Phóng phi tiêu nếu người chơi P2 nhấn nút "l"
                         if keys[pygame.K_l] and throwSpeed == 0:
                              shurikensong.play()
                              if self.speed > 0:
                                   self.shooting = True
                                   if self.flip:
                                        facing = -1
                                   else:
                                        facing = 1
                                   if len(shurikens) < 5:
                                        #Tạo shuriken thêm vào danh sách
                                        shurikens.append(wp.Weapons(round(self.rect.x + 60),round(self.rect.y + 30),40, 40, facing))
                    for shuriken in shurikens:
                         self.shooting = False
                         if target.health > 0:
                              #Tính toán va chạm của hitbox shuriken với hitbox người chơi
                              if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > target.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < target.hitbox[1] + target.hitbox[3]:
                                   if shuriken.hitbox[0] + shuriken.hitbox[2] > target.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < target.hitbox[0] + target.hitbox[2]:    
                                        target.Hit()
                                        target.hit = True
                                        hitsound.play()
                                        shurikens.pop(shurikens.index(shuriken))
                         else:
                              target.speed = 0
                         if shuriken.x < 1000 and shuriken.x > 0:
                              shuriken.x += shuriken.vel
                         else:
                              shurikens.pop(shurikens.index(shuriken))
          else:
               if self.health > 0 and target.health > 0:
                    if keys[self.input_dict['shurikens']] and throwSpeed == 0:
                         #Âm thanh khi phóng phi tiêu
                         shurikensong.play()
                         if self.speed > 0:
                              self.shooting = True
                              #Đảm bảo phi tiêu sẽ luôn bay về hướng target
                              if self.flip:
                                   facing = -1
                              else:
                                   facing = 1
                              if len(shurikens) < 5:
                                   shurikens.append(wp.Weapons(round(self.rect.x + 60),round(self.rect.y + 30),40, 40, facing))
               for shuriken in shurikens:
                    self.shooting = False
                    if target.health > 0:
                         #Tính toán va chạm của hitbox shuriken với hitbox người chơi
                         if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > target.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < target.hitbox[1] + target.hitbox[3]:
                              if shuriken.hitbox[0] + shuriken.hitbox[2] > target.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < target.hitbox[0] + target.hitbox[2]:
                                   target.Hit()
                                   target.hit = True
                                   hitsound.play()
                                   shurikens.pop(shurikens.index(shuriken))
                    else:
                         target.speed = 0
                    #Đảm bảo shuriken sẽ xuất hiện trong màn hình game chính
                    if shuriken.x < 1000 and shuriken.x > 0:
                         shuriken.x += shuriken.vel
                    #Nếu vượt ngoài màn hình game chính tiến hành xóa bỏ shuriken
                    else:
                         shurikens.pop(shurikens.index(shuriken))
     #Hàm xử lý, cắt sprites sheet thành những ảnh nhỏ liên tiếp đưa vào trong một danh sách
     #Input: sprites_sheet, các bước di hoạt động của 1 action
     #Output: Không có
     def loadimg(self, sprites_sheet, animation_steps):
          animation_list = []
          for y, animation in enumerate(animation_steps):
               temp_img_list = []
               for i in range (animation):
                    #Chia nhỏ srpites sheet thành từng ảnh nhỏ cắt theo tọa độ
                    temp_img = sprites_sheet.subsurface(i * self.size, y * self.size, self.size, self.size)
                    #Phóng các ảnh đã chia theo self.image_scale mà người dùng đã nhập
                    temp_img_list.append(pygame.transform.scale(temp_img,(self.size * self.image_scale, self.size * self.image_scale)))
               animation_list.append(temp_img_list)
          return animation_list
     
     #Hàm tỷ lệ hóa giá trị đầu vào dựa trên tỷ lệ màn hình hiện tại và tỷ lệ màn hình mong muốn
     #Input: giá trị
     #Output: Không có
     def scale(self, val):
          monitor_size = (pygame.display.Info().current_w,pygame.display.Info().current_h)
          self.screen_ratio = (16,9)
          horiz = monitor_size[0]/self.screen_ratio[0]
          vert = monitor_size[1]/self.screen_ratio[1]
          self.scale_factor = min(horiz,vert)
          if isinstance(val,(int,float)):
               return math.floor((val/60)*self.scale_factor)
          if isinstance(val,(list,tuple)):
               return [math.floor((i/60)*self.scale_factor) for i in val]
     
     #Hàm xử lý hitbox đánh nhau, trừ máu
     #Input: target, tọa độ x,y
     #Output: Không có
     def attack(self, DISPLAYSURF, target, x, y):
          self.attacking = True
          if self.attack_cooldown == 0:
               self.attacking = True
               if self.alive == True:
                         self.attacking = True
                         attacking_rect = pygame.Rect(self.rect.centerx - (y * self.rect.width * self.flip),self.rect.y, x * self.rect.width,self.rect.height)
                         # pygame.draw.rect(DISPLAYSURF,(0,255,0),attacking_rect)
                         if attacking_rect.colliderect(target.rect):
                              target.health -= 7
                              if target.alive == True:
                                   target.hit = True
                              else:
                                   target.hit = False
                         # pygame.display.update()

     #Hàm cập nhật hoạt ảnh: chết, chạy, ra chiêu, trúng chiêu, đứng,....
     #Input: target, tọa độ x,y
     #Output: Không có          
     def update (self): 
          if self.health <=0:
               self.health = 0
               self.alive = False
               self.update_action(3)#3 Chết 
               self.offset[1] = 1
          elif self.hit == True:
               hitsound.play()
               self.update_action(2)#2 bị gây dame
               self.offset[1] = 8
          elif self.attacking == True:
               if self.attack_type == 1:
                    self.update_action(4)#4 Attack loại 1
                    self.offset[1] = 8
               elif self.attack_type == 2:
                    self.update_action(5)#5 Attack loại 2
                    self.offset[1] = 10
               elif self.attack_type == 3:
                    self.update_action(6)#6 Attack loại 3
                    self.offset[1] = 22
          elif self.running == True:
               self.update_action(1)
               self.offset[1] = 18 #1 Chạy
          else:
               self.offset[1] = 28
               self.update_action(0) #0 Đứng
          #Đếm ngược animation
          animation_cooldown = 50
          self.image = self.animation_list[self.action][self.frame_index]
          if pygame.time.get_ticks() - self.update_time > animation_cooldown:
               self.frame_index += 1
               self.update_time = pygame.time.get_ticks()
          #Kết thúc chuỗi hoạt ảnh
          if self.frame_index >= len(self.animation_list[self.action]):
               #Nếu nhân vật chết
               if self.alive == False:
                    self.frame_index = len(self.animation_list[self.action]) - 1
               #Nếu nhân vật sống
               else:
                    self.frame_index = 0
                    if self.action == 4 or self.action == 5 or self.action == 6:
                         self.attacking = False
                         self.attack_cooldown = 5
                    if self.action == 2:
                         self.hit = False
                         self.attacking = False
                    if self.action == 3:
                         self.hit = False
                         self.attacking = False
                         self.alive = False
     #Hàm cập nhật action
     #Input: action mới
     #Output: Không có   
     def update_action(self, new_action):
          if new_action != self.action:
               self.action = new_action
               self.frame_index = 0
               self.update_time = pygame.time.get_ticks()

     #Hàm xử lý trừ máu khi dính shuriken
     #Input: action mới
     #Output: Không có
     def Hit(self):
          if self.health > 0:
               self.health -= 2
     