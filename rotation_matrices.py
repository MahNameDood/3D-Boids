import math, numpy as np
from math import cos
from math import sin

def get_matrix(direction, theta):
	if direction == 'x':
		return np.array([
			[1, 0, 0],
			[0, cos(theta), 0-sin(theta)],
			[0, sin(theta), cos(theta)]])
	elif direction == 'y':
		return np.array([
			[cos(theta), 0, sin(theta)],
			[0, 1, 0],
			[0-sin(theta), 0, cos(theta)]])
	elif direction == 'z':
		return np.array([
			[cos(theta), 0-sin(theta), 0],
			[sin(theta), cos(theta), 0],
			[0, 0, 1]])

def rotate(p, origin, direction, angle):
	angle = angle * 0.0174533
	m = get_matrix(direction, angle)
	point = p

	point[0] -= origin[0]
	point[1] -= origin[1]
	point[2] -= origin[2]

	new_point = np.dot(m, point)

	point[0] += origin[0]
	point[1] += origin[1]
	point[2] += origin[2]

	return new_point
