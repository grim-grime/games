import pygame, sys
from pygame.locals import *
import random

FPS = 30
WINDOWWIDTH = 600
WINDOWHEIGHT = 650
BANNERHEIGHT = 50

WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
DARKGREEN = 0, 155, 0
DARKGRAY = 40, 40, 40
BLUE = 0, 0, 155
GRAY = 120, 120, 120
ORANGE = 255,127,0
YELLOW = 255,255,0
GREEN= 0,255,0
TEAL = 0, 255, 255
PINK = 255,0,255
PURPLE = 127,0,255

BRICKCOLORS = [RED,ORANGE,GREEN,BLUE,TEAL,PURPLE,PINK]

BGCOLOR = BLACK

PADDLEWIDTH = 100
PADDLEHEIGHT = 10
PADDLEMARGIN = 20

PADDLEACCELERATION = 2
PADDLEFRICTION = 1
PADDLESPEED = 10

BRICKWIDTH = 47
BRICKHEIGHT = 20
BRICKTOP = BANNERHEIGHT + 70
ROWS = 10
COLUMNS = 10

BALLRADIUS = 6
STARTSPEED = 10
MAXBALLSPEED = 10

RELOADFRAMES = 20
WIN, LOSE = 'win','lose'

class Paddle:
	def __init__(self):
		self.width = PADDLEWIDTH
		self.color = YELLOW
		self.x = WINDOWWIDTH // 2 - self.width // 2
		self.y = WINDOWHEIGHT - PADDLEMARGIN - PADDLEHEIGHT
		self.vx = 0
	def move(self):
		pass
	def draw(self):
		paddleRect = pygame.Rect(self.x, self.y,self.width,PADDLEHEIGHT)
		pygame.draw.rect(DISPLAYSURF,self.color,paddleRect)
	def checkBoundary(self):
		if self.x + PADDLEWIDTH >= WINDOWWIDTH:
			self.x = WINDOWWIDTH - 1 - PADDLEWIDTH
		elif self.x < 0:
			self.x = 0

class Brick:
	def __init__(self,j,i):
		self.color = random.choice(BRICKCOLORS)
		self.j = j
		self.i = i
		self.y = BRICKTOP + j * BRICKHEIGHT
		self.x = (WINDOWWIDTH - COLUMNS * BRICKWIDTH) // 2 + i * BRICKWIDTH
	def draw(self):
		outerRect = pygame.Rect(self.x, self.y,BRICKWIDTH,BRICKHEIGHT)
		innerRect = pygame.Rect(self.x+1, self.y+1, BRICKWIDTH -2, BRICKHEIGHT -2)
		pygame.draw.rect(DISPLAYSURF,BLACK,outerRect)
		pygame.draw.rect(DISPLAYSURF,self.color,innerRect)

class Brickboard:
	def __init__(self):
		self.bricks = [[Brick(j,i) for i in range(COLUMNS)] for j in range(ROWS)]
		self.remaining = COLUMNS * ROWS
	def draw(self):
		for row in self.bricks:
			for brick in row:
				if brick:
					brick.draw()
	def delete(self,j,i):
		self.bricks[j][i] = None
		self.remaining -= 1

	def flatten(self):
		return [brick for row in self.bricks for brick in row if brick]

	def done(self):
		return self.remaining == 0

class Ball:
	def __init__(self):
		self.y = ((BRICKTOP + ROWS * BRICKHEIGHT) + (WINDOWHEIGHT - PADDLEMARGIN - PADDLEHEIGHT)) // 2
		self.x = WINDOWWIDTH // 2
		self.radius = BALLRADIUS
		self.color = RED
		self.vy = -STARTSPEED
		self.vx = random.randint(-STARTSPEED,STARTSPEED)
	def draw(self):
		pygame.draw.circle(DISPLAYSURF, BLACK, (self.x,self.y) ,self.radius*2)
		pygame.draw.circle(DISPLAYSURF, self.color, (self.x,self.y),self.radius*2-1)
	def move(self):
		self.x += self.vx
		self.y += self.vy
		self.checkBoundary()
		self.checkBlocks()
		if self.bounce(PADDLE.x,PADDLE.y,PADDLEWIDTH,PADDLEHEIGHT):
			self.vx = MAXBALLSPEED * (self.x - (PADDLE.x + PADDLEWIDTH //2)) // (PADDLEWIDTH // 2 )
	def outOfBounds(self):
		return self.y - self.radius > WINDOWHEIGHT + 10
	def checkBlocks(self):
		for brick in BRICKBOARD.flatten():
			if self.bounce(brick.x,brick.y,BRICKWIDTH,BRICKHEIGHT):
				BRICKBOARD.delete(brick.j,brick.i)
	def checkBoundary(self):
		if self.x - self.radius < 1:
			self.x = self.radius + 1
			self.vx = -self.vx
		elif self.x + self.radius >= WINDOWWIDTH -1 :
			self.x = WINDOWWIDTH - 1 - self.radius - 1
			self.vx = -self.vx
		elif self.y - self.radius < BANNERHEIGHT + 1:
			self.y = self.radius + BANNERHEIGHT + 1
			self.vy = -self.vy
	def bounce(self,x,y,dx,dy):
		checkx = self.x + self.vx
		checky = self.y + self.vy
		if checkx - self.radius <= x + dx and checkx + self.radius >= x and \
		checky - self.radius <= y + dy and checky + self.radius >= y:
			if self.x + self.radius < x:
				self.x = x - self.radius
				self.vx = -self.vx
			elif self.x - self.radius > x +dx:
				self.x = x + dx + self.radius
				self.vx = -self.vx
			elif self.y + self.radius < y:
				self.y = y - self.radius
				self.vy = -self.vy
			elif self.y - self.radius > y + dy:
				self.y = y + dy + self.radius
				self.vy = -self.vy
			return 'Collision'




def drawInfo(lives):
	infoRect = pygame.Rect(0, 0, WINDOWWIDTH, BANNERHEIGHT)
	pygame.draw.rect(DISPLAYSURF,GRAY,infoRect)
	spacing = 30 
	rightmargin = 30
	for i in range(lives):
		x = WINDOWWIDTH - rightmargin - BALLRADIUS  - (i * (spacing + BALLRADIUS * 2))
		y = BANNERHEIGHT // 2 
		pygame.draw.circle(DISPLAYSURF, BLACK, (x,y) ,BALLRADIUS*2)
		pygame.draw.circle(DISPLAYSURF, RED, (x,y),BALLRADIUS*2-1)

def terminate():
	pygame.quit()
	sys.exit()

def gameOverScreen(result):
	if result == WIN:
		msg = 'YOU WIN'
	else:
		msg = 'GAME OVER'
	gameOverFont = pygame.font.Font('freesansbold.ttf',50)
	msgSurf = gameOverFont.render(msg,True,RED)
	msgRect = msgSurf.get_rect()
	msgRect.center = WINDOWWIDTH // 2, BANNERHEIGHT // 2
	DISPLAYSURF.blit(msgSurf,msgRect)
	pygame.display.update()
	pygame.time.wait(2000)

def runGame():
	global PADDLE, BRICKBOARD, BALL
	PADDLE = Paddle()
	BRICKBOARD = Brickboard()
	BALL = Ball()

	movingRight = False
	movingLeft = False
	lives = 3
	reloadFrames = 0

	while True:
		#get input
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_LEFT:
					movingLeft = True
				elif event.key == K_RIGHT:
					movingRight = True
				elif event.key == K_ESCAPE:
					terminate()
			elif event.type == KEYUP:
				if event.key == K_LEFT:
					movingLeft = False
				elif event.key == K_RIGHT:
					movingRight = False
		#move paddle
		if movingLeft:
			PADDLE.x -= PADDLESPEED
		if movingRight:
			PADDLE.x += PADDLESPEED
		PADDLE.checkBoundary()

		#move ball
		BALL.move()

		#check if out of bounds
		if BALL.outOfBounds() and reloadFrames == 0:
			lives -= 1
			reloadFrames = RELOADFRAMES

		#if out of bounds, wait to reload ball
		if reloadFrames > 0:
			reloadFrames -= 1
			if reloadFrames == 0:
				BALL = Ball()


		#draw screen
		DISPLAYSURF.fill(BGCOLOR)
		PADDLE.draw()
		BRICKBOARD.draw()
		BALL.draw()
		drawInfo(lives)
		pygame.display.update()

		#exit conditions
		if lives == 0:
			return LOSE
		elif BRICKBOARD.done():
			return WIN

		FPSCLOCK.tick(FPS)


def main():
	global FPSCLOCK,DISPLAYSURF, BASICFONT


	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf',18)
	pygame.display.set_caption("This is a game.")

	while True:
		result = runGame()
		gameOverScreen(result)

if __name__ == '__main__':
	main()