"""
File: sierpinski.py
Name: 姜佳成
---------------------------
This file recursively prints the Sierpinski triangle on GWindow.
The Sierpinski triangle is a fractal described in 1915 by Waclaw Sierpinski.
It is a self similar structure that occurs at different levels of iterations.
"""

from campy.graphics.gobjects import GLine
from campy.gui.events.timer import pause
from sierpinski_class import Sierpinski
from math import sqrt as sq

# Constants
ORDER = 6                  # Controls the order of Sierpinski Triangle
OFFSET = 0.5			   # Make the corner of triangles smoother
LENGTH = 600               # The length of order 1 Sierpinski Triangle
UPPER_LEFT_X = 150		   # The upper left x coordinate of order 1 Sierpinski Triangle
UPPER_LEFT_Y = 100         # The upper left y coordinate of order 1 Sierpinski Triangle
WINDOW_WIDTH = 950         # The width of the GWindow
WINDOW_HEIGHT = 700        # The height of the GWindow


def main():
	"""
	This program prints Sierpinski Triangle corresponding to given order.
	Modify constant "ORDER" to obtain different level of Sierpinski Triangle.
	"""
	program = Sierpinski(WINDOW_WIDTH, WINDOW_HEIGHT)
	while True:
		if program.program_active:
			sierpinski_triangle(program, ORDER, LENGTH, OFFSET, UPPER_LEFT_X, UPPER_LEFT_Y)
			program.set_turn_off_active()
			program.set_turn_on_finish()
		pause(60)


def sierpinski_triangle(program, order, length, offset, upper_left_x, upper_left_y):
	"""
	:param program: The class to control draw or clear.
	:param order: Draws Sierpinski Triangle patterns corresponding to given order.
	:param length: Length of level_1 Sierpinski Triangle.
	:param offset: To make the corners of triangle smoother.
	:param upper_left_x: The upper-left x coordinate of level_1 Sierpinski Triangle.
	:param upper_left_y: The upper-left y coordinate of level_1 Sierpinski Triangle.
	:return: Sierpinski Triangle of given order will be displayed on window.
	"""
	if order == 0:  # Base case
		pass
	else:
		line_1 = GLine(upper_left_x, upper_left_y, upper_left_x+length, upper_left_y)
		line_2 = GLine(upper_left_x+length, upper_left_y, upper_left_x+0.5*length-offset, upper_left_y+sq(0.75)*length)
		line_3 = GLine(upper_left_x+0.5*length+offset, upper_left_y+sq(0.75)*length, upper_left_x, upper_left_y)

		program.window.add(line_1)
		pause(10)
		program.window.add(line_2)
		pause(10)
		program.window.add(line_3)
		pause(10)

		# Top-left
		sierpinski_triangle(program, order-1, length/2, offset, upper_left_x, upper_left_y)
		# Top-right
		sierpinski_triangle(program, order-1, length/2, offset, upper_left_x+length/2, upper_left_y)
		# Bottom
		sierpinski_triangle(program, order-1, length/2, offset, upper_left_x+length/4, upper_left_y+(length/2)*sq(0.75))


if __name__ == '__main__':
	main()
