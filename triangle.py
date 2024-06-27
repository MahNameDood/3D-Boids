import math, pygame, random
from renderer import project

class Triangle:
	def __init__(self, points):
		self.points = points
	def render(self, win, focal_length, win_dim, col, cam_pos, cam_rot, wire_frame=False):
		projected_points = []
		in_frame = False
		for i, p in enumerate(self.points):

			proj = project(focal_length, win_dim, p, cam_pos, cam_rot)

			#print(f'prefreeze {i}, {cam_pos}, {proj}')
			if proj[1]:
				in_frame = True

			projected_points.append(proj[0])

		if wire_frame:
			w = 1
		else:
			w = 0
		if in_frame:
			pygame.draw.polygon(win, col, projected_points, w)