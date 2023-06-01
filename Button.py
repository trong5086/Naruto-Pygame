#Import thư viện
import pygame

#Lớp Nút
class Button():
	#Phương thức khởi tạo nút 
	#Input: ảnh nút, vị trí nút, chữ, font, màu nút, màu nút khi rê chuột vào
	#Output: Không có
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		#Font
		self.font = font
		#Màu gốc, màu hover
		self.base_color, self.hovering_color = base_color, hovering_color
		#Text
		self.text_input = text_input
		#Font
		self.text = self.font.render(self.text_input, True, self.base_color)
		#Khởi tạo image = None
		if self.image == None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	#Phương thức cập nhật nút xử lý lên màn hình giải quyết case khi nút có ảnh và không có ảnh
	#Input: Màn hình chính
	#Output: Không có
	def update(self, screen):
		#Nếu thuộc tính image khác none
		if self.image != None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	#Phương thức bắt sự kiện click chuột
	#Input: Vị trí chuột
	#Output: True khi click trúng button, False khi không trúng
	def checkForInput(self, position):
		#Nếu tọa độ x chuột trong khoảng trái và phải của nút, tọa độ y torng khoảng trên và dưới
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False
	
	#Phương thức đổi màu khi rê chuột vào nút
	#Input: Vị trí chuột
	#Output: Không có
	def changeColor(self, position):
		#Nếu tọa độ x chuột trong khoảng trái và phải của nút, tọa độ y torng khoảng trên và dưới
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			#Đổi màu hover
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			#Màu nút gốc
			self.text = self.font.render(self.text_input, True, self.base_color)