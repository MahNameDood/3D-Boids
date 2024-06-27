import pygame, math, random
import funcs
from renderer import project


def spawn_birds(amt, win_dim):
	return [Bird([random.randint(0, win_dim[0]), random.randint(0, win_dim[1]), random.randint(0, win_dim[2])], 5, [random.randint(-1,1), random.randint(-1,1), random.randint(-1,1)]) for i in range(amt)]
	#random.randint(-1,1), random.randint(-1,1), random.randint(-1,1)

def update_birds(predators, birds, win_dim):
	new_birds = birds
	for i in range(len(new_birds)):
		new_birds[i].update(win_dim, birds, predators, i)

	return new_birds

def render_birds(birds, win, focal_length, win_dim, cam_pos, cam_rot):
	for bird in birds:
		#bird.render(win, False)
		pos = bird.pos
		#point = [0,0]
		point = project(focal_length, win_dim, pos, cam_pos, cam_rot)[0]
		#print(point)
		pygame.draw.circle(win, (255,255,255), point, 5)


class Bird():
	def __init__(self, pos, speed, vel):
		self.pos = pos
		self.speed = speed
		self.rot = 0.0 # ALWAYS IN DEGREES
		self.vel = vel
		self.size = 2

		self.steering_coefficient = 0.2 # how well the birds will be able to steer
		self.view_dist = 100

	def get_neighbors(self, birds):
		neighbors = []
		for i, predator in enumerate(birds):
			if i != self.idx:
				if funcs.distance(self.pos, predator.pos) <= self.view_dist:
					neighbors.append(predator)

		return neighbors

	def cap_vec(self, vec, cap):
		mag = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
		if mag > 0:
			return [(vec[0]/mag)*cap, (vec[1]/mag)*cap, (vec[2]/mag)*cap]
		else:
			return [0,0,0]


	def alignment(self, neighbors):
		avg = [0,0,0]
		for n in neighbors:
			avg[0] += n.vel[0]
			avg[1] += n.vel[1]
			avg[2] += n.vel[2]

		avg = [avg[0]/len(neighbors), avg[1]/len(neighbors), avg[2]/len(neighbors)]
		self.steer_in_dir(avg)

	def repel(self, neighbors):
		avg = [0,0,0]
		for n in neighbors:
			avg[0] += self.pos[0] - n.pos[0]
			avg[1] += self.pos[1] - n.pos[1]
			avg[2] += self.pos[2] - n.pos[2]

		avg = [avg[0]/len(neighbors), avg[1]/len(neighbors), avg[2]/len(neighbors)]
		self.steer_in_dir(avg)

	def attract(self, neighbors):
		avg = [0,0,0]
		for n in neighbors:
			avg[0] += n.pos[0]
			avg[1] += n.pos[1]
			avg[2] += n.pos[2]

		avg = [avg[0]/len(neighbors), avg[1]/len(neighbors), avg[2]/len(neighbors)]
		self.steer_towards(avg)

	
	def steer_in_dir(self, vec):
		force = [vec[0]-self.vel[0], vec[1]-self.vel[1], vec[2]-self.vel[2]]

		# NORMALIZING STEER FORCE AND SETTING TO STEER COEFF.
		mag = math.sqrt(force[0]**2 + force[1]**2 + force[2]**2)
		if mag > 0:
			self.apply_force([(force[0]/mag)*self.steering_coefficient, (force[1]/mag)*self.steering_coefficient, (force[2]/mag)*self.steering_coefficient])

	def steer_towards(self, point):
		desired = [point[0]-self.pos[0], point[1]-self.pos[1], point[2]-self.pos[2]]
		force = [desired[0]-self.vel[0], desired[1]-self.vel[1], desired[2]-self.vel[2]]

		# NORMALIZING STEER FORCE AND SETTING TO STEER COEFF.
		mag = math.sqrt(force[0]**2 + force[1]**2 + force[2]**2)
		if mag > 0:
			self.apply_force([(force[0]/mag)*self.steering_coefficient, (force[1]/mag)*self.steering_coefficient, (force[2]/mag)*self.steering_coefficient])

	def apply_force(self, force):
		self.vel[0] += force[0]
		self.vel[1] += force[1]
		self.vel[2] += force[2]


	def update(self, win_dim, birds, predators, idx):
		#target_rot = self.rot
		
		# CONVERT SPEED AND ROTATION INTO VECTOR
		self.idx = idx


		# FIND NEIGHBORING BIRDS
		neighbors = self.get_neighbors(birds)
		pred_neighbors = self.get_neighbors(predators)

		#self.apply_force(self.steer_towards(pygame.mouse.get_pos()))

		# OPERATIONS
		
		self.desired_vecs = [[0,0], [0,0], [0,0]]
		#if len(pred_neighbors) > 0:
			#self.repel(pred_neighbors)
			#self.repel(pred_neighbors)
			#self.alignment(pred_neighbors, True)


		if len(neighbors) > 0:
			self.alignment(neighbors)
			self.attract(neighbors)
			self.repel(neighbors)
		else:
			#pass
			self.apply_force([random.randint(-1,1), random.randint(-1,1), random.randint(-1,1)])
			
			

		#if pygame.mouse.get_pressed()[0]:# and funcs.distance(self.pos, pygame.mouse.get_pos()) < self.view_dist:
			#self.steer_in_dir([self.pos[0]-pygame.mouse.get_pos()[0], self.pos[1]-pygame.mouse.get_pos()[1]])
		



		self.vel = self.cap_vec(self.vel, self.speed)

		# APPLY VELOCITY VECTOR TO POSITION
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
		self.pos[2] += self.vel[2]
		

		# CHECK FOR BOUNDARIES; WRAP AROUND IF OUTSIDE
		self.pos[0] %= win_dim[0]
		self.pos[1] %= win_dim[1]
		self.pos[2] %= win_dim[2]

		

		
		

	def render(self, win, draw_lines=False):
		self.rot = funcs.rad_to_deg(math.atan2(self.vel[1], self.vel[0]))
		p1 = (self.pos[0] + math.cos(funcs.deg_to_rad(self.rot))*5*self.size, self.pos[1] + math.sin(funcs.deg_to_rad(self.rot))*5*self.size)
		p2 = (self.pos[0] + math.cos(funcs.deg_to_rad(self.rot+135))*5*self.size, self.pos[1] + math.sin(funcs.deg_to_rad(self.rot+135))*5*self.size)
		p3 = (self.pos[0] + math.cos(funcs.deg_to_rad(self.rot-135))*5*self.size, self.pos[1] + math.sin(funcs.deg_to_rad(self.rot-135))*5*self.size)
		points = (p1,p2,p3)

		pygame.draw.polygon(win, (255,255,255), points)


		if draw_lines:
			pygame.draw.line(win, (0,255,0), self.pos, [self.pos[0] + self.desired_vecs[0][0], self.pos[1] + self.desired_vecs[0][1]])
			pygame.draw.line(win, (0,0,255), self.pos, [self.pos[0] + self.desired_vecs[1][0] * 10, self.pos[1] + self.desired_vecs[1][1] * 10])
			pygame.draw.line(win, (255,0,0), self.pos, [self.pos[0] + self.desired_vecs[2][0], self.pos[1] + self.desired_vecs[2][1]])
			pygame.draw.circle(win, (255,0,255), self.pos, self.view_dist, 2)