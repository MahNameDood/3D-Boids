import math, sys
from rotation_matrices import rotate
import copy

def in_frame(focal_length, win_dim, p):
	in_x = p[2] >= ((focal_length/(win_dim[0]/2))*p[0]) and p[2] >= (((0-focal_length)/(win_dim[0]/2))*p[0])
	in_y = p[2] >= ((focal_length/(win_dim[1]/2))*p[1]) and p[2] >= (((0-focal_length)/(win_dim[1]/2))*p[1])
	#in_y = p[2] >= ((focal_length/(win_dim[0]/2))*p[0])-focal_length and p[2] >= (((0-focal_length)/(win_dim[0]/2))*p[0])-focal_length
	#print(in_x)

	if p[2] < 0:
		return False

	else:
		return in_x and in_y

def project(focal_length, win_dim, p, cam_pos, cam_rot):
	new_point = [0,0]
	point = copy.deepcopy(p) 

	point[0] -= cam_pos[0]
	point[1] -= cam_pos[1]
	point[2] -= cam_pos[2]

	# rotation
	point = rotate(rotate(point, [0,0,0], 'y', cam_rot[1]), [0,0,0], 'x', cam_rot[0])
	#point = rotate(point, [0,0,0], 'y', cam_rot[1])
	#point = rotate(point, [0,0,0], 'z', cam_rot[2])
	framed = in_frame(focal_length, win_dim, point)

	

	#if not framed:
		#point = [0-point[0], 0-point[1], 0-point[2]]


	new_point[0] = (point[0] * (focal_length / (point[2]+sys.float_info.epsilon))) + win_dim[0]/2
	new_point[1] = (point[1] * (focal_length / (point[2]+sys.float_info.epsilon))) + win_dim[1]/2


	return new_point, framed

