import pygame, math, random
import funcs


def spawn_predators(amt, win_dim):
	return [Predator([random.randint(0, win_dim[0]), random.randint(0, win_dim[1]), random.randint(0, win_dim[2])], 5, [0,0,0]) for i in range(amt)]
	#random.randint(-10,10), random.randint(-10,10), random.randint(-10,10), random.randint(-10,10)

def update_predators(predators, birds, win_dim):
	new_predators = predators
	for i in range(len(new_predators)):
		new_predators[i].update(win_dim, birds, i)

	return new_predators

def render_predators(predators, win):
	for predator in predators:
		pass

class Predator():
	def __init__(self, pos, speed, vel):
		self.pos = pos
		self.speed = speed
		self.rot = 0.0 # ALWAYS IN DEGREES
		self.vel = vel
		self.size = 2

		self.steering_coefficient = 0.5 # how well the predators will be able to steer
		self.view_dist = 50

	def get_neighbors(self, predators):
		neighbors = []
		for i, predator in enumerate(predators):
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


	def update(self, win_dim, birds, idx):
		#target_rot = self.rot

		# CONVERT SPEED AND ROTATION INTO VECTOR
		self.idx = idx


		# FIND NEIGHBORING BIRDS
		neighbors = self.get_neighbors(birds)

		#self.apply_force(self.steer_towards(pygame.mouse.get_pos()))

		# OPERATIONS
		if len(neighbors) > 0:
			self.attract(neighbors)


		self.vel = self.cap_vec(self.vel, self.speed)

		# APPLY VELOCITY VECTOR TO POSITION
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
		self.pos[2] += self.vel[2]

		# CHECK FOR BOUNDARIES; WRAP AROUND IF OUTSIDE
		if self.pos[0] > win_dim[0]:
			self.pos[0] = 0
		elif self.pos[0] < 0:
			self.pos[0] = win_dim[0]
		if self.pos[1] > win_dim[1]:
			self.pos[1] = 0
		elif self.pos[1] < 0:
			self.pos[1] = win_dim[1]

		

		
		

	def render(self, win):
		self.rot = funcs.rad_to_deg(math.atan2(self.vel[1], self.vel[0]))
		p1 = (self.pos[0] + math.cos(funcs.deg_to_rad(self.rot))*5*self.size, self.pos[1] + math.sin(funcs.deg_to_rad(self.rot))*5*self.size)
		p2 = (self.pos[0] + math.cos(funcs.deg_to_rad(self.rot+135))*5*self.size, self.pos[1] + math.sin(funcs.deg_to_rad(self.rot+135))*5*self.size)
		p3 = (self.pos[0] + math.cos(funcs.deg_to_rad(self.rot-135))*5*self.size, self.pos[1] + math.sin(funcs.deg_to_rad(self.rot-135))*5*self.size)
		points = (p1,p2,p3)

		pygame.draw.polygon(win, (255,0,0), points)