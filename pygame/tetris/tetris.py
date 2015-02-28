import pygame, sys
from pygame.locals import *
import random
from pprint import pprint

FPS = 30
WINDOWWIDTH = 600
WINDOWHEIGHT = 800

ROWCOUNT = 25
COLUMNCOUNT = 10
CELLSIZE = 20
GRIDWIDTH = COLUMNCOUNT * CELLSIZE
GRIDHEIGHT = ROWCOUNT * CELLSIZE

XMARGIN = (WINDOWWIDTH - (CELLSIZE * COLUMNCOUNT)) // 2
YMARGIN = (WINDOWHEIGHT - (CELLSIZE * ROWCOUNT)) // 2

PLAYLEFT = XMARGIN
PLAYRIGHT = WINDOWWIDTH - XMARGIN
PLAYTOP = YMARGIN
PLAYBOTTOM = WINDOWHEIGHT - YMARGIN

INFOMARGIN = 10
TEMPLATESIZE = 5

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
GREEN=0,255,0
TEAL = 0, 255, 255
PINK = 255,0,255
PURPLE = 127,0,255

COLORLIST = [RED,ORANGE,YELLOW,GREEN,TEAL,PINK,PURPLE]
BGCOLOR = BLUE

HOLDWAITMAX = 3
DIFFICULTYRATE = 5
DROPTIMEMAX = 7
DROPTIME = DROPTIMEMAX
DROPCOUNTER = DROPTIME
NEXTPIECE = None
CURRENTPIECE = None


LEFT, RIGHT, DOWN, NONE = 'left', 'right', 'down', 'none'
CW, CCW = 'cw', 'ccw'
BLANK = 'blank'

DELTS = {LEFT: (0,-1), RIGHT: (0,1), DOWN: (1,0), NONE:(0,0)}

TEMPLATES = [[[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]], #I
				[[1,1],[1,1]], #SQUARE
				[[1,0,0],[1,1,0],[0,1,0]], #SQUIGGLE1
				[[0,1,0],[1,1,0],[1,0,0]], #SQUIGGLE2
				[[0,1,0],[0,1,0],[1,1,0]], #J
				[[0,1,0],[0,1,0],[0,1,1]], #L
				[[1,1,1],[0,1,0],[0,0,0]] #T
				]
class Piece:
	def __init__(self):
		self.color = random.choice(COLORLIST)
		self.pos = {'x':3, 'y':-5}
		self.template = random.choice(TEMPLATES)
		self.width = len(self.template)


def drawTrash():
	for y in range(ROWCOUNT):
		for x in range(COLUMNCOUNT):
			color = TRASH[y][x] 
			if color != BLANK:
				drawSquare(color,x,y)
def fill(piece):
	for y in range(piece.width):
		for x in range(piece.width):
			if piece.template[y][x]:
				trashy = piece.pos['y'] + y
				trashx = piece.pos['x'] + x
				if trashy >= 0:
					TRASH[trashy][trashx] = piece.color

def canMove(piece,direction):
	j, i = DELTS[direction]
	for y in range(piece.width):
		for x in range(piece.width):
			if piece.template[y][x]:
				checkx = piece.pos['x'] + x + i
				checky = piece.pos['y'] + y + j
				if checkx < 0 or checkx >= COLUMNCOUNT or checky >= ROWCOUNT or (checky>0 and TRASH[checky][checkx] != BLANK):
					return False
	return True

def validPosition(template,piecex,piecey,direction=NONE):
	j, i = DELTS[direction]
	for y, row in enumerate(template):
		for x, val in enumerate(row):
			if val:
				checkx = piecex + x + i
				checky = piecey + y + j
				if checkx < 0 or checkx >= COLUMNCOUNT or checky >= ROWCOUNT or (checky>0 and TRASH[checky][checkx] != BLANK):
					return False
	return True

def writeAtLocation(text,x,y,pos = 'topleft'):
	textSurf = BASICFONT.render(text,True,WHITE)
	textRect = textSurf.get_rect()
	if pos == 'topleft':
		textRect.topleft = x, y
	else:
		print('text position error')
		terminate()
	DISPLAYSURF.blit(textSurf,textRect)

def terminate():
	pygame.quit()
	sys.exit()

def drawScore(score):
	writeAtLocation("Score: {}".format(score),PLAYRIGHT+INFOMARGIN,PLAYTOP)

def drawNextPiece():
	drawx, drawy = PLAYRIGHT + INFOMARGIN, PLAYTOP + 30
	writeAtLocation('Next piece',drawx,drawy)
	spacing = 30
	innerspacing = 5
	nextRect = pygame.Rect(drawx,drawy+spacing, CELLSIZE * 4 + 2 * innerspacing, CELLSIZE * 4  + 2 * innerspacing)
	pygame.draw.rect(DISPLAYSURF,BLACK,nextRect)
	drawPiece(NEXTPIECE,(drawy+spacing+innerspacing,drawx+innerspacing))



def rotate(template, direction):
	if direction == CW:
		return [[template[y][x] for y in range(len(template)-1,-1,-1)] for x in range(len(template))]
	elif direction == CCW:
		return [[template[y][x] for y in range(len(template))] for x in range(len(template)-1,-1,-1)]

def drawGrid():
	playRect = pygame.Rect(XMARGIN,YMARGIN,GRIDWIDTH,GRIDHEIGHT)
	pygame.draw.rect(DISPLAYSURF,BLACK,playRect)
	for x in range(PLAYLEFT,PLAYRIGHT,CELLSIZE):
		pygame.draw.line(DISPLAYSURF,GRAY,(x,PLAYTOP),(x,PLAYBOTTOM))
	for y in range(PLAYTOP,PLAYBOTTOM,CELLSIZE):
		pygame.draw.line(DISPLAYSURF,GRAY,(PLAYLEFT,y),(PLAYRIGHT,y))

def drawSquare(color,x,y,absolute=False):
	if not absolute:
		squareRect = pygame.Rect(x*CELLSIZE + XMARGIN, y*CELLSIZE + YMARGIN, CELLSIZE, CELLSIZE)
	else:
		squareRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
	pygame.draw.rect(DISPLAYSURF,color,squareRect)

def cyclePieces():
	global CURRENTPIECE, NEXTPIECE
	fill(CURRENTPIECE)
	CURRENTPIECE = NEXTPIECE
	NEXTPIECE = Piece()

def gravity():
	global DROPCOUNTER
	if DROPCOUNTER <= 0:
		if canMove(CURRENTPIECE,DOWN):
			CURRENTPIECE.pos['y'] +=1
		else:
			if outOfBounds(CURRENTPIECE):
				return 'quit'
			else:
				cyclePieces()
				clearLines()
		DROPCOUNTER = DROPTIME
	else:
		DROPCOUNTER -= 1

def drop(piece):
	while canMove(piece,DOWN):
		piece.pos['y'] += 1

def lineFull(row):
	for x in range(COLUMNCOUNT):
		if TRASH[row][x] == BLANK:
			return False
	return True

def pullDown(row):
	if row == 0:
		TRASH[0] = [BLANK] * COLUMNCOUNT
	else:
		for i, val in enumerate(TRASH[row-1]):
			TRASH[row][i] = val

def clearLines():
	global TRASH, SCORE
	for row in range(ROWCOUNT):
		if lineFull(row):
			SCORE+=1
			setDifficulty(SCORE)
			for pullRow in range(row,-1,-1):
				pullDown(pullRow)
	return

def runGame():
	global CURRENTPIECE, NEXTPIECE, DROPCOUNTER, TRASH, SCORE
	SCORE = 0

	TRASH = []	
	for _ in range(ROWCOUNT):
		TRASH.append([BLANK] * COLUMNCOUNT)
	CURRENTPIECE = Piece()
	NEXTPIECE = Piece()
	moving = None
	movingDown = None
	rotate_dir = None

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_RIGHT:
					moving = RIGHT
					holdWait = HOLDWAITMAX
					firstTouch = True
				elif event.key == K_LEFT:
					moving = LEFT
					holdWait = HOLDWAITMAX
					firstTouch = True
				elif event.key == K_DOWN:
					movingDown = True
					holdWait = HOLDWAITMAX
					firstTouch = True	
				elif event.key == K_a:
					rotate_dir = CCW
				elif event.key == K_s:
					rotate_dir = CW
				elif event.key == K_SPACE:
					moving = None
					movingDown = False
					rotate_dir = None
					drop(CURRENTPIECE)
				elif event.key == K_ESCAPE:
					terminate()
			elif event.type == KEYUP:
				if event.key == K_RIGHT:
					if moving == RIGHT:
						moving = None
				elif event.key == K_LEFT:
					if moving == LEFT:
						moving = None
				elif event.key == K_DOWN:
					movingDown = False

		if rotate_dir:
			new_template = rotate(CURRENTPIECE.template,rotate_dir)
			if validPosition(new_template,CURRENTPIECE.pos['x'],CURRENTPIECE.pos['y']):
				CURRENTPIECE.template = new_template
			rotate_dir = None
		if moving:
			if firstTouch or holdWait < 1:
				if canMove(CURRENTPIECE,moving):
					dy, dx = DELTS[moving]
					CURRENTPIECE.pos['x'] += dx
					CURRENTPIECE.pos['y'] += dy
				firstTouch = False
			else:
				holdWait -= 1
		if movingDown:
			if firstTouch or holdWait < 1:
				if canMove(CURRENTPIECE,DOWN):
					dy, dx = DELTS[DOWN]
					CURRENTPIECE.pos['x'] += dx
					CURRENTPIECE.pos['y'] += dy
				firstTouch = False
			else:
				holdWait -= 1			
		if moving == DOWN and canMove(CURRENTPIECE,DOWN):
			DROPCOUNTER = DROPTIME

		quitFlag = gravity()
		if quitFlag:
			return


		DISPLAYSURF.fill(BGCOLOR)
		drawGrid()
		drawTrash()
		drawScore(SCORE)
		drawNextPiece()
		drawPiece(CURRENTPIECE)
		pygame.display.update()

		FPSCLOCK.tick(FPS)

def setDifficulty(score):
	global DROPTIME
	DROPTIME = max(1, DROPTIMEMAX - SCORE // DIFFICULTYRATE)

def drawPiece(piece, pos = None):
	if pos == None:
		for y in range(piece.width):
			for x in range(piece.width):
				if piece.template[y][x] and y + piece.pos['y'] >= 0:
					drawSquare(piece.color,x+piece.pos['x'],y+piece.pos['y'])
	else:
		absy, absx = pos
		for y in range(piece.width):
			for x in range(piece.width):
				if piece.template[y][x]:
					dx = x * CELLSIZE
					dy = y * CELLSIZE
					drawSquare(piece.color,absx + dx,absy+dy,True)

def showGameOverScreen():
	gameOverFont = pygame.font.Font('freesansbold.ttf',80)
	gameSurf = gameOverFont.render('Game Over',True,WHITE)
	gameRect = gameSurf.get_rect()
	gameRect.center = WINDOWWIDTH / 2, YMARGIN / 2

	DISPLAYSURF.blit(gameSurf,gameRect)

	pygame.display.update()
	pygame.time.wait(1500)

	while True:
		return

def outOfBounds(piece):
	for x in range(piece.width):
		for y in range(piece.width):
			if piece.template[y][x] and piece.pos['y'] + y < 0:
				return True
	return False

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('TETRIS')

	while True:
		runGame()
		showGameOverScreen()

if __name__=='__main__':
	main()