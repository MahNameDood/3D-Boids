import math, numpy as np, pygame

class Camera:
	def __init__(self, pos=[0,0,0], rot=[0.0,0.0,0.0], focal_length=1000, speed=10):
		self.pos = pos
		self.rot = rot
		self.focal_length = focal_length
		self.speed = speed
		self.pitch = 0.0
		self.yaw = 0.0
		self.vel = [0,0,0]

	def update(self):
		keys = pygame.key.get_pressed()

		self.rot[1] = self.yaw
		self.rot[0] = self.pitch
		#gravity = 0.0

		#self.vel[1] += gravity
		#self.pos[1] += self.vel[1]
		#if self.pos[1] > 0:
			#self.pos[1] = 0
			#self.vel[1] = 0
			#can_jump = True
		#else:
			#can_jump = False

		if keys[pygame.K_a]:
			self.pos[2] -= math.cos(self.rot[1]*0.0174533-90*0.0174533)*self.speed
			self.pos[0] += math.sin(self.rot[1]*0.0174533-90*0.0174533)*self.speed
		if keys[pygame.K_d]:
			self.pos[2] -= math.cos(self.rot[1]*0.0174533+90*0.0174533)*self.speed
			self.pos[0] += math.sin(self.rot[1]*0.0174533+90*0.0174533)*self.speed
		if keys[pygame.K_w]:
			self.pos[2] += math.cos(self.rot[1]*0.0174533)*self.speed
			self.pos[0] -= math.sin(self.rot[1]*0.0174533)*self.speed
		if keys[pygame.K_s]:
			self.pos[2] -= math.cos(self.rot[1]*0.0174533)*self.speed
			self.pos[0] += math.sin(self.rot[1]*0.0174533)*self.speed
		if keys[pygame.K_SPACE]:
			self.pos[1] -= self.speed
		if keys[pygame.K_LSHIFT]:
			self.pos[1] += self.speed
		if keys[pygame.K_e]:
			self.yaw -= 1
		if keys[pygame.K_q]:
			self.yaw += 1
		if keys[pygame.K_u]:
			self.pitch -= 1
		if keys[pygame.K_j]:
			self.pitch += 1
		if keys[pygame.K_y]:
			self.focal_length += 10
		if keys[pygame.K_h]:
			self.focal_length -= 10



		


		self.pos = [round(self.pos[0],2), round(self.pos[1],2), round(self.pos[2],2)]