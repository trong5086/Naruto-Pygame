#Import thư viện
import pygame
import random

class Player:
     # Khởi tạo AI Player với danh sách phím nhập, P1, P2 (bot), giải thuật sử dụng là heuristic
     def __init__(self, input_dict, player1, player2, ai_scheme = 'heuristic'):
          #Sử dụng giải thuật heuristic
          self.ai_scheme = ai_scheme

          self.playera = player1
          self.playerb = player2

          self.input_dict = input_dict
          #object gồm key:keys nhập từ bàn phím, value:0 (không nhập từ phím) hoặc 1 (nhập từ phím)
          self.ai_key_dict = {
               self.input_dict['jump']:0,
               self.input_dict['left']:0,
               self.input_dict['right']:0,
               self.input_dict['down']:0,
               self.input_dict['attack1']:0,
               self.input_dict['attack2']:0,
               self.input_dict['attack3']:0,
               self.input_dict['shurikens']:0
               }
          #Lần lượt tạo ra danh sách số lần nhập keys từ phím 
          self.walk_left = [self.input_dict['left']]*10
          self.walk_right = [self.input_dict['right']]*10
          self.attack1 = [self.input_dict['attack1']]
          self.attack2 = [self.input_dict['attack2']]
          self.attack3 = [self.input_dict['attack3']]
          self.shurikens = [self.input_dict['shurikens']]*4
          self.attack1_left = [self.input_dict['left']]*3 + [None]*3 + [self.input_dict['left']]*5 + self.attack1
          self.attack1_right = [self.input_dict['right']]*3 + [None]*3 + [self.input_dict['right']]*5 + self.attack1
          self.attack2_left = [self.input_dict['left']]*3 + [None]*3 + [self.input_dict['left']]*5 + self.attack2
          self.attack2_right = [self.input_dict['right']]*3 + [None]*3 + [self.input_dict['right']]*5 + self.attack2
          self.attack3_left = [self.input_dict['left']]*3 + [None]*3 + [self.input_dict['left']]*5 + self.attack3
          self.attack3_right = [self.input_dict['right']]*3 + [None]*3 + [self.input_dict['right']]*5 + self.attack3
          self.shurikens_left = [self.input_dict['left']]*3 + [None]*3 + [self.input_dict['left']]*5 + self.shurikens
          self.shurikens_right = [self.input_dict['right']]*3 + [None]*3 + [self.input_dict['right']]*5 + self.shurikens
          self.jump_left = [[self.input_dict['jump'],self.input_dict['left']]] + self.walk_left
          self.jump_right = [[self.input_dict['jump'],self.input_dict['right']]] + self.walk_right
          self.jump_left_downstrike = self.jump_left + self.walk_left*2 + [self.input_dict['down']]
          self.jump_right_downstrike = self.jump_right + self.walk_right*2 + [self.input_dict['down']]
          self.down_strike = [self.input_dict['jump']]*5 + [self.input_dict['down']]

          #Index sequence
          self.sequence_index = 0

          #Danh sách sequence
          self.sequence_list = [
          self.walk_left, 
          self.walk_right,
          self.attack1_left,
          self.attack1_right,
          self.attack2_left,
          self.attack2_right,
          self.attack3_left,
          self.attack3_right,
          self.shurikens_left,
          self.shurikens_right,
          self.attack1, self.attack2, self.attack3,
          self.shurikens, self.attack1, self.attack2,
          self.jump_left_downstrike,
          self.jump_right_downstrike,
          self.down_strike
          ]
          self.sequence = self.walk_left
         

     # Sequence (chứa các random input là các key tùy vào các tình huống phân case ở hàm choose_heuristic())
     # Input: Không có
     # Output: trả về danh sách các sequence 
     def heuristics(self):
          if self.sequence_index >= len(self.sequence)-1:
               self.sequence = self.choose_heuristic()
               self.sequence_index = 0
          else:
               self.sequence_index += 1
          #Input keys trả về từ danh sách sequence
          input = self.sequence[self.sequence_index]
          #Copy object self.ai_key_dict
          ai_key_dict_copy = self.ai_key_dict.copy()
          
          #Input nếu không phải list sẽ gán list cho nó
          if not isinstance(input,list):
               input = [input]
          #Duyệt danh sách input keys
          for i in input:
               # gáng value bằng 1 cho key nằm trong input
               ai_key_dict_copy[i] = 1
          
          return ai_key_dict_copy
     # Đưa ra sequence dựa vào các case
     # Input: Không có
     # Output: Danh sách các input keys tùy vào các case ở bên dưới
     def choose_heuristic(self):
          sequence = [None]
          #Case Bot trên đầu nhân vật P1
          if self.is_on_top():
               possible_sequences = [self.down_strike,self.walk_right,self.walk_left]
               sequence = random.sample(possible_sequences,1)[0]

          #Case Bot dưới nhân vật P1
          elif self.is_under():
               possible_sequences = [self.walk_left*2,self.walk_right*2]
               sequence = random.sample(possible_sequences,1)[0]

          #Case Bot ở xa nhân vật P1   
          elif self.is_far():
               #Case Bot bên trái nhân vật P1
               if self.is_left():
                    sequence = self.walk_left
               #Case Bot bên phải nhân vật P1
               else:
                    sequence = self.walk_right
          #Case Bot ở gần nhân vật P1
          elif self.is_close():
               #Case Bot bên trái nhân vật P1
               if self.is_left():
                    sequence = [[self.input_dict['left'],self.input_dict['attack1'],self.input_dict['attack3'],self.input_dict['attack2'], self.input_dict['shurikens'], self.input_dict['shurikens']]]
               #Case Bot bên phải nhân vật P1
               else:
                    sequence = [[self.input_dict['right'],self.input_dict['attack1'],self.input_dict['attack2'],self.input_dict['attack3'], self.input_dict['shurikens'], self.input_dict['shurikens']]]
                    
          #Case Bot bên trái với khoảng cách vừa phải
          elif self.is_left() & self.is_medium():
               possible_sequences = [self.jump_left_downstrike, self.shurikens, self.jump_left_downstrike,self.walk_left]
               sequence = random.sample(possible_sequences,1)[0]

          #Case Bot bên phải với khoảng cách vừa phải
          elif self.is_right() & self.is_medium():
               possible_sequences = [self.jump_right_downstrike, self.shurikens, self.jump_right_downstrike,self.walk_right]
               sequence = random.sample(possible_sequences,1)[0]
          return sequence
     
     # Kiểm tra bot có bên trái P1 hay không ? 
     # Input: Không có
     # Output: Nếu tọa độ x (tính từ giữa) của bot > P1 thì return True, ngược lại return False
     def is_left(self):
          return self.playera.rect.centerx < self.playerb.rect.centerx
     
     # Kiểm tra  bot có bên phải P1 hay không ? 
     # Input: Không có
     # Output: Nếu tọa độ x (tính từ giữa) của bot < P1 thì return True, ngược lại return False
     def is_right(self):
          return self.playera.rect.centerx > self.playerb.rect.centerx
     
     # Kiểm tra  bot có đang ở xa người chơi hay không ? 
     # Input: Khoảng cách để xác định
     # Output: Nếu tọa độ x (tính từ giữa) của P1 - Bot mà lớn hơn hàm scale(tính toán khoảng cách của nhân vật P1 dựa trên tỷ lệ màn hình thực tế và màn hình game) thì return True, ngược lại return False
     def is_far(self, distance = 160):
          return abs(self.playera.rect.centerx - self.playerb.rect.centerx) > self.playera.scale(distance)

     # Kiểm tra  bot có đang ở không xa không gần người chơi hay không ? 
     # Input: Khoảng cách xa để xác định, khoảng cách gần để xác định
     # Output: Nếu không xa, không gần thì return True, ngược lại return False
     def is_medium(self, low_distance = 100, high_distance = 160):
          return (not self.is_far(high_distance)) & (not self.is_close(low_distance))

     # Kiểm tra  bot có đang ở gần người chơi hay không ? 
     # Input: Khoảng cách để xác định
     # Output: Nếu tọa độ x (tính từ giữa) của P1 - Bot mà bé hơn hàm scale(tính toán khoảng cách của nhân vật P1 dựa trên tỷ lệ màn hình thực tế và màn hình game) thì return True, ngược lại return False  
     def is_close(self, distance = 100):
          return abs(self.playera.rect.centerx - self.playerb.rect.centerx) < self.playera.scale(distance)

     # Kiểm tra  bot có đang ở phía trên P1 hay không ? 
     # Input: Không có
     # Output: Nếu tọa độ y (tính từ giữa) của Bot bé hơn P1 và P1 vs Bot gần nhau với khoảng cách 20 sẽ return True, ngược lại False   
     def is_on_top(self):
          return (self.playerb.rect.centery < self.playera.rect.centery) & self.is_close(20)
        
     # Kiểm tra  bot có đang ở phía dưới P1 hay không ? 
     # Input: Không có
     # Output: Nếu tọa độ y (tính từ giữa) của Bot lớn hơn P1 và P1 vs Bot gần nhau với khoảng cách 50 sẽ return True, ngược lại False 
     def is_under(self):
          return (self.playerb.rect.centery > self.playera.rect.centery) & self.is_close(50)


        
     