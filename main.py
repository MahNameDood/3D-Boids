import pygame, sys, random
import bird, predator
import pygame, sys, random, math
from renderer import project
from triangle import Triangle
from camera_controller import Camera

pygame.init()

WIDTH = 1900
HEIGHT = 1100
win_dim = (WIDTH, HEIGHT)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BOIDS 3D !!!')
clock = pygame.time.Clock()

birds = bird.spawn_birds(250, [1000,1000,1000])
predators = predator.spawn_predators(0, [1000,1000,1000])






# 3D STUFF !!!!1!!11
cam = Camera()


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	win.fill((0,0,0))
	keys = pygame.key.get_pressed()

	predators = predator.update_predators(predators, birds, win_dim)
	predator.render_predators(predators, win)

	
	if not keys[pygame.K_TAB]:
		birds = bird.update_birds(predators, birds, [1000,1000,1000])
	bird.render_birds(birds, win, cam.focal_length, win_dim, cam.pos, cam.rot)
	


	for i in range(2):
		for j in range(2):
			for k in range(2):
				if i == 0 or i == 1 or j == 0 or j == 1 or k == 0 or k == 1:
					pygame.draw.circle(win, (255,0,0), project(cam.focal_length, win_dim, [i*1000, k*1000, j*1000], cam.pos, cam.rot)[0], 5)

	cam.update()

	pygame.display.update()
	clock.tick(60)