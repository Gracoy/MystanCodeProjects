"""
File: draw_line.py
Name: 姜佳成
-------------------------
This file let user draw straight lines in a blank window.
"""

from campy.graphics.gobjects import GOval, GLine
from campy.graphics.gwindow import GWindow
from campy.gui.events.mouse import onmouseclicked

# Constants
SIZE = 10
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

# Global variables
window = GWindow(WINDOW_WIDTH, WINDOW_HEIGHT)
start_x, start_y = 0, 0  # GLine needs 4 positional args, so coordinate of line start must be global variable.
line_start = True  # To determine the click is line start or line end.


def main():
    """
    This program creates lines on an instance of GWindow class.
    There is a circle indicating the user’s first click. A line appears
    at the condition where the circle disappears as the user clicks
    on the canvas for the second time.
    """
    onmouseclicked(draw_line)


def draw_line(event):
    """
    This function puts a circle at line start and remove it when a line is created.
    Click the mouse to define line start and line end.

    :param event: Click mouse to provide coordinates for function.
    """
    global start_x, start_y, line_start
    # ------------ Coordinate of line start ------------
    if line_start:
        start_x, start_y = event.x, event.y  # Record x,y of line start
        start_point = GOval(SIZE, SIZE)
        window.add(start_point, start_x - SIZE / 2, start_y - SIZE / 2)
        line_start = False
    # ------------ Coordinate of line end ------------
    elif line_start is False:
        window.remove(window.get_object_at(start_x, start_y))
        line = GLine(start_x, start_y, event.x, event.y)
        window.add(line)
        line_start = True


if __name__ == "__main__":
    main()
