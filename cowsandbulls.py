import os
import re
import random

HUMAN = 'human'
COMPUTER = 'computer'

class Board:
	_secret = []
	_history = []

	def valid(self,x):
		if re.match('^\d{4}$',x):
			return True
		return False
	def add_secret(self,x):
		if self.valid(x):
			self._secret = list(x)
			return 0
		else:
			return -1
	def get_secret(self):
		return ''.join(self._secret)

	def check(self,guess):
		bulls = 0
		cows = 0
		cows_and_bulls = 0
		count = [0] * 10
		for i in [int(x) for x in guess]:
			count[i] += 1
		for i in [int(x) for x in self._secret]:
			count[i] -= 1
		cows_and_bulls = 4-sum([abs(x) for x in count])//2
		bulls = sum([a==b for a,b in zip(guess,self._secret)])
		cows = cows_and_bulls - bulls

		if bulls:
			return (' '.join(['X']*bulls) + ' ' + ' '.join(['O'] * cows))
		else:
			return (' '.join(['O'] * cows))

	def add_history(self,guess,resp):
		self._history.append(guess + ':  ' + resp)

	def show_history(self):
		return '\n'.join(self._history)

BOARD = Board()

def check_quit(x):
	if x =='q':
		os._exit(1)
	return x

def get_player():
	while True:
		try:
			x = int(check_quit(input().strip()))
		except:
			print("I don't understand!")
		if x == 1:
			return HUMAN
		elif x == 2:
			return COMPUTER
		else:
			print("Number not in range.")

def setup():
	print('Welcome to Cows and Bulls! \n\nYou get 10 chances to guess a secret number from 0000 to 9999. \
You get an X for each correct digit in the right place and an O for each digit in the wrong place.\
\nPress q at any time to quit.')
	print('\nType 1 or 2 to: \n1. Guess the number\n2. Pick the number.')
	return get_player()

def human_game():
	BOARD.add_secret(str(random.randint(0,9999)).zfill(4))
	print('Guess!'.format(BOARD.get_secret()))
	for i in range(1,11):
		print ('Turn {}:'.format(i))
		while True:
			x = check_quit(input().strip())
			if BOARD.valid(x):
				resp = BOARD.check(x)
				if resp == 'X X X X ':
					return i
				BOARD.add_history(x,resp)
				print('')
				print(BOARD.show_history())
				break
			else:
				print('The secret is a 4-digit number 0000 to 9999.')
	return 11

def computer_game():
	print ("I can't do this yet. Sorry.")
	return 9999
	print("Add the secret:")
	while True:
		if BOARD.add_secret(input().strip()) == 0:
			break
		else:
			print('The secret is a 4-digit number 0000 to 9999.')
	return 4

def play_again(count,player):
	if count > 10:
		print('Out of moves... ', end ='')
	elif player == HUMAN:
		if count == 1:
			print('You won in 1 move. ',end='')
		else:
			print('You won in {} moves. '.format(count),end='')
	else:
		if count == 1:
			print('It took the computer 1 move. ',end='')
		else:
			print('It took the computer {} moves. '.format(count),end='')
	print('Play again?\n1. Guess the number.\n2. Pick the number.')
	return get_player()

if __name__=='__main__':
	player = setup()
	while True:
		if player == HUMAN:
			count = human_game()
		else:
			count = computer_game()
		player = play_again(count,player)