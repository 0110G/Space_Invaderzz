import pygame,sys
from pygame.locals import *
import random
import time

FPS = 30
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
SCREEN_SIZE = (600,900)

pygame.init()
fpsClock = pygame.time.Clock()
G_DISPLAY = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Space Invaders')
fpsClock = pygame.time.Clock()
bg = pygame.image.load("bg2.jpg")
bg = pygame.transform.scale(bg,SCREEN_SIZE)

class spaceship :
	def __init__(self,x,y,w,h):
		self.disp = pygame.image.load("spaceship.jpg")
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.disp = pygame.transform.scale(self.disp,(self.w,self.h))
		self.vel = 5
		self.direction = 'stand'

	def draw (self) :
		self.surf = G_DISPLAY.blit(self.disp,(self.x,self.y))

	def move (self) :
		self.boundary()
		if self.direction == 'right' :
			self.x = self.x + self.vel
			#self.direction = 'stand'
			return True
		elif self.direction == 'left' :
			self.x = self.x - self.vel
			#self.direction = 'stand'
			return True
		elif self.direction == 'up' :
			self.y = self.y - self.vel
			#self.direction = 'stand'
			return True
		elif self.direction == 'down' :
			self.y = self.y + self.vel
			#self.direction = 'stand'
			return True
		else :
			return False


	def boundary (self) :
		if self.x < 0 :
			self.x = 0
		if self.x + self.w > SCREEN_SIZE[0] :
			self.x = SCREEN_SIZE[0] - self.w
		if self.y + self.h >= SCREEN_SIZE[1] :
			self.y = SCREEN_SIZE[1] - self.h

#**********************************************************************************************

class bullet :
	def __init__(self,w,h,direction,vel) :
		self.bullets = []
		self.disp = pygame.image.load("bullet.png")
		self.w = w
		self.h = h
		self.disp = pygame.transform.scale(self.disp,(self.w,self.h))
		self.direction = direction
		self.vel = vel
		self.num = 0

	def draw (self) :
			i = 0
			#pygame.draw.rect(G_DISPLAY,RED,(bullet[0]+8,bullet[1],10,self.h),1)
			if self.direction == 'up':
				while i < self.num :

					if self.bullets[i][1] - self.vel > 0 :
						self.bullets[i][1] = self.bullets[i][1] - self.vel
						G_DISPLAY.blit(self.disp,(self.bullets[i][0],self.bullets[i][1]))
						i+=1
					else :
						self.bullets.remove(self.bullets[i])
						self.num -= 1
			else :
				while i < self.num :

					if self.bullets[i][1] + self.vel < SCREEN_SIZE[1] :
						self.bullets[i][1] = self.bullets[i][1] + self.vel
						G_DISPLAY.blit(self.disp,(self.bullets[i][0],self.bullets[i][1]))
						i+=1
					else :
						self.bullets.remove(self.bullets[i])
						self.num -= 1
						#self.bullets[0][1] += self.vel

					

	def check_if_hit(self,coordinate,w,h):
		for i in self.bullets :
				if i[0] + 8 >= coordinate[0] and coordinate[0] + w >= i[0] + 18 :
					if coordinate[1] + h  >= i[1] and coordinate[1] <= i[1] + self.h :
						G_DISPLAY.blit(fire,(coordinate[0],coordinate[1]))
						self.bullets.remove(i)
						self.num -=1
						return True
		return False
#*********************************************************************************************
class boss :
	def __init__(self,x,y,w,h):
		self.disp = pygame.image.load("boss.png")
		self.disp = pygame.transform.scale(self.disp,(w,h))
		self.health = 20
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.frame = 0
		self.rand_dir = 'right'
		self.b_bullet = bullet(25,20,'down',25)
	def draw(self) :
		G_DISPLAY.blit(self.disp,(self.x,self.y))
		self.b_bullet.draw()
		pygame.draw.rect(G_DISPLAY,RED,(self.x,self.y,40,5))
		for i in range (self.health) :
			pygame.draw.rect(G_DISPLAY,GREEN,(self.x+2*i,self.y,2,5))
		
	def move (self) :
		self.boundary()

		if self.rand_dir == 'right' :
			self.x = self.x + 10
		if self.rand_dir == 'left':
			self.x = self.x - 10
		self.frame += 1
		if self.frame == 30 :
			self.frame = 0
		

	def boundary(self) :
		if self.x - 10 < 0 :
			self.x = 0
			self.rand_dir = 'right'
		if self.x + self.w + 10 > SCREEN_SIZE[0] :
			self.x = SCREEN_SIZE[0] - self.w
			self.rand_dir = 'left'
		if self.y - 10 <= 0 :
			self.y = 0
			self.rand_dir = 'down'
		if self.y + self.h + 10 > 600 :
			self.y = 600
			self.rand_dir = 'up' 

	def shoot (self) :
		if self.frame == 0 :
			for i in range (10,70,25) :
				self.b_bullet.num+=1
				self.b_bullet.bullets.append([self.x+i,self.y+self.h])
			#self.b_bullet.bullets.append([self.x+30,self.y+10])



#*********************************************************************************************
class enemy : 
	def __init__(self,w,h) :
		self.enemies = [[i,j] for i in range (20,490,90) for j in range (20,400,80)]
		self.disp = pygame.image.load("enemy.jpg")
		self.w = w
		self.h = h
		self.disp = pygame.transform.scale(self.disp,(self.w,self.h))
		self.number = 30
		self.Rect = pygame.Rect(15,15,100,400)

	def draw_enemy (self) :
		self.rem = [G_DISPLAY.blit(self.disp,(_enemy[0]+random.randint(0,2),_enemy[1]+random.randint(0,2))) for _enemy in self.enemies ]
		return self.enemies

		#
	def check_if_hit(self,coordinates) :
		for i in self.enemies :
				if coordinates[0] >= i[0]-12 and coordinates[0] <= i[0] + self.w :
					if coordinates[1] >= i[1] and coordinates[1] <= i[1] + self.h -25  :
						G_DISPLAY.blit(fire,(i[0],i[1]))
						self.enemies.remove(i)
						self.number -= 1
						return True
		return False
		#20,100,180,240,320
	def reset(self):
		self.enemies = [[i,j] for i in range (20,490,90) for j in range (20,400,80)]
#*************************************************************************************************

class wall :
	def __init__(self,x1,y1,x2,y2):
		self.walls = [[i,j] for i in range (x1,x1+300,25) for j in range (y1,y1+100,25)]
		for i in range (x2,x2+200,25) : 
			for j in range (y1,y1+100,25) : 
				self.walls.append([i,j])
		self.disp = pygame.image.load("wall.png")
		self.disp = pygame.transform.scale(self.disp,(25,25))

	def draw(self) :
		[G_DISPLAY.blit(self.disp,(i[0],i[1])) for i in self.walls]

#**************************************************************************************************
def text_objects(text, font , color) :
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text,font_size,x,y,color = BLACK) :
    largeText = pygame.font.Font('freesansbold.ttf',font_size)
    TextSurf, TextRect = text_objects(text, largeText,color)
    TextRect.center = (x,y)                              #200 307
    G_DISPLAY.blit(TextSurf, TextRect)

fire = pygame.image.load("fire.png")
fire = pygame.transform.scale(fire,(60,60))

def game_loop():
	BULLET = bullet(25,20,'up',10)
	HERO = spaceship(10,800,70,50)
	ENEMY = enemy(60,60)
	ENEMY_BULLET = bullet(25,20,'down',20)
	WALL = wall(50,700,375,700)
	frame_count = 0
	

	while True :
		#G_DISPLAY.fill(WHITE)
		events = pygame.event.get()
		for event in events :
			if event.type == pygame.QUIT :
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_RIGHT :
					HERO.direction = 'right'
				if event.key == pygame.K_LEFT :
					HERO.direction = 'left'
				if event.key == pygame.K_UP :
					HERO.direction = 'up'
				if event.key == pygame.K_DOWN :
					HERO.direction = 'down'
				if event.key == pygame.K_SPACE :
					BULLET.bullets.append([HERO.x,HERO.y])
					BULLET.num += 1
			
		G_DISPLAY.blit(bg,(0,0)) 
		if frame_count == 20 and ENEMY.number != 0:
			a =random.sample(ENEMY.enemies,1)[0]
			ENEMY_BULLET.bullets.append([a[0],a[1]])
			ENEMY_BULLET.num+=1
			ENEMY.enemies = [[x[0],x[1]+10] for x in ENEMY.enemies]
			frame_count = 0

		WALL.draw()
		HERO.move()  
		HERO.draw()
		v = ENEMY.draw_enemy()
		BULLET.draw()
		ENEMY_BULLET.draw()
		for i in v :
			if BULLET.check_if_hit(i,ENEMY.w,ENEMY.h) :
				ENEMY.enemies.remove(i)
				ENEMY.number -= 1
				if ENEMY.number == 0:
					return 0

		for j in WALL.walls :
			if BULLET.check_if_hit(j,35,35) or ENEMY_BULLET.check_if_hit(j,35,35):
				WALL.walls.remove(j)

		if ENEMY_BULLET.check_if_hit((HERO.x,HERO.y),HERO.w,HERO.h) or ENEMY.check_if_hit((HERO.x,HERO.y)):
			G_DISPLAY.blit(bg,(0,0))
			G_DISPLAY.blit(fire,(HERO.x,HERO.y))
			message_display('YOU LOST :{',50,300,400,RED)
			pygame.display.update()
			time.sleep(2)
			pygame.quit()
			sys.exit()			

		#pygame.draw.rect(G_DISPLAY,RED,(HERO.x,HERO.y,HERO.w,HERO.h),1)
		frame_count = frame_count + 1
		pygame.display.update()
		fpsClock.tick(15)

def boss_fight():
	HERO = spaceship(10,800,70,50)
	BOSS = boss(100,100,90,90)
	BOSS1 = boss(450,400,90,90)
	BULLET = bullet(25,20,'up',10)
	while True :
		#G_DISPLAY.fill(WHITE)
		events = pygame.event.get()
		for event in events :
			if event.type == pygame.QUIT :
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_RIGHT :
					HERO.direction = 'right'
				if event.key == pygame.K_LEFT :
					HERO.direction = 'left'
				if event.key == pygame.K_UP :
					HERO.direction = 'up'
				if event.key == pygame.K_DOWN :
					HERO.direction = 'down'
				if event.key == pygame.K_SPACE :
					BULLET.bullets.append([HERO.x,HERO.y])
					BULLET.num += 1
			
		G_DISPLAY.blit(bg,(0,0))
		HERO.move()
		
		if BOSS.health > 0:
			BOSS.move()
			BOSS.shoot()
			BOSS.draw()
		if BOSS1.health > 0:
			BOSS1.move()
			BOSS1.shoot() 
			BOSS1.draw()
		
		  
		HERO.draw()
		BULLET.draw()
		if BOSS.b_bullet.check_if_hit((HERO.x,HERO.y),HERO.w,HERO.h) or BOSS1.b_bullet.check_if_hit((HERO.x,HERO.y),HERO.w,HERO.h) :
			message_display('YOU LOST :{',50,300,400,RED)
			pygame.display.update()
			time.sleep(2)
			pygame.quit()
			sys.exit()
		if BULLET.check_if_hit((BOSS.x,BOSS.y),BOSS.w,BOSS.h) :
			BOSS.health -= 1
		if BULLET.check_if_hit((BOSS1.x,BOSS1.y),BOSS1.w,BOSS1.h):
			BOSS1.health -= 1
		pygame.display.update()
		fpsClock.tick(15)

def main():
	G_DISPLAY.blit(bg,(0,0))
	message_display('Welcome to',40,290,200,WHITE)
	message_display('Instructions :',30,120,330,WHITE)
	message_display('Press [->]  [<-]  [/|\]  [\|/] to Navigate Captain Rambo',20,265,360,WHITE)
	message_display('Press Space to shoot',20,119,390,WHITE)
	message_display('Press Any Key to continue',30,290,530,GREEN)
	while True:
		message_display('$P@[<  !N\/@[Rs',55,290,260,(random.randint(1,255),random.randint(1,255),random.randint(1,255)))
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				return 0
		time.sleep(0.5)
		pygame.display.update()

main()
game_loop()
boss_fight()
	




