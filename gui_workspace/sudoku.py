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

def parse_arguments():
	"""
	Parses arguments of the form:
		sudoku.py <board name>
	Where 'board name' must be in the 'BOARD' list
	"""

	# example input: python sudoku.py --board n00b 
	# your --board is a flag

	arg_parser = argparse.ArgumentParser() # instantiate ArgumentParser from the argparse library
	arg_parser.add_argument("--board", 
							help="Desired board name",
							type=str,
							choices=BOARDS,
							required=True)

	# Creates a dictionary of keys = argument flag, and value = argument
	args = vars(arg_parser.parse_args()) # parse_args is from the argparse library, vars makes a dict

	# ArgumentParser parses arguments through the parse_args() method, which inspects the CL, converts each arg to the specified type 
	# and invokes the 'appropriate' action

	return args['board'] # board is the dict key, this returns you the name of the board like --board n00b 

	# so basically you get the name of the board from the CLI input



class SudokuUI(Frame): # Frame is a rectangular region on a screen
	"""
	The Tkinter UI, responsible for drawing the board and accepting user input
	"""
	def __init__(self, parent, game):
		self.game = game
		Frame.__init__(self, parent)
		self.parent = parent # all widgets belong to a parent
		
		self.row, self.col = -1, -1 # initialize row and col to use later

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
			self.canvas.create_line(x0, y0, x1, y1, fill=color) # draw the vertical lines coordinates are (x0, y0) (x1, y1)

			# draw horizontal lines
			x0 = MARGIN
			y0 = MARGIN + i * SIDE
			x1 = WIDTH - MARGIN
			y1 = MARGIN + i * SIDE
			self.canvas.create_line(x0, y0, x1, y1, fill=color)

	def __draw_puzzle(self):
		self.canvas.delete("numbers") # delete old numbers?
		for i in xrange(9):
			for j in xrange(9):
				answer = self.game.puzzle[i][j]
				if answer != 0:
					x = MARGIN + j * SIDE + SIDE / 2 # in the middle of the applicable cell
					y = MARGIN + i * SIDE + SIDE / 2
					original = self.game.start_puzzle[i][j]
					color = "black" if answer == original else "sea green"
					self.canvas.create_text(
						x, y, text=answer, tags="numbers", fill=color

						)

	def __draw_cursor(self):
		self.canvas.delete("cursor")
		if self.row >= 0 and self.col >= 0: # you set these variables as 0 first in init
			x0 = MARGIN + self.col * SIDE + 1 # what does -1 do to these variables?
	 		y0 = MARGIN + self.row * SIDE + 1
			x1 = MARGIN + (self.col + 1) * SIDE - 1
			y1 = MARGIN + (self.row + 1) * SIDE - 1
			self.canvas.create_rectangle(
				x0, y0, x1, y1,
				outline="red", tags="cursor")

	def __draw_victory(self):
		# creates an oval/circle
		x0 = y0 = MARGIN + SIDE * 2 # upper left box of circle starts margin + 2 rows in
		x1 = y1 = MARGIN + SIDE * 7
		self.canvas.create_oval(
			x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")

		# create text
		x = y = MARGIN + 4 * SIDE + SIDE / 2 # middle of the circle
		self.canvas.create_text(
			x, y,
			text="You win!", tags="victory",
			fill="white", font=("Arial", 32)
		)

	def __cell_clicked(self, event): # event parameter: gives us x&y coordinates of where user clicked
		if self.game.game_over:
			return # do nothing if game is over

		x, y = event.x, event.y
		if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN): # if our puzzle grid is clicked
			self.canvas.focus_set() # focus_set: move focus to a widget

			# get row and col numbers from x, y coordinates
			row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE

			# if cell was selected already, another click should de-select it
			if (row, col) == (self.row, self.col):
				self.row, self.col = -1, -1 # I assume -1 means de-selecting?
			elif self.game.puzzle[row][col] == 0: # otherwise, grab corresponding cell 
				self.row, self.col = row, col
			else:
				self.row, self.col = -1, -1 

			self.__draw_cursor()



	def __key_pressed(self, event):
		if self.game.game_over:
			return 
		if self.row >= 0 and self.col >= 0 and event.char in "1234567890": # where does event.char come from? tkinter?
			self.game.puzzle[self.row][self.col] = int(event.char)
			self.col, self.row = -1, -1
			self.__draw_puzzle()
			self.__draw_cursor()
			if self.game.check_win(): # every time you enter in a number, the game checks to see if you have won
				self.__draw_victory()

	def __clear_answers(self):
		self.game.start()
		self.canvas.delete("victory") # remove the victory circle
		self.__draw_puzzle()

class SudokuBoard(object): # attribute canvas_create_line??
	"""
	Sudoku Board representation, the wonders of OOP
	"""
	def __init__(self, board_file): # when a new board is created, it should initialize w/ the name of the .sudoku file
		self.board = self.__create_board(board_file) # set self.board = to private function

	def __create_board(self, board_file):
		# create an initial matrix, or a list of a list
		board = []

		# iterate over each line
		for line in board_file: # what type of input is board_file?
			line = line.strip()  # strip method: removes all whitespace at start and end

			# raise error if line is longer or shorter than 9 characters
			if len(line) != 9:
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

if __name__ == '__main__':
	board_name = parse_arguments() # parse_arguments() returns board name

	with open('%s.sudoku' % board_name, 'r') as boards_file: # what is boards_file?
		game = SudokuGame(boards_file) # create a SudokuGame object
		game.start()

		root = Tk() # I always see this line of code w/ Tkinter tutorials, no need to assign the instantiated SudokuUI class
		SudokuUI(root, game)
		root.geometry("%dx%d" % (WIDTH, HEIGHT + 40)) # draw root slightly larger
		root.mainloop()  # I see this line as well in Tkinter programs, this is what starts the program














