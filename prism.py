import pygame, math
from triangle import Triangle

class Rect_Prism:
	def __init__(self, pos, size):
		self.pos = pos
		self.size = size

		self.x = pos[0]
		self.y = pos[1]
		self.z = pos[2]
		self.w = size[0]
		self.h = size[1]
		self.d = size[2]

		
	def gen_face(rect):
		t1 = Triangle()