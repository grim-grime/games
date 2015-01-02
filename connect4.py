import sys
from pprint import pprint

WIDTH = 7
HEIGHT = 6
BLANK = '_'
PLAYER = 'X'
POINTS = [[(x+i,y) for i in range(4)] for x in range(WIDTH-3) for y in range(HEIGHT)]
POINTS += [[(x,y+i) for i in range(4)] for x in range(WIDTH) for y in range(HEIGHT-3)]
POINTS += [[(x+i,y+i)for i in range(4)] for x in range(WIDTH-3) for y in range(HEIGHT-3)]
POINTS += [[(x+i,y-i) for i in range(4)] for x in range(WIDTH-3) for y in range(3,HEIGHT)]

class Board:
	_ar = [[BLANK for _ in range(WIDTH)] for _ in range(HEIGHT)]
	def move(self,move):
		try:
			idx = int(move) - 1
		except:
			print("I don't understand!")
			return False
		if idx < 0 or idx >= WIDTH:
			print('Out of range!')
			return False
		for i in range(HEIGHT-1,-1,-1):
			if self._ar[i][idx] == BLANK:
				self._ar[i][idx] = PLAYER
				return True
		print('Column full!')
		return False
	def format(self):
		return '\n'.join([' '.join(r) for r in self._ar]) + '\n1 2 3 4 5 6 7'
	def over(self):
		for line in POINTS:
			if set([self._ar[y][x] for x,y in line]) in [set('X'),set('O')]:
				return True
		return False
	def full(self):
		for row in self._ar:
			if BLANK in row:
				return False
		return True
	def refresh(self):
		self._ar = [[BLANK for _ in range(WIDTH)] for _ in range(HEIGHT)]
BOARD = Board()


def instructions():
	message = '''\nWelcome to Connect 4!
To play, type the column you wish to play in.
Press 'q' to quit.\n'''

	print(message)

def check_quit(x):
	if x[0].lower() == 'q':
		sys.exit()

def change_player():
	global PLAYER
	if PLAYER == 'X':
		PLAYER = 'O'
	else:
		PLAYER = 'X'

def game():
	turn = 1
	while not BOARD.over():
		if BOARD.full():
			return 'No one'
		print('Turn {}:'.format(turn))
		change_player()
		print(BOARD.format())
		while True:
			move = input()
			check_quit(move)
			if BOARD.move(move):
				break
		turn += 1
	return PLAYER

def game_over(winner):
	print('GAME OVER')
	print(BOARD.format())
	print("{} won!".format(winner))
	print("Play again?")
	resp = input()
	if resp[0].lower() == 'y':
		BOARD.refresh()
		return
	else:
		sys.exit()


if __name__ == '__main__':
	instructions()
	while True:
		winner = game()
		game_over(winner)