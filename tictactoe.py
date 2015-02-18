import sys
import random
import copy
import operator
from timeit import default_timer as time
import math
import random


BLANK = '_'
PLAYER = 'O'

COMBOS=[[1,5,9],[3,5,7],[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9]]

class Board:
	def set(self,move,player=PLAYER):
		idx = int(move) - 1
		self.remaining.remove(idx)
		self._ar[idx//3][idx%3] = player
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
		global PLAYER
		self._ar = [[BLANK for _ in range(3)] for _ in range(3)]
		self.remaining = list(range(9))
		PLAYER = 'O'
	def __init__(self,string):
		string = string.split()
		self._ar = [string[3*i:3*i+3] for i in range(3)]
		self.remaining = list(range(9))
	def get_winner(self):
		for combo in COMBOS:
			if len(set([self.get(m) for m in combo])) <= 1 and self.get(combo[0]) != BLANK:
				return self.get(combo[0])
		if all(self.get(i) != BLANK for i in range(1,9)):
			return 'No one'
		return None



BOARD = Board(' '.join([BLANK] * 9))



def check_for_exit(inp):
	if inp[0].lower() == 'q':
		sys.exit()


def change_player():
	global PLAYER
	PLAYER = other(PLAYER)

def other(player):
	if player == 'X':
		return 'O'
	else:
		return 'X'
		
def ai_move(alpha,beta,depth,board,player):
	winner = board.get_winner()
	if winner:
		if winner == PLAYER:
			return (1, -1)
		elif winner == other(PLAYER):
			return (-1, -1)
		else:
			return (0, -1)
	else:
		if player == PLAYER:
			bestval, bestmove = -2, -1
			for move in sorted([i+1 for i in board.remaining],key=lambda x: random.random()):
				newboard = copy.deepcopy(board)
				newboard.set(move,player)
				newval, newmove = ai_move(alpha,beta,depth-1,newboard,other(player))
				if newval > bestval:
					bestval = newval
					bestmove = move
				alpha = max(alpha,newval)
				if beta <= alpha:
					break
			return (bestval, bestmove)
				
				

		else:
			bestval, bestmove = 2, -1
			for move in sorted([i+1 for i in board.remaining],key=lambda x: random.random()):
				newboard = copy.deepcopy(board)
				newboard.set(move,player)
				newval, newmove = ai_move(alpha,beta,depth-1,newboard,other(player))
				if newval < bestval:
					bestval = newval
					bestmove = move
				beta = min(beta,newval)
				if beta <= alpha:
					break
			return (bestval, bestmove)


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
	if players == 1:
		human_turn = random.choice([True,False])
		if human_turn:
			print('You go first!')
		else:
			print('Computer goes first!')
	while not BOARD.get_winner():
		print(BOARD.format())
		change_player()
		if players == 1:
			if human_turn:
				while True:
					move = input()
					check_for_exit(move)
					if BOARD.valid(move):
						break
			else:
				start = time()
				move = ai_move(float('-inf'),float('inf'),4,BOARD,PLAYER)
				move = move[1]
				end = time()
				t = end - start
				rounded_t = round(t,-math.floor(math.log10(t))+2)
			human_turn ^= True
		else:
			while True:
				move = input()
				check_for_exit(move)
				if BOARD.valid(move):
					break
		BOARD.set(move,PLAYER)
		print('')

	return BOARD.get_winner()

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