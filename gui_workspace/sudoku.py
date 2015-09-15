import argparse
from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARDS = ['debug', 'n00b', 'l33t', 'error'] # sudoku boards available
MARGIN = 20 # pixels around board
SIDE = 50 # Width of each board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9 # Width and height of whole board is 20 * 2 + 50 + 9 

class SudokuError(Exception):
	"""
	An application specific error.
	"""
	pass
	