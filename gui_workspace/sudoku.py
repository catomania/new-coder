import argparse
from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARDS = ['debug', 'n00b', 'l33t', 'error'] # sudoku boards available
MARGIN = 20 # pixels around board
SIDE = 50 # Width of each board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9 # Width and height of whole board is 20 * 2 + 50 + 9 

class SudokuError(Exception): # In the future, we'll use this error class to pass our own error messages
	"""
	An application specific error.
	"""
	pass

class SudokuBoard(object):
	"""
	Sudoku Board representation, the wonders of OOP
	"""
	def __init__(self, board_file): # when a new board is created, it should initialize w/ the name of the .sudoku file
		self.board = board_file

	def __create_board(self, board_file):
		# create an initial matrix, or a list of a list
		board = []

		# iterate over each line
		for line in board_file: # what type of input is board_file?
			line = line.strip()  # strip method: removes all whitespace at start and end

			# raise error if line is longer or shorter than 9 characters
			if len(line) != 9:
				board = [] # this line exists on www but not in the reference script
				raise SudokuError(
					"Each line in the sudoku puzzle must be 9 chars long") 

			# create a list for the line
			board.append([]) # empty list for each line 

			# then iterate over each character
			for c in line:
				# Raise an error if the character is not an integer
				if not c.isdigit():
					raise SudokuError(
						"Valid characters for a sudoku puzzle must be 0-9")
					# Add to the latest list for the line, -1 means end of list
					board[-1].append(int(c))

		# Raise an error if there are not 9 lines
		if len(board) != 9: 
			raise SudokuError("Each sudoku puzzle must have 9 lines")

		# Return the constructed board
		return board

class SudokuGame(object):
	"""
	A Sudoku game, in charge of storing the state of the board and checking
	whether the puzzle is completed.
	"""
	def __init__(self, board_file):
		self.board_file = board_file
		self.start_puzzle = SudokuBoard(board_file).board # .board here calls the board method from the SudokuBoard class