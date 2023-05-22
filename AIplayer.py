import pygame
import weapons as wp
import random
class Player:
     def __init__(self, input_dict, player1, player2, ai_scheme = 'heuristic'):

          self.ai_scheme = ai_scheme
          self.playera = player1
          self.playerb = player2

          self.input_dict = input_dict
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
          if ai_scheme != 'random_input':
                self.walk_left = [self.input_dict['left']]*10
                self.walk_right = [self.input_dict['right']]*10
                self.attack1 = [self.input_dict['attack1']]
                self.attack2 = [self.input_dict['attack2']]
                self.attack3 = [self.input_dict['attack3']]
                self.shurikens = [self.input_dict['shurikens']]
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
                
                self.sequence_index = 0
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
                self.sequence_break = False
                self.avoiding = False
     def get_input(self):
            if self.ai_scheme == 'random_input':
                return self.random_input()
            elif self.ai_scheme == 'random_sequence':
                return self.random_sequence()
            elif self.ai_scheme == 'heuristic':
                return self.heuristics()
     def random_input(self):
          ai_key_dict_copy = self.ai_key_dict.copy()
          ai_key_dict_copy[random.sample(self.ai_key_dict.keys(),1)[0]] = 1
          return ai_key_dict_copy
        
     def random_sequence(self):
            if self.sequence_index == len(self.sequence)-1:
                self.sequence = random.sample(self.sequence_list,1)[0]
                self.sequence_index = 0
            else:
                self.sequence_index += 1
            input = self.sequence[self.sequence_index]
            ai_key_dict_copy = self.ai_key_dict.copy()
            ai_key_dict_copy[input] = 1
            return ai_key_dict_copy
        
     def heuristics(self):
          if self.sequence_index >= len(self.sequence)-1:
               self.sequence = self.choose_heuristic()
               if self.sequence_break is True:
                    self.sequence_break = False
               self.sequence_index = 0
          else:
               self.sequence_index += 1
          input = self.sequence[self.sequence_index]
          ai_key_dict_copy = self.ai_key_dict.copy()

          if not isinstance(input,list):
               input = [input]
          for i in input:
               ai_key_dict_copy[i] = 1
          
          return ai_key_dict_copy

     def choose_heuristic(self):
          sequence = [None]
          # is over or under
          if self.is_on_top():
               possible_sequences = [self.down_strike,self.walk_right,self.walk_left]
               sequence = random.sample(possible_sequences,1)[0]
          elif self.is_under():
               possible_sequences = [self.walk_left*2,self.walk_right*2]
               sequence = random.sample(possible_sequences,1)[0]
          # far away
          elif self.is_far():
               if self.is_left():
                    sequence = [self.walk_left, self.input_dict['shurikens']]
               else:
                    sequence = [self.walk_right, self.input_dict['shurikens']]
          # close
          elif self.is_close():
               if self.is_left():
                    sequence = [[self.input_dict['left'],self.input_dict['attack1'],self.input_dict['attack3']]]
               else:
                    sequence = [[self.input_dict['right'],self.input_dict['attack1'],self.input_dict['attack2']]]
          # medium distance
          elif self.is_left() & self.is_medium():
               possible_sequences = [self.jump_left_downstrike,self.walk_left]
               sequence = random.sample(possible_sequences,1)[0]
          elif self.is_right() & self.is_medium():
               possible_sequences = [self.jump_right_downstrike,self.walk_right]
               sequence = random.sample(possible_sequences,1)[0]
          return sequence

     def _avoid(self):
            self.sequence_index = 0
            self.sequence_break = True
            self.avoiding = True
            if self.is_left():
                if self.near_right_edge():
                    possible_sequences = [self.walk_left*3,self.jump_left]
                    sequence = random.sample(possible_sequences,1)[0] 
                    return sequence
                else:
                    self.walk_left
            if self.is_right():
                if self.near_left_edge():
                    possible_sequences = [self.walk_right*3,self.jump_right]
                    sequence = random.sample(possible_sequences,1)[0] 
                    return sequence
                else:
                    self.walk_right
            return [None]
           
     def is_left(self):
          return self.playera.rect.centerx < self.playerb.rect.centerx

     def is_right(self):
          return self.playera.rect.centerx > self.playerb.rect.centerx
            
     def is_far(self, distance = 160):
          return abs(self.playera.rect.centerx - self.playerb.rect.centerx) > self.playera.scale(distance)
        
     def is_medium(self, low_distance = 100, high_distance = 160):
          return (not self.is_far(high_distance)) & (not self.is_close(low_distance))
        
     def is_close(self, distance = 100):
          return abs(self.playera.rect.centerx - self.playerb.rect.centerx) < self.playera.scale(distance)

     def is_on_top(self):
          return (self.playerb.rect.centery < self.playera.rect.centery) & self.is_close(20)
        
     def is_under(self):
          return (self.playerb.rect.centery > self.playera.rect.centery) & self.is_close(50)

     def near_right_edge(self):
          return abs(self.playerb.rect.x - self.playerb.screen.get_width()) < self.playera.scale(100)
        
     def near_left_edge(self):
          return abs(self.playerb.rect.x - 0) < self.playera.scale(100)
        
     