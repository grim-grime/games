import pygame, sys
from pygame.locals import *
import random

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

WHITECOLOR = 255, 255, 255
BLACKCOLOR = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
DARKGREEN = 0, 130, 0
DARKGRAY = 40, 40, 40
BLUE = 0, 0, 155
GRAY = 120, 120, 120
ORANGE = 255,127,0
YELLOW = 255,255,0
GREEN=0,255,0
TEAL = 0, 255, 255
PINK = 255,0,255
PURPLE = 127,0,255
BROWN = 150,100,0

BGCOLOR = BLACKCOLOR
BOARDCOLOR = DARKGREEN

BLANK = 0
BLACK = 1
WHITE = 2

ROWS = 8

INFOWIDTH = WINDOWWIDTH - WINDOWHEIGHT
PLAYWIDTH= WINDOWWIDTH - INFOWIDTH

CELLSIZE = 50
PIECERADIUS = CELLSIZE //2 - 3

XMARGIN = (PLAYWIDTH - ROWS * CELLSIZE) //2
YMARGIN = (WINDOWHEIGHT - ROWS * CELLSIZE) // 2
FONTSIZE = 24
DELTS = []
for dx in range(-1,2):
	for dy in range(-1,2):
		DELTS.append((dy,dx))
DELTS.remove((0,0))

def drawInfo():

	if PLAYER == BLACK:
		playerText = 'Black'
	else:
		playerText = 'White'

	#xcenter = (PLAYWIDTH - XMARGIN + WINDOWWIDTH) // 2

	playerSurf = BASICFONT.render('Turn: {}'.format(playerText),True,WHITECOLOR)
	playerRect = playerSurf.get_rect()
	xalign = PLAYWIDTH - 50
	yalign = YMARGIN + 100
	playerRect.topleft = xalign, yalign
	DISPLAYSURF.blit(playerSurf,playerRect)

	whiteScore = 0
	blackScore = 0
	for row in BOARD:
		whiteScore += row.count(WHITE)
		blackScore += row.count(BLACK)

	whiteSurf = BASICFONT.render('White: {}'.format(whiteScore),True,WHITECOLOR)
	blackSurf = BASICFONT.render('Black: {}'.format(blackScore),True,WHITECOLOR)
	whiteRect = whiteSurf.get_rect()
	blackRect = blackSurf.get_rect()
	whiteRect.topleft = xalign, yalign + 50
	blackRect.topleft = xalign, yalign + 100
	DISPLAYSURF.blit(blackSurf,blackRect)
	DISPLAYSURF.blit(whiteSurf,whiteRect)




def drawBoard():
	boardRect = pygame.Rect(XMARGIN,YMARGIN,ROWS*CELLSIZE,ROWS*CELLSIZE)
	pygame.draw.rect(DISPLAYSURF,BOARDCOLOR,boardRect)
	for x in range(XMARGIN,XMARGIN+ROWS*CELLSIZE+1,CELLSIZE):
		pygame.draw.line(DISPLAYSURF,BLACKCOLOR,(x,YMARGIN),(x,WINDOWHEIGHT-YMARGIN))
	for y in range(YMARGIN,YMARGIN+ROWS*CELLSIZE+1,CELLSIZE):
		pygame.draw.line(DISPLAYSURF,BLACKCOLOR,(XMARGIN,y),(PLAYWIDTH-XMARGIN,y))	

def drawPieces():
	for j in range(ROWS):
		for i in range(ROWS):
			drawPiece(BOARD[j][i],j,i)

def drawPiece(piece,y,x):
	if piece == BLACK:
		color = BLACKCOLOR
	elif piece == WHITE:
		color = WHITECOLOR
	else:
		return

	center = (XMARGIN+x*CELLSIZE + CELLSIZE//2, YMARGIN+y*CELLSIZE + CELLSIZE // 2)
	pygame.draw.circle(DISPLAYSURF,color,center,PIECERADIUS)

def terminate():
	pygame.quit()
	sys.exit()

def gameOverScreen():
	terminate()

def other(player):
	if player == BLACK:
		return WHITE
	return BLACK

def valid(j,i):
	if not inBounds(j,i):
		return False
	if BOARD[j][i] != BLANK:
		return False
	if not any( hasFriend(PLAYER,j,i,dj,di) for dj, di in DELTS ):
		return False
	return True


def inBounds(j,i):
	return j >=0 and j < ROWS and i >=0 and i < ROWS

def hasFriend(player,j,i,dj,di):
	newj,newi = j+dj,i+di
	if inBounds(newj,newi) and BOARD[newj][newi] == other(player):
		newj+=dj
		newi+=di
		while inBounds(newj,newi) and BOARD[newj][newi]!=BLANK:
			if BOARD[newj][newi] == player:
				return True
			newj+=dj
			newi+=di
	return False

def flip(j,i):
	player = BOARD[j][i]
	for dj, di in DELTS:
		if hasFriend(player,j,i,dj,di):
			newj, newi = j+dj, i+di
			while inBounds(newj,newi) and BOARD[newj][newi] == other(player):
				BOARD[newj][newi] = player


def runGame():
	global BOARD, PLAYER
	doneMode = False
	checkInput = True
	change = False

	BOARD = []
	for _ in range(ROWS):
		BOARD.append( [BLANK] * ROWS )
	PLAYER = BLACK

	configVals = ((3,3,BLACK),(4,4,BLACK),(3,4,WHITE),(4,3,WHITE))
	for j,i,color in configVals:
		BOARD[j][i]=color

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == MOUSEBUTTONUP:
				checkInput = True
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()
		if checkInput:
			mousex, mousey = pygame.mouse.get_pos()
			j, i = (mousey - YMARGIN) // CELLSIZE, (mousex - XMARGIN) // CELLSIZE
			if valid(j,i):
				BOARD[j][i] = PLAYER
				flip(j,i)
				PLAYER = other(PLAYER)
			checkInput = False

			DISPLAYSURF.fill(BGCOLOR)
			drawBoard()
			drawPieces()
			drawInfo()
			pygame.display.update()
		FPSCLOCK.tick(FPS)


def main():
	global FPSCLOCK,DISPLAYSURF, BASICFONT


	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf',FONTSIZE)
	pygame.display.set_caption("This is a game.")

	while True:
		splashPage()
		runGame()

def splashPage():
	return
if __name__ == '__main__':
	main()