import pygame, sys, random, math
from renderer import project
from triangle import Triangle
from camera_controller import Camera


def main():
	pygame.init()
	pygame.font.init()

	verdana_font = pygame.font.SysFont('verdana', 10)

	WIDTH = 1900
	HEIGHT = 1000
	win = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	pygame.display.set_caption('3D')

	cam = Camera()


	mouse_sens = 0.2
	mouse_moved = [0.0,0.0]

	draw_grid = True
	temp = 0

	pygame.mouse.set_visible(False)



	t = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEWHEEL:
				temp += event.y
			else:
				mouse_scroll = 0

		win.fill((0,0,0))
		keys = pygame.key.get_pressed()


		
		for x in range(temp):
			for z in range(temp):
				pos = [x*20, 10, z*20]
				pos1 = [(x+1)*20, 10, z*20]
				pos2 = [x*20, 10, (z+1)*20]
				grid_tri = Triangle((pos, pos1, pos2))
				grid_tri.render(win, cam.focal_length, (WIDTH, HEIGHT), ((math.sin(t*0.1)/2+0.5)*255,(math.cos(t*0.1)/2+0.5)*255,(math.cos(t*0.1+0.5)/2+0.5)*255), cam.pos, cam.rot, True)
				projected = project(cam.focal_length, (WIDTH, HEIGHT), pos, cam.pos, cam.rot)
				#print(f'x: {x}, z: {z}; proj: {projected}')
				if projected[1]:
						pygame.draw.circle(win, (255,0,0), projected[0], 2)
		
		temp += mouse_scroll
		
		font_surf = verdana_font.render(f'FPS: {clock.get_fps()}', True, (255,255,255))
		win.blit(font_surf, (10,10))
		cam.update(mouse_moved)
		

		test = Triangle(([10,0,1], [0,10,1], [0,0,1]))
		#test.render(win, cam.focal_length, (WIDTH, HEIGHT), (255,255,255), cam.pos, cam.rot)

		



		
		
		#mouse_moved = (pygame.mouse.get_pos()[0] - WIDTH/2, pygame.mouse.get_pos()[1] - HEIGHT/2)
		#pygame.mouse.set_pos((WIDTH/2, HEIGHT/2))
		t += 1
		pygame.display.update()
		clock.tick(60)
	


if __name__ == '__main__':
	main()