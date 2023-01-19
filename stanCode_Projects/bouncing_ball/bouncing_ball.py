"""
File: bouncing_ball.py
Name: 姜佳成
-------------------------
This file simulates the animation of a free-falling ball.
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

# Constants
VX = 3
DELAY = 10
GRAVITY = 1
SIZE = 20
REDUCE = 0.9
START_X = 30
START_Y = 40

# Global variables
window = GWindow(800, 500, title='bouncing_ball.py')
ball = GOval(SIZE, SIZE)
click_lock = False  # To lock the function after clicking until the ball is out of window.
count = 0  # To count how many times the ball is out of window.


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    ball.filled = True
    ball.color = 'black'
    window.add(ball, START_X, START_Y)
    onmouseclicked(bouncing_ball)


def bouncing_ball(_):
    """
    This function simulates the animation of a free-falling ball.
    Click the mouse to start animation and it will be locked after playing for 3 times.
    """
    global click_lock, count
    vy = 0
    if click_lock is False and count < 3:
        click_lock = True  # Lock the function after clicking.
        while True:
            vy += GRAVITY
    # ------------ Determine how does the ball move ------------
            if ball.y + ball.height + vy >= window.height:
                ball.move(VX, window.height - ball.y - ball.height)  # Make sure the ball hits ground and bounce.
                vy *= -REDUCE  # Switch moving direction and y-velocity decreases by REDUCE after every bouncing.
            else:
                ball.move(VX, vy)
    # ------------ Check if the ball is out of window ------------
            if ball.x >= window.width:
                count += 1
                window.remove(ball)  # Remove the ball which is out of window.
                window.add(ball, START_X, START_Y)  # Put a new ball at start point.
                click_lock = False  # Unlock the function.
                break
            pause(DELAY)


if __name__ == "__main__":
    main()
