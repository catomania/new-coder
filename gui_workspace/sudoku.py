import argparse
from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM # what do these things from Tkinter do?

BOARDS = ['debug', 'n00b', 'l33t', 'error'] # list of sudoku boards available
MARGIN = 20 # pixels around board
SIDE = 50 # Width of each board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9 # Width and height of whole board is 20 * 2 + 50 + 9 

class SudokuError(Exception): # In the future, we'll use this error class to pass our own error messages
	"""
	An application specific error.
	"""
	pass

class SudokuUI(Frame): # Frame is a rectangular region on a screen
	"""
	The Tkinter UI, responsible for drawing the board and accepting user input
	"""
	def __init__(self, parent, game):
		self.parent = parent # all widgets belong to a parent
		self.game = game
		Frame.__init__(self, parent)

		self.row, self.col = 0, 0 # initialize row and col to use later

		self.__initUI() # calls the initUI function

	def __initUI(self):
		self.parent.title("Sudoku") # our parent window will be called Sudoku
		self.pack(fill=BOTH, expand=1) # Frame attribute, organizes geometry relative to parent, fill options: both, none, x, y
		self.canvas = Canvas(self, 
							 width=WIDTH,
							 height=HEIGHT)
		self.canvas.pack(fill=BOTH, side=TOP) # canvas attribute, helps display our board
		clear_button = Button(self,
							  text="Clear answers",
							  command=self.__clear_answers)
		clear_button.pack(fill=BOTH, side=BOTTOM) # Clear button is at the bottom and fills the space

		self.__draw_grid() # helper functions
		self.__draw_puzzle()

		self.canvas.bind("<Button-1>", self.__cell_clicked) # binds Button-1 to a callback, another method: cell_clicked
		# in Tkinter, Button-1 is a default left mouse click
		self.canvas.bind("<Key>", self.__key_pressed) # binds the key (guesed number) to the key presseed method

	def __draw_grid(self): # make the sudoku layout, do all private functions take self and then other potential arguments?
		"""
		Draws grid divided with blue lines into 3x3 squares
		"""

		for i in xrange(10):
			color = "blue" if i % 3 == 0 else "gray" # blue lines if divisible by 3

			# draw vertical lines
			x0 = MARGIN + i * SIDE 
			y0 = MARGIN
			x1 = MARGIN + i * SIDE
			y1 = HEIGHT - MARGIN
			self.canvas_create_line(x0, y0, x1, y1, fill=color) # draw the vertical lines coordinates are (x0, y0) (x1, y1)

			# draw horizontal lines
			x0 = MARGIN
			y0 = MARGIN + i * SIDE
			x1 = WIDTH - MARGIN
			y1 = MARGIN + i * SIDE
			self.canvas_create_line(x0, y0, x1, y1, fill=color)

	def __draw_puzzle(self):
		self.canvas.delete("numbers") # delete old numbers? hrm?
		for i in xrange(9):
			for j in xrange(9:):
				answer = self.game.puzzle[i][j]
				if answer != 0:
					x = MARGIN + j * SIDE + SIDE / 2 # in the middle of the applicable cell

	def __draw_cursor(self):
		self.canvas.delete("cursor")
		if self.row >= 0 and self.col >= 0: # you set these variables as 0 first in init
		x0 = MARGIN + self.col * SIDE + 1
		y0 = MARGIN + self.row * SIDE + 1
		x1 = MARGIN + (self.col + 1) * SIDE - 1
		y1 = MARGIN + (self.row + 1) * SIDE - 1
		self.canvas.create_rectange(
			x0, y0, x1, y1,
			outline="red", tags="cursor")



class SudokuBoard(object):
	"""
	Sudoku Board representation, the wonders of OOP
	"""
	def __init__(self, board_file): # when a new board is created, it should initialize w/ the name of the .sudoku file
		self.board = board_file # set self.board = to private function

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
			board.append([]) # empty list for each line (9 lines)

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

		# Return the constructed board, which is a list of lists at this point
		return board

class SudokuGame(object): # creates actual board for game
	"""
	A Sudoku game, in charge of storing the state of the board and checking
	whether the puzzle is completed.
	"""
	def __init__(self, board_file):
		self.board_file = board_file # because you set self.board = board_file in class SudokuBoard
		self.start_puzzle = SudokuBoard(board_file).board # 'gets' .board from the init method of SudokuBoard, why do you do this?

	def start(self):
		self.game_over = False # flag to see if game is over or not
		self.puzzle = []  # create a copy of the puzzle
		for i in xrange(9): # create a copy of the puzzle
			self.puzzle.append([])  # makes 9 empty lists, which will contain 9 [j] values for each [i] (81 values total)
			for j in xrange(9): # for each empty list made from above, append X nine times
				self.puzzle[i].append(self.start_puzzle[i][j]) # put in the numbers from the SudokuBoard(board_file).board 

	def check_win(self): # function to check board's rows, columns, and each 3x3 square
		for row in xrange(9): #why is range different from xrange? is one a generator?
			if not self.__check_row(row): # helper functions
				return False 
		for column in xrange(9): # 0 to 8
			if not self.__check_column(column):
				return False
		for row in xrange(3):
			for column in xrange(3):
				if not self.__check_square(row, column):
					return False
		self.game_over = True #set flag to True
		return True # flag for winning the game?

	def __check_block(self, block): # main logic method
	# set: http://www.programiz.com/python-programming/set
	# what's the block? puzzle(row) ?
		return set(block) == set(range(1, 10)) # set: no repeats

	def __check_row(self, row): 
		return self.__check_block(self.puzzle[row])

	def __check_column(self, column):
		return self.__check_block(
			[self.puzzle[row][column] for row in xrange(9)] #[i][j]
		)

	def __check_square(self, row, column): # what does each line of code do here? Do row and column here mean 9 numbers?
		return self.__check_block(
			[
				self.puzzle[r][c] # self.puzzle[0, 1 2][0, 1 2], which grabs a 3x3 square
				for r in xrange(row * 3, (row + 1) * 3) # what is being calculated here? it's a 3x3 square... (0, 3) (3, 6) 
				for c in xrange(column * 3, (column + 1) * 3) 

				]
			)












