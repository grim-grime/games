import sys
import random

BLANK = '_'
PLAYER = 'O'


COMBOS=[[1,5,9],[3,5,7],[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9]]

class Board:
	_ar = [['_' for _ in range(3)] for _ in range(3)]
	remaining = list(range(9))
	def set(self,move):
		idx = int(move) - 1
		self.remaining.remove(idx)
		self._ar[idx//3][idx%3] = PLAYER
	def get(self,move):
		idx = int(move) - 1
		return self._ar[idx//3][idx%3]
	def format(self):
		return ('\n'.join([' '.join(row) for row in self._ar]))
	def valid(self,move):
		idx = int(move) - 1
		if idx < 0 or idx > 8:
			print('Out of bounds!')
			return False
		if self._ar[idx//3][idx%3] != BLANK:
			print('Space is already occupied!')
			return False
		return True
	def refresh(self):
		self._ar = [[BLANK for _ in range(3)] for _ in range(3)]
		self.remaining = list(range(9))
		PLAYER = 'O'
	def __init__(self,string):
		string = string.split()
		self._ar = [string[3*i:3*i+3] for i in range(3)]
	def over(self):
		for combo in COMBOS:
			if len(set([self.get(m) for m in combo])) <= 1 and self.get(combo[0]) != BLANK:
				return True
		return False



BOARD = Board(' '.join([BLANK] * 9))



def check_for_exit(inp):
	if inp[0].lower() == 'q':
		sys.exit()


def change_player():
	global PLAYER
	if PLAYER == 'O':
		PLAYER = 'X'
	else:
		PLAYER = 'O'

def ai_move():
	return str(random.choice(BOARD.remaining) + 1)

def setup():
	message = '''Welcome to tic-tac-toe!
To make a move, input the number of the corresponding square:'''

	print(message)
	print('')
	print(Board('1 2 3 4 5 6 7 8 9').format())
	print('')

	print('Would you like to play against a human or computer?')
	if any([x[0].lower()=='c' for x in input().split()]):
			print("Playing a computer!")
			return 1
	print("Playing a human!")
	return 2

def game(players):
	turn = 0
	while not BOARD.over() and turn < 9:
		print(BOARD.format())
		change_player()
		turn += 1
		if turn %2 == 0 and players == 1:
			move = ai_move()
		else:
			while True:
				move = input()
				check_for_exit(move)
				if BOARD.valid(move):
					break
		BOARD.set(move)
		print('')

	if turn == 9:
		return 'No one'
	else:
		return PLAYER

def game_over(winner):
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
	players = setup()
	while True:
		winner = game(players)
		game_over(winner)