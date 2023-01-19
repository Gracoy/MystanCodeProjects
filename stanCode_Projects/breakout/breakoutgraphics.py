"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 3  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40  # Width of a brick (in pixels)
BRICK_HEIGHT = 16  # Height of a brick (in pixels)
BRICK_ROWS = 10  # Number of rows of bricks
BRICK_COLS = 10  # Number of columns of bricks
BRICK_OFFSET = 100  # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 15  # Radius of the ball (in pixels)
PADDLE_WIDTH = 100  # Width of the paddle (in pixels)
PADDLE_HEIGHT = 14  # Height of the paddle (in pixels)
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels)
GAME_LIVES = 3


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        self.__game_menu = True
        self.__game_over = False
        self.__score_history = False
        self.__start_game = False

        self.__ball_exist = False
        self.__bonus_ball_exist = False
        self.__drop_bonus = False
        self.__catch_bonus = False
        self.__bonus_time_counter = False
        self.__trigger_bonus = False
        self.__bonus1_dropped, self.__bonus2_dropped, self.__bonus3_dropped = False, False, False
        self.__trigger_bonus1, self.__trigger_bonus2, self.__trigger_bonus3 = False, False, False

        self.__vx = 0  # Velocity of original ball
        self.__vy = 0
        self.__vx_b = 0  # Velocity of bonus ball
        self.__vy_b = 0
        self.__total_v = 10  # V_x^2 + V_y^2 = V_total^2

        self.__score_list = []  # To record score
        self.__brick_number = 0
        self.__score = 0
        self.__bonus_condition = 0
        self.__bonus_time_remain = 5

        self._paddle_width = paddle_width
        self._paddle_height = paddle_height
        self._paddle_offset = paddle_offset
        self._ball_radius = ball_radius
        self._brick_height = brick_height
        self.__game_lives = GAME_LIVES

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height - 100, title=title)

        # Create game labels
        self.__main_menu = GLabel('Break Out')
        self.__main_menu.font = 'Times New Roman-50-bold'

        self.__start_icon = GLabel('-- Start --')
        self.__start_icon.font = 'Times New Roman-36-bold'

        self.__gamelose = GLabel('Game Over')
        self.__gamelose.font = 'Times New Roman-48-bold'

        self.__gamewin = GLabel('You Win')
        self.__gamewin.font = 'Times New Roman-48-bold'

        self.__continue_icon = GLabel('-- Continue --')
        self.__continue_icon.font = 'Times New Roman-36-bold'

        self.__back_to_menu = GLabel('-- Back to menu --')
        self.__back_to_menu.font = 'Times New Roman-36-bold'

        self.__score_recorder = GLabel(f'Score: {str(self.__score)}')
        self.__score_recorder.font = 'Times New Roman-20'

        self.__top1 = GLabel('')
        self.__top2 = GLabel('')
        self.__top3 = GLabel('')
        self.__top4 = GLabel('')
        self.__top5 = GLabel('')

        # Create game rectangles
        self.paddle = GRect(self._paddle_width, self._paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'

        self._bricks = GRect(BRICK_WIDTH, BRICK_HEIGHT)

        self.__bonus1 = GRect(BRICK_WIDTH, BRICK_HEIGHT)
        self.__bonus1.filled = True
        self.__bonus1.fill_color = 'lime'

        self.__bonus2 = GRect(BRICK_WIDTH, BRICK_HEIGHT)
        self.__bonus2.filled = True
        self.__bonus2.fill_color = 'lime'

        self.__bonus3 = GRect(BRICK_WIDTH, BRICK_HEIGHT)
        self.__bonus3.filled = True
        self.__bonus3.fill_color = 'lime'

        self.__bonus4 = GRect(BRICK_WIDTH, BRICK_HEIGHT)
        self.__bonus4.filled = True
        self.__bonus4.fill_color = 'lime'

        self.__bonus5 = GRect(BRICK_WIDTH, BRICK_HEIGHT)
        self.__bonus5.filled = True
        self.__bonus5.fill_color = 'lime'

        self.__bonus6 = GRect(BRICK_WIDTH, BRICK_HEIGHT)
        self.__bonus6.filled = True
        self.__bonus6.fill_color = 'lime'

        self.__blank_bonus_cube = GRect(15, 15)

        self.__bonus1_cube = GRect(15, 15)
        self.__bonus1_cube.filled = True
        self.__bonus1_cube.fill_color = 'pink'
        self.__bonus1_cube.color = 'pink'

        self.__bonus2_cube = GRect(15, 15)
        self.__bonus2_cube.filled = True
        self.__bonus2_cube.fill_color = 'blue'
        self.__bonus2_cube.color = 'blue'

        self.__bonus3_cube = GRect(15, 15)
        self.__bonus3_cube.filled = True
        self.__bonus3_cube.fill_color = 'red'
        self.__bonus3_cube.color = 'red'

        # Create game ovals
        self.ball = GOval(self._ball_radius, self._ball_radius)
        self.ball.filled = True
        self.ball.fill_color = 'black'

        self.bonus_ball = GOval(self._ball_radius, self._ball_radius)
        self.bonus_ball.filled = True
        self.bonus_ball.fill_color = 'red'
        self.bonus_ball.color = 'red'

        self.__lives1 = GOval(20, 20)
        self.__lives1.filled = True
        self.__lives1.fill_color = 'black'

        self.__lives2 = GOval(20, 20)
        self.__lives2.filled = True
        self.__lives2.fill_color = 'black'

        self.__lives3 = GOval(20, 20)
        self.__lives3.filled = True
        self.__lives3.fill_color = 'black'

        self.__lives4 = GOval(20, 20)
        self.__lives4.filled = True
        self.__lives4.fill_color = 'black'

        self.__lives5 = GOval(20, 20)
        self.__lives5.filled = True
        self.__lives5.fill_color = 'black'

        self.__lives6 = GOval(20, 20)
        self.__lives6.filled = True
        self.__lives6.fill_color = 'black'

        self.__lives7 = GOval(20, 20)
        self.__lives7.filled = True
        self.__lives7.fill_color = 'black'

        self.__lives8 = GOval(20, 20)
        self.__lives8.filled = True
        self.__lives8.fill_color = 'black'

        self.__lives9 = GOval(20, 20)
        self.__lives9.filled = True
        self.__lives9.fill_color = 'black'

        # Initialize our mouse listeners
        onmouseclicked(self.lunch_ball)
        onmousemoved(self.move_paddle)

    # ------------------------ Getters ------------------------
    def get_if_game_menu(self):
        return self.__game_menu

    def get_if_game_start(self):
        return self.__start_game

    def get_if_game_over(self):
        return self.__game_over

    def get_if_score_history(self):
        return self.__score_history

    def get_vx(self):
        return self.__vx

    def get_vy(self):
        return self.__vy

    def get_vx_b(self):
        return self.__vx_b

    def get_vy_b(self):
        return self.__vy_b

    def get_if_ball_exist(self):
        return self.__ball_exist

    def get_if_bonus_ball_exist(self):
        return self.__bonus_ball_exist

    def get_brick_remain(self):
        return self.__brick_number

    def get_bonus1_cube(self):
        return self.__bonus1_cube

    def get_bonus2_cube(self):
        return self.__bonus2_cube

    def get_bonus3_cube(self):
        return self.__bonus3_cube

    def get_if_catch_bonus(self):
        return self.__catch_bonus

    def get_bonus_time_counter(self):
        return self.__bonus_time_counter

    def get_bonus_time_remain(self):
        return self.__bonus_time_remain

    def get_game_lives_remain(self):
        return self.__game_lives

    # ------------------------ Setters ------------------------
    def set_game_menu(self):
        for i in range(1, BRICK_ROWS + 1):
            for j in range(1, BRICK_COLS + 1):
                self._bricks = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                self._bricks.filled = True
                if 0 < j <= 2:
                    self._bricks.fill_color = 'dimgray'
                    self._bricks.color = 'dimgray'
                elif 2 < j <= 4:
                    self._bricks.fill_color = 'gray'
                    self._bricks.color = 'gray'
                elif 4 < j <= 6:
                    self._bricks.fill_color = 'silver'
                    self._bricks.color = 'silver'
                elif 6 < j <= 8:
                    self._bricks.fill_color = 'lightgray'
                    self._bricks.color = 'lightgray'
                elif 8 < j <= 10:
                    self._bricks.fill_color = 'gainsboro'
                    self._bricks.color = 'gainsboro'
                if (i - 1) == 6 and (j - 1) == 9 or (i - 1) == 7 and (j - 1) == 9 or (i - 1) == 8 and (j - 1) == 9 or \
                        (i - 1) == 7 and (j - 1) == 8 or (i - 1) == 2 and (j - 1) == 9 or (i - 1) == 2 and (j - 1) == 8:
                    pass
                else:
                    self.window.add(self._bricks, (i - 1) * BRICK_SPACING + (i - 1) * BRICK_WIDTH,
                                    (j - 1) * BRICK_SPACING + (j - 1) * BRICK_HEIGHT + 80)

        self.window.add(self.paddle, (self.window.width - self._paddle_width) / 2-50,
                        self.window.height - self._paddle_offset)
        self.window.add(self.ball, (self.window.width - self.ball.width) / 2+50,
                        (self.window.height - self.ball.height) / 2+70)
        self.window.add(self.__main_menu, (self.window.width - self.__main_menu.width) / 2, 250)
        self.window.add(self.__start_icon, (self.window.width - self.__start_icon.width) / 2, 450)

        while True:
            if not self.__game_menu:
                self.window.clear()
                break
            self.window.add(self.__start_icon)
            pause(300)
            self.window.remove(self.__start_icon)
            pause(300)

    def set_score_history(self):
        self.window.clear()
        if len(self.__score_list) == 1:
            self.__top1 = GLabel(f'TOP 1: {str(sorted(self.__score_list, reverse=True)[0])}')
            self.__top2 = GLabel('TOP 2: _____')
            self.__top3 = GLabel('TOP 3: _____')
            self.__top4 = GLabel('TOP 4: _____')
            self.__top5 = GLabel('TOP 5: _____')
        elif len(self.__score_list) == 2:
            self.__top1 = GLabel(f'TOP 1: {str(sorted(self.__score_list, reverse=True)[0])}')
            self.__top2 = GLabel(f'TOP 2: {str(sorted(self.__score_list, reverse=True)[1])}')
            self.__top3 = GLabel('TOP 3: _____')
            self.__top4 = GLabel('TOP 4: _____')
            self.__top5 = GLabel('TOP 5: _____')
        elif len(self.__score_list) == 3:
            self.__top1 = GLabel(f'TOP 1: {str(sorted(self.__score_list, reverse=True)[0])}')
            self.__top2 = GLabel(f'TOP 2: {str(sorted(self.__score_list, reverse=True)[1])}')
            self.__top3 = GLabel(f'TOP 3: {str(sorted(self.__score_list, reverse=True)[2])}')
            self.__top4 = GLabel('TOP 4: _____')
            self.__top5 = GLabel('TOP 5: _____')
        elif len(self.__score_list) == 4:
            self.__top1 = GLabel(f'TOP 1: {str(sorted(self.__score_list, reverse=True)[0])}')
            self.__top2 = GLabel(f'TOP 2: {str(sorted(self.__score_list, reverse=True)[1])}')
            self.__top3 = GLabel(f'TOP 3: {str(sorted(self.__score_list, reverse=True)[2])}')
            self.__top4 = GLabel(f'TOP 4: {str(sorted(self.__score_list, reverse=True)[3])}')
            self.__top5 = GLabel('TOP 5: _____')
        elif len(self.__score_list) >= 4:
            self.__top1 = GLabel(f'TOP 1: {str(sorted(self.__score_list, reverse=True)[0])}')
            self.__top2 = GLabel(f'TOP 2: {str(sorted(self.__score_list, reverse=True)[1])}')
            self.__top3 = GLabel(f'TOP 3: {str(sorted(self.__score_list, reverse=True)[2])}')
            self.__top4 = GLabel(f'TOP 4: {str(sorted(self.__score_list, reverse=True)[3])}')
            self.__top5 = GLabel(f'TOP 5: {str(sorted(self.__score_list, reverse=True)[4])}')

        self.__top1.font = 'Times New Roman-28-bold'
        self.__top2.font = 'Times New Roman-28-bold'
        self.__top3.font = 'Times New Roman-28-bold'
        self.__top4.font = 'Times New Roman-28-bold'
        self.__top5.font = 'Times New Roman-28-bold'

        self.window.add(self.__top1, self.window.width / 2 - 120, 150)
        self.window.add(self.__top2, self.window.width / 2 - 120, 200)
        self.window.add(self.__top3, self.window.width / 2 - 120, 250)
        self.window.add(self.__top4, self.window.width / 2 - 120, 300)
        self.window.add(self.__top5, self.window.width / 2 - 120, 350)
        self.window.add(self.__back_to_menu, (self.window.width - self.__back_to_menu.width) / 2, 450)

        while True:
            if not self.__score_history:
                self.window.clear()
                self.__game_menu = True
                self.__score_history = False
                break
            self.window.add(self.__back_to_menu)
            pause(300)
            self.window.remove(self.__back_to_menu)
            pause(300)

    def set_game(self):
        self.__vx, self.__vy, self.__vx_b, self.__vy_b = 0, 0, 0, 0
        self.__score_recorder.text = f'Score: {str(self.__score)}'
        self.window.add(self.paddle, (self.window.width - self.paddle.width) / 2,
                        self.window.height - self._paddle_offset)
        self.window.add(self.ball, self.paddle.x + (self.paddle.width - self.ball.width) / 2,
                        self.paddle.y - self.ball.height)
        self.window.add(self.__score_recorder, 8, self.__score_recorder.height + 12)

        if self.__game_lives == 1:
            self.window.add(self.__lives1, self.window.width - self.__game_lives * 25, 8)
        elif self.__game_lives == 2:
            self.window.add(self.__lives1, self.window.width - (self.__game_lives - 1) * 25, 8)
            self.window.add(self.__lives2, self.window.width - self.__game_lives * 25, 8)
        elif self.__game_lives == 3:
            self.window.add(self.__lives1, self.window.width - (self.__game_lives - 2) * 25, 8)
            self.window.add(self.__lives2, self.window.width - (self.__game_lives - 1) * 25, 8)
            self.window.add(self.__lives3, self.window.width - self.__game_lives * 25, 8)
        elif self.__game_lives == 4:
            self.window.add(self.__lives1, self.window.width - (self.__game_lives - 3) * 25, 8)
            self.window.add(self.__lives2, self.window.width - (self.__game_lives - 2) * 25, 8)
            self.window.add(self.__lives3, self.window.width - (self.__game_lives - 1) * 25, 8)
            self.window.add(self.__lives4, self.window.width - self.__game_lives * 25, 8)
        elif self.__game_lives == 5:
            self.window.add(self.__lives1, self.window.width - (self.__game_lives - 4) * 25, 8)
            self.window.add(self.__lives2, self.window.width - (self.__game_lives - 3) * 25, 8)
            self.window.add(self.__lives3, self.window.width - (self.__game_lives - 2) * 25, 8)
            self.window.add(self.__lives4, self.window.width - (self.__game_lives - 1) * 25, 8)
            self.window.add(self.__lives5, self.window.width - self.__game_lives * 25, 8)
        elif self.__game_lives == 6:
            self.window.add(self.__lives1, self.window.width - (self.__game_lives - 5) * 25, 8)
            self.window.add(self.__lives2, self.window.width - (self.__game_lives - 4) * 25, 8)
            self.window.add(self.__lives3, self.window.width - (self.__game_lives - 3) * 25, 8)
            self.window.add(self.__lives4, self.window.width - (self.__game_lives - 2) * 25, 8)
            self.window.add(self.__lives5, self.window.width - (self.__game_lives - 1) * 25, 8)
            self.window.add(self.__lives6, self.window.width - self.__game_lives * 25, 8)
        elif self.__game_lives == 7:
            self.window.add(self.__lives1, self.window.width - (self.__game_lives - 6) * 25, 8)
            self.window.add(self.__lives2, self.window.width - (self.__game_lives - 5) * 25, 8)
            self.window.add(self.__lives3, self.window.width - (self.__game_lives - 4) * 25, 8)
            self.window.add(self.__lives4, self.window.width - (self.__game_lives - 3) * 25, 8)
            self.window.add(self.__lives5, self.window.width - (self.__game_lives - 2) * 25, 8)
            self.window.add(self.__lives6, self.window.width - (self.__game_lives - 1) * 25, 8)
            self.window.add(self.__lives7, self.window.width - self.__game_lives * 25, 8)
        elif self.__game_lives == 8:
            self.window.add(self.__lives1, self.window.width - (self.__game_lives - 7) * 25, 8)
            self.window.add(self.__lives2, self.window.width - (self.__game_lives - 6) * 25, 8)
            self.window.add(self.__lives3, self.window.width - (self.__game_lives - 5) * 25, 8)
            self.window.add(self.__lives4, self.window.width - (self.__game_lives - 4) * 25, 8)
            self.window.add(self.__lives5, self.window.width - (self.__game_lives - 3) * 25, 8)
            self.window.add(self.__lives6, self.window.width - (self.__game_lives - 2) * 25, 8)
            self.window.add(self.__lives7, self.window.width - (self.__game_lives - 1) * 25, 8)
            self.window.add(self.__lives8, self.window.width - self.__game_lives * 25, 8)
        elif self.__game_lives == 9:
            self.window.add(self.__lives1, self.window.width - (self.__game_lives - 8) * 25, 8)
            self.window.add(self.__lives2, self.window.width - (self.__game_lives - 7) * 25, 8)
            self.window.add(self.__lives3, self.window.width - (self.__game_lives - 6) * 25, 8)
            self.window.add(self.__lives4, self.window.width - (self.__game_lives - 5) * 25, 8)
            self.window.add(self.__lives5, self.window.width - (self.__game_lives - 4) * 25, 8)
            self.window.add(self.__lives6, self.window.width - (self.__game_lives - 3) * 25, 8)
            self.window.add(self.__lives7, self.window.width - (self.__game_lives - 2) * 25, 8)
            self.window.add(self.__lives8, self.window.width - (self.__game_lives - 1) * 25, 8)
            self.window.add(self.__lives9, self.window.width - self.__game_lives * 25, 8)

        for i in range(1, BRICK_ROWS + 1):
            for j in range(1, BRICK_COLS + 1):
                self._bricks = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                self._bricks.filled = True
                self._bricks.fill_color = 'yellow'
                if (i - 1) == 2 and (j - 1) == 1 or (i - 1) == 2 and (j - 1) == 4 or (i - 1) == 2 and (j - 1) == 8 or \
                        (i - 1) == 7 and (j - 1) == 1 or (i - 1) == 7 and (j - 1) == 4 or (i - 1) == 7 and (j - 1) == 8:
                    pass
                else:
                    self.window.add(self._bricks, (i - 1) * BRICK_SPACING + (i - 1) * BRICK_WIDTH,
                                    (j - 1) * BRICK_SPACING + (j - 1) * BRICK_HEIGHT + BRICK_OFFSET)
                    self.__brick_number += 1

        self.window.add(self.__bonus1, 2 * (BRICK_SPACING + BRICK_WIDTH),
                        1 * (BRICK_SPACING + BRICK_HEIGHT) + BRICK_OFFSET)
        self.window.add(self.__bonus2, 7 * (BRICK_SPACING + BRICK_WIDTH),
                        1 * (BRICK_SPACING + BRICK_HEIGHT) + BRICK_OFFSET)
        self.window.add(self.__bonus3, 2 * (BRICK_SPACING + BRICK_WIDTH),
                        4 * (BRICK_SPACING + BRICK_HEIGHT) + BRICK_OFFSET)
        self.window.add(self.__bonus4, 7 * (BRICK_SPACING + BRICK_WIDTH),
                        4 * (BRICK_SPACING + BRICK_HEIGHT) + BRICK_OFFSET)
        self.window.add(self.__bonus5, 2 * (BRICK_SPACING + BRICK_WIDTH),
                        8 * (BRICK_SPACING + BRICK_HEIGHT) + BRICK_OFFSET)
        self.window.add(self.__bonus6, 7 * (BRICK_SPACING + BRICK_WIDTH),
                        8 * (BRICK_SPACING + BRICK_HEIGHT) + BRICK_OFFSET)
        self.__brick_number += 6

    def set_game_result(self):
        self.window.remove(self.paddle)
        self.window.remove(self.ball)
        self.__bonus_ball_exist = False
        self.__bonus1_dropped, self.__bonus2_dropped, self.__bonus3_dropped = False, False, False

        if self.__game_lives == 0:
            self.window.add(self.__gamelose, (self.window.width - self.__gamelose.width) / 2, self.window.height / 2)
        elif self.__brick_number == 0:
            self.window.add(self.__gamewin, (self.window.width - self.__gamewin.width) / 2, self.window.height / 2)
            pause(700)

            while self.__game_lives != 0:
                if self.__game_lives == 1:
                    self.__score += 500
                    self.window.remove(self.__lives1)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                elif self.__game_lives == 2:
                    self.__score += 500
                    self.window.remove(self.__lives2)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                elif self.__game_lives == 3:
                    self.__score += 500
                    self.window.remove(self.__lives3)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                elif self.__game_lives == 4:
                    self.__score += 500
                    self.window.remove(self.__lives4)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                elif self.__game_lives == 5:
                    self.__score += 500
                    self.window.remove(self.__lives5)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                elif self.__game_lives == 6:
                    self.__score += 500
                    self.window.remove(self.__lives6)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                elif self.__game_lives == 7:
                    self.__score += 500
                    self.window.remove(self.__lives7)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                elif self.__game_lives == 8:
                    self.__score += 500
                    self.window.remove(self.__lives8)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                elif self.__game_lives == 9:
                    self.__score += 500
                    self.window.remove(self.__lives9)
                    self.__score_recorder.text = f'Score: {str(self.__score)}'
                    pause(300)
                self.__game_lives -= 1

        self.__score_list.append(self.__score)  # Record score of each play
        pause(1000)
        self.__game_over = True
        self.__game_lives = 3
        self.__score = 0

        while True:
            if self.__score_history:
                self.window.clear()
                break
            self.window.add(self.__continue_icon, (self.window.width - self.__continue_icon.width) / 2, 450)
            pause(300)
            self.window.remove(self.__continue_icon)
            pause(300)
        self.__start_game = False

    def set_remove_bonus_ball(self):
        self.window.remove(self.bonus_ball)
        self.__bonus_ball_exist = False

    def set_reset_bonus(self):
        self.__bonus_time_counter = False
        self.__bonus_time_remain = 5
        self.window.remove(self.paddle)
        self._paddle_width = 100
        self.paddle = GRect(self._paddle_width, self._paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle, (self.window.width - self.paddle.width) / 2,
                        self.window.height - self._paddle_offset)

    def set_restart_game(self):
        self.__start_game = False
        self.__ball_exist = False
        self.__bonus_ball_exist = False
        self.__bonus_time_remain = 5
        self.__vx, self.__vy, self.__vx_b, self.__vy_b = 0, 0, 0, 0

        self.ball.x, self.ball.y = self.paddle.x + (
                    self.paddle.width - self.ball.width) / 2, self.paddle.y - self.ball.height

        self.window.remove(self.paddle)
        self._paddle_width = 100
        self.paddle = GRect(self._paddle_width, self._paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle, (self.window.width - self.paddle.width) / 2,
                        self.window.height - self._paddle_offset)

        if self.__game_lives == 1:
            self.window.remove(self.__lives1)
        elif self.__game_lives == 2:
            self.window.remove(self.__lives2)
        elif self.__game_lives == 3:
            self.window.remove(self.__lives3)
        elif self.__game_lives == 4:
            self.window.remove(self.__lives4)
        elif self.__game_lives == 5:
            self.window.remove(self.__lives5)
        elif self.__game_lives == 6:
            self.window.remove(self.__lives6)
        elif self.__game_lives == 7:
            self.window.remove(self.__lives7)
        elif self.__game_lives == 8:
            self.window.remove(self.__lives8)
        elif self.__game_lives == 9:
            self.window.remove(self.__lives9)

        self.__game_lives -= 1

    # ------------------------ Methods ------------------------
    def lunch_ball(self, event):
        """
        Lunch the ball and switch every screen by clicking mouse.
        """
        if self.__game_over and self.window.get_object_at(event.x, event.y) is self.__continue_icon:
            self.__game_over = False
            self.__score_history = True

        elif self.__score_history and self.window.get_object_at(event.x, event.y) is self.__back_to_menu:
            self.__score_history = False
            self.__game_menu = True

        elif self.get_if_game_menu() and self.window.get_object_at(event.x, event.y) is self.__start_icon:
            self.__game_menu = False

        elif not self.get_if_game_start() and \
                self.window.get_object_at(8, self.__score_recorder.height + 12) is self.__score_recorder:
            self.__ball_exist = True
            self.__vx = random.randint(self.__total_v - 7, self.__total_v - 5)
            if random.random() > 0.5:
                self.__vx *= -1
            self.__vy = -int((self.__total_v ** 2 - self.__vx ** 2) ** 0.5)
            self.__start_game = True

    def reset_velocity(self):
        """
        Reset ball velocity when it meets paddle.
        If the ball hits top of paddle, reverse y-velocity and x-velocity is given according to the
        position of paddle that the ball hit.
        If the ball hits sides of paddle, only reverse x-velocity.
        """
        if self.ball.y + self.ball.height <= self.paddle.y:
            if self.paddle.x + self.paddle.width * 0.5 > self.ball.x + self.ball.width / 2 > \
                    self.paddle.x + self.paddle.width * 0.25:
                self.__vx = -random.randint(self.__total_v - 7, self.__total_v - 5)
            elif self.paddle.x + self.paddle.width * 0.25 > self.ball.x + self.ball.width / 2 > self.paddle.x:
                self.__vx = -random.randint(self.__total_v - 4, self.__total_v - 2)
            elif self.paddle.x + self.paddle.width * 0.75 > self.ball.x + self.ball.width / 2 > \
                    self.paddle.x + self.paddle.width * 0.5:
                self.__vx = random.randint(self.__total_v - 7, self.__total_v - 5)
            else:
                self.__vx = random.randint(self.__total_v - 4, self.__total_v - 2)
            self.__vy = -int((self.__total_v ** 2 - self.__vx ** 2) ** 0.5)

        elif self.ball.y + self.ball.height > self.paddle.y:
            self.__vx *= -1

    def move_paddle(self, event):
        """
        Move the paddle by mouse-moving when game is playing.
        The paddle edge will not be over window boundary.
        """
        if not self.__game_over and not self.__game_menu and \
                self.window.get_object_at(8, self.__score_recorder.height + 12) is self.__score_recorder:
            self.paddle.x = event.x - self.paddle.width / 2
            if self.paddle.x < 0:
                self.paddle.x = 0
            elif self.paddle.x + self.paddle.width > self.window.width:
                self.paddle.x = self.window.width - self.paddle.width
            if not self.get_if_game_start():
                self.ball.x = self.paddle.x + (self.paddle.width - self.ball.width) / 2

    def break_bricks_and_bound(self):
        """
        Break the brick which the ball hits and change moving direction
        according the condition of the ball hits bricks.
        Number of bricks remain will -1 after every brick-removing.
        """
        maybe_bricks_top_left = self.window.get_object_at(self.ball.x, self.ball.y)
        maybe_bricks_top_right = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        maybe_bricks_bottom_right = self.window.get_object_at(self.ball.x + self.ball.width,
                                                              self.ball.y + self.ball.height)
        maybe_bricks_bottom_left = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)

        maybe_bricks_bonus_top_left = self.window.get_object_at(self.bonus_ball.x, self.bonus_ball.y)
        maybe_bricks_bonus_top_right = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width,
                                                                 self.bonus_ball.y)
        maybe_bricks_bonus_bottom_right = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width,
                                                                    self.bonus_ball.y + self.bonus_ball.height)
        maybe_bricks_bonus_bottom_left = self.window.get_object_at(self.bonus_ball.x,
                                                                   self.bonus_ball.y + self.bonus_ball.height)

        # Consider objects above paddle and below score recorder as bricks.
        # If object height != brick height, ignore it
        if self.paddle.y - self.ball.height - 20 > self.ball.y > self.__score_recorder.height + 12:
            if maybe_bricks_top_left is not None and maybe_bricks_top_right is not None and self.__vy < 0 and \
                    maybe_bricks_top_left.height == self._brick_height and \
                    maybe_bricks_top_right.height == self._brick_height:
                if maybe_bricks_top_left is self.__bonus1 or maybe_bricks_top_left is self.__bonus2 or \
                        maybe_bricks_top_left is self.__bonus3 or maybe_bricks_top_left is self.__bonus4 or \
                        maybe_bricks_top_left is self.__bonus5 or maybe_bricks_top_left is self.__bonus6 or \
                        maybe_bricks_top_right is self.__bonus1 or maybe_bricks_top_right is self.__bonus2 or \
                        maybe_bricks_top_right is self.__bonus3 or maybe_bricks_top_right is self.__bonus4 or \
                        maybe_bricks_top_right is self.__bonus5 or maybe_bricks_top_right is self.__bonus6:
                    self.__drop_bonus = True
                    self.__brick_number -= 1
                    self.__score += 200  # Bonus bricks score +200
                    self.window.remove(maybe_bricks_top_left)
                    self.__vy *= -1
                else:
                    self.__brick_number -= 1
                    self.__score += 100
                    self.window.remove(maybe_bricks_top_left)
                    self.__vy *= -1

            elif maybe_bricks_bottom_left is not None and maybe_bricks_bottom_right is not None and self.__vy < 0 and \
                    maybe_bricks_bottom_left.height == self._brick_height and \
                    maybe_bricks_bottom_right.height == self._brick_height:
                if maybe_bricks_bottom_left is self.__bonus1 or maybe_bricks_bottom_left is self.__bonus2 or \
                        maybe_bricks_bottom_left is self.__bonus3 or maybe_bricks_bottom_left is self.__bonus4 or \
                        maybe_bricks_bottom_left is self.__bonus5 or maybe_bricks_bottom_left is self.__bonus6 or \
                        maybe_bricks_bottom_right is self.__bonus1 or maybe_bricks_bottom_right is self.__bonus2 or \
                        maybe_bricks_bottom_right is self.__bonus3 or maybe_bricks_bottom_right is self.__bonus4 or \
                        maybe_bricks_bottom_right is self.__bonus5 or maybe_bricks_bottom_right is self.__bonus6:
                    self.__drop_bonus = True
                    self.__brick_number -= 1
                    self.__score += 200
                    self.window.remove(maybe_bricks_bottom_left)
                    self.__vy *= -1
                else:
                    self.__brick_number -= 1
                    self.__score += 100
                    self.window.remove(maybe_bricks_bottom_left)
                    self.__vy *= -1

            elif maybe_bricks_top_left is not None and self.__vx < 0 and self.__vy < 0 and \
                    maybe_bricks_top_left.height == self._brick_height:
                if maybe_bricks_top_left is self.__bonus1 or maybe_bricks_top_left is self.__bonus2 or \
                        maybe_bricks_top_left is self.__bonus3 or maybe_bricks_top_left is self.__bonus4 or \
                        maybe_bricks_top_left is self.__bonus5 or maybe_bricks_top_left is self.__bonus6:
                    self.__drop_bonus = True
                    self.window.remove(maybe_bricks_top_left)
                    self.__brick_number -= 1
                    self.__score += 200
                    if self.ball.x < maybe_bricks_top_left.x + maybe_bricks_top_left.width - 5:
                        self.__vy *= -1
                    elif self.ball.x > maybe_bricks_top_left.x + maybe_bricks_top_left.width - 5:
                        self.__vx *= -1
                else:
                    self.window.remove(maybe_bricks_top_left)
                    self.__brick_number -= 1
                    self.__score += 100
                    if self.ball.x < maybe_bricks_top_left.x + maybe_bricks_top_left.width - 5:
                        self.__vy *= -1
                    elif self.ball.x > maybe_bricks_top_left.x + maybe_bricks_top_left.width - 5:
                        self.__vx *= -1

            elif maybe_bricks_top_right is not None and self.__vx > 0 > self.__vy and \
                    maybe_bricks_top_right.height == self._brick_height:
                if maybe_bricks_top_right is self.__bonus1 or maybe_bricks_top_right is self.__bonus2 or \
                        maybe_bricks_top_right is self.__bonus3 or maybe_bricks_top_right is self.__bonus4 or \
                        maybe_bricks_top_right is self.__bonus5 or maybe_bricks_top_right is self.__bonus6:
                    self.__drop_bonus = True
                    self.window.remove(maybe_bricks_top_right)
                    self.__brick_number -= 1
                    self.__score += 200
                    if self.ball.x < maybe_bricks_top_right.x + 5:
                        self.__vx *= -1
                    elif self.ball.x > maybe_bricks_top_right.x + 5:
                        self.__vy *= -1
                else:
                    self.window.remove(maybe_bricks_top_right)
                    self.__brick_number -= 1
                    self.__score += 100
                    if self.ball.x < maybe_bricks_top_right.x + 5:
                        self.__vx *= -1
                    elif self.ball.x > maybe_bricks_top_right.x + 5:
                        self.__vy *= -1

            elif maybe_bricks_bottom_right is not None and self.__vy > 0 and self.__vx > 0 and \
                    maybe_bricks_bottom_right.height == self._brick_height:
                if maybe_bricks_bottom_right is self.__bonus1 or maybe_bricks_bottom_right is self.__bonus2 or \
                        maybe_bricks_bottom_right is self.__bonus3 or maybe_bricks_bottom_right is self.__bonus4 or \
                        maybe_bricks_bottom_right is self.__bonus5 or maybe_bricks_bottom_right is self.__bonus6:
                    self.__drop_bonus = True
                    self.window.remove(maybe_bricks_bottom_right)
                    self.__brick_number -= 1
                    self.__score += 200
                    if self.ball.x < maybe_bricks_bottom_right.x + 5:
                        self.__vx *= -1
                    elif self.ball.x > maybe_bricks_bottom_right.x + 5:
                        self.__vy *= -1
                else:
                    self.window.remove(maybe_bricks_bottom_right)
                    self.__brick_number -= 1
                    self.__score += 100
                    if self.ball.x < maybe_bricks_bottom_right.x + 5:
                        self.__vx *= -1
                    elif self.ball.x > maybe_bricks_bottom_right.x + 5:
                        self.__vy *= -1

            elif maybe_bricks_bottom_left is not None and self.__vx < 0 < self.__vy and \
                    maybe_bricks_bottom_left.height == self._brick_height:
                if maybe_bricks_bottom_left is self.__bonus1 or maybe_bricks_bottom_left is self.__bonus2 or \
                        maybe_bricks_bottom_left is self.__bonus3 or maybe_bricks_bottom_left is self.__bonus4 or \
                        maybe_bricks_bottom_left is self.__bonus5 or maybe_bricks_bottom_left is self.__bonus6:
                    self.__drop_bonus = True
                    self.window.remove(maybe_bricks_bottom_left)
                    self.__brick_number -= 1
                    self.__score += 200
                    if self.ball.x < maybe_bricks_bottom_left.x + maybe_bricks_bottom_left.width - 5:
                        self.__vy *= -1
                    elif self.ball.x > maybe_bricks_bottom_left.x + maybe_bricks_bottom_left.width - 5:
                        self.__vx *= -1
                else:
                    self.window.remove(maybe_bricks_bottom_left)
                    self.__brick_number -= 1
                    self.__score += 100
                    if self.ball.x < maybe_bricks_bottom_left.x + maybe_bricks_bottom_left.width - 5:
                        self.__vy *= -1
                    elif self.ball.x > maybe_bricks_bottom_left.x + maybe_bricks_bottom_left.width - 5:
                        self.__vx *= -1
            self.__score_recorder.text = f'Score: {str(self.__score)}'

        # Below conditions are for bonus ball, same as original ball
        if self.paddle.y - self.bonus_ball.height - 20 > self.bonus_ball.y > self.__score_recorder.height + 12:
            if maybe_bricks_bonus_top_left is not None and maybe_bricks_bonus_top_right is not None and \
                    self.__vy_b < 0 and \
                    maybe_bricks_bonus_top_left.height == self._brick_height and \
                    maybe_bricks_bonus_top_right.height == self._brick_height:
                if maybe_bricks_bonus_top_left is self.__bonus1 or maybe_bricks_bonus_top_left is self.__bonus2 or \
                        maybe_bricks_bonus_top_left is self.__bonus3 or \
                        maybe_bricks_bonus_top_left is self.__bonus4 or \
                        maybe_bricks_bonus_top_left is self.__bonus5 or \
                        maybe_bricks_bonus_top_left is self.__bonus6 or \
                        maybe_bricks_bonus_top_right is self.__bonus1 or \
                        maybe_bricks_bonus_top_right is self.__bonus2 or \
                        maybe_bricks_bonus_top_right is self.__bonus3 or \
                        maybe_bricks_bonus_top_right is self.__bonus4 or \
                        maybe_bricks_bonus_top_right is self.__bonus5 or \
                        maybe_bricks_bonus_top_right is self.__bonus6:
                    self.__drop_bonus = True
                    self.__brick_number -= 1
                    self.__score += 200
                    self.window.remove(maybe_bricks_bonus_top_left)
                    self.__vy_b *= -1
                else:
                    self.__brick_number -= 1
                    self.__score += 100
                    self.window.remove(maybe_bricks_bonus_top_left)
                    self.__vy_b *= -1

            elif maybe_bricks_bonus_bottom_left is not None and maybe_bricks_bonus_bottom_right is not None and \
                    self.__vy_b < 0 and \
                    maybe_bricks_bonus_bottom_left.height == self._brick_height and \
                    maybe_bricks_bonus_bottom_right.height == self._brick_height:
                if maybe_bricks_bonus_bottom_left is self.__bonus1 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus2 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus3 or\
                        maybe_bricks_bonus_bottom_left is self.__bonus4 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus5 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus6 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus1 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus2 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus3 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus4 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus5 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus6:
                    self.__drop_bonus = True
                    self.__brick_number -= 1
                    self.__score += 200
                    self.window.remove(maybe_bricks_bonus_bottom_left)
                    self.__vy_b *= -1
                else:
                    self.__brick_number -= 1
                    self.__score += 100
                    self.window.remove(maybe_bricks_bonus_bottom_left)
                    self.__vy_b *= -1

            elif maybe_bricks_bonus_top_left is not None and self.__vx_b < 0 and self.__vy_b < 0 and \
                    maybe_bricks_bonus_top_left.height == self._brick_height:
                if maybe_bricks_bonus_top_left is self.__bonus1 or \
                        maybe_bricks_bonus_top_left is self.__bonus2 or \
                        maybe_bricks_bonus_top_left is self.__bonus3 or \
                        maybe_bricks_bonus_top_left is self.__bonus4 or \
                        maybe_bricks_bonus_top_left is self.__bonus5 or \
                        maybe_bricks_bonus_top_left is self.__bonus6:
                    self.__drop_bonus = True
                    self.window.remove(maybe_bricks_bonus_top_left)
                    self.__brick_number -= 1
                    self.__score += 200
                    if self.bonus_ball.x < maybe_bricks_bonus_top_left.x + maybe_bricks_bonus_top_left.width - 5:
                        self.__vy_b *= -1
                    elif self.bonus_ball.x > maybe_bricks_bonus_top_left.x + maybe_bricks_bonus_top_left.width - 5:
                        self.__vx_b *= -1
                else:
                    self.window.remove(maybe_bricks_bonus_top_left)
                    self.__brick_number -= 1
                    self.__score += 100
                    if self.bonus_ball.x < maybe_bricks_bonus_top_left.x + maybe_bricks_bonus_top_left.width - 5:
                        self.__vy_b *= -1
                    elif self.bonus_ball.x > maybe_bricks_bonus_top_left.x + maybe_bricks_bonus_top_left.width - 5:
                        self.__vx_b *= -1

            elif maybe_bricks_bonus_top_right is not None and self.__vx_b > 0 > self.__vy_b and \
                    maybe_bricks_bonus_top_right.height == self._brick_height:
                if maybe_bricks_bonus_top_right is self.__bonus1 or \
                        maybe_bricks_bonus_top_right is self.__bonus2 or \
                        maybe_bricks_bonus_top_right is self.__bonus3 or \
                        maybe_bricks_bonus_top_right is self.__bonus4 or \
                        maybe_bricks_bonus_top_right is self.__bonus5 or \
                        maybe_bricks_bonus_top_right is self.__bonus6:
                    self.__drop_bonus = True
                    self.window.remove(maybe_bricks_bonus_top_right)
                    self.__brick_number -= 1
                    self.__score += 200
                    if self.bonus_ball.x < maybe_bricks_bonus_top_right.x + 5:
                        self.__vx_b *= -1
                    elif self.bonus_ball.x > maybe_bricks_bonus_top_right.x + 5:
                        self.__vy_b *= -1
                else:
                    self.window.remove(maybe_bricks_bonus_top_right)
                    self.__brick_number -= 1
                    self.__score += 100
                    if self.bonus_ball.x < maybe_bricks_bonus_top_right.x + 5:
                        self.__vx_b *= -1
                    elif self.bonus_ball.x > maybe_bricks_bonus_top_right.x + 5:
                        self.__vy_b *= -1

            elif maybe_bricks_bonus_bottom_right is not None and self.__vy_b > 0 and self.__vx_b > 0 and \
                    maybe_bricks_bonus_bottom_right.height == self._brick_height:
                if maybe_bricks_bonus_bottom_right is self.__bonus1 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus2 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus3 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus4 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus5 or \
                        maybe_bricks_bonus_bottom_right is self.__bonus6:
                    self.__drop_bonus = True
                    self.window.remove(maybe_bricks_bonus_bottom_right)
                    self.__brick_number -= 1
                    self.__score += 200
                    if self.bonus_ball.x < maybe_bricks_bonus_bottom_right.x + 5:
                        self.__vx_b *= -1
                    elif self.bonus_ball.x > maybe_bricks_bonus_bottom_right.x + 5:
                        self.__vy_b *= -1
                else:
                    self.window.remove(maybe_bricks_bonus_bottom_right)
                    self.__brick_number -= 1
                    self.__score += 100
                    if self.bonus_ball.x < maybe_bricks_bonus_bottom_right.x + 5:
                        self.__vx_b *= -1
                    elif self.bonus_ball.x > maybe_bricks_bonus_bottom_right.x + 5:
                        self.__vy_b *= -1

            elif maybe_bricks_bonus_bottom_left is not None and self.__vx_b < 0 < self.__vy_b and \
                    maybe_bricks_bonus_bottom_left.height == self._brick_height:
                if maybe_bricks_bonus_bottom_left is self.__bonus1 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus2 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus3 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus4 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus5 or \
                        maybe_bricks_bonus_bottom_left is self.__bonus6:
                    self.__drop_bonus = True
                    self.window.remove(maybe_bricks_bonus_bottom_left)
                    self.__brick_number -= 1
                    self.__score += 200
                    if self.bonus_ball.x < maybe_bricks_bonus_bottom_left.x+maybe_bricks_bonus_bottom_left.width - 5:
                        self.__vy_b *= -1
                    elif self.bonus_ball.x > maybe_bricks_bonus_bottom_left.x+maybe_bricks_bonus_bottom_left.width - 5:
                        self.__vx_b *= -1
                else:
                    self.window.remove(maybe_bricks_bonus_bottom_left)
                    self.__brick_number -= 1
                    self.__score += 100
                    if self.bonus_ball.x < maybe_bricks_bonus_bottom_left.x+maybe_bricks_bonus_bottom_left.width-5:
                        self.__vy_b *= -1
                    elif self.bonus_ball.x > maybe_bricks_bonus_bottom_left.x+maybe_bricks_bonus_bottom_left.width-5:
                        self.__vx_b *= -1

            self.__score_recorder.text = f'Score: {str(self.__score)}'

    def drop_bonus(self):
        """
        Drop the bonus cube when ball hit bonus brick.
        Bonus condition is randomly and alternatively appear.
        """
        if self.__drop_bonus:
            self.__drop_bonus = False
            self.__catch_bonus = True

            if self.__bonus_ball_exist:  # Make sure only one extra ball exists
                if not self.__bonus1_dropped:
                    self.__bonus_condition = 1
                else:
                    self.__bonus_condition = 2

            elif not self.__bonus_ball_exist and not self.__bonus1_dropped and not self.__bonus2_dropped:
                self.__bonus_condition = random.randint(1, 3)

            else:
                if self.__bonus1_dropped:
                    self.__bonus_condition = random.randint(2, 3)
                    self.__bonus1_dropped = False
                elif self.__bonus2_dropped:
                    self.__bonus_condition = random.randrange(1, 4, 2)
                    self.__bonus2_dropped = False

            if self.__bonus_condition == 1:
                self.__bonus1_dropped, self.__bonus2_dropped, self.__bonus3_dropped = True, False, False
                self.window.add(self.__bonus1_cube, self.ball.x, self.ball.y)

            elif self.__bonus_condition == 2:
                self.__bonus1_dropped, self.__bonus2_dropped, self.__bonus3_dropped = False, True, False
                self.window.add(self.__bonus2_cube, self.ball.x, self.ball.y)

            elif self.__bonus_condition == 3:
                self.__bonus_ball_exist = True
                self.__bonus1_dropped, self.__bonus2_dropped, self.__bonus3_dropped = False, False, True
                self.window.add(self.__bonus3_cube, self.ball.x, self.ball.y)

    def catch_bonus(self):
        """
        Catch the bonus cube when it hits paddle.
        """
        bonus1_detector1 = self.window.get_object_at(self.__bonus1_cube.x, self.__bonus1_cube.y + 16)
        bonus1_detector2 = self.window.get_object_at(self.__bonus1_cube.x + self.__bonus1_cube.width / 2,
                                                     self.__bonus1_cube.y + 16)
        bonus1_detector3 = self.window.get_object_at(self.__bonus1_cube.x + self.__bonus1_cube.width,
                                                     self.__bonus1_cube.y + 16)

        bonus2_detector1 = self.window.get_object_at(self.__bonus2_cube.x, self.__bonus2_cube.y + 16)
        bonus2_detector2 = self.window.get_object_at(self.__bonus2_cube.x + self.__bonus2_cube.width / 2,
                                                     self.__bonus2_cube.y + 16)
        bonus2_detector3 = self.window.get_object_at(self.__bonus2_cube.x + self.__bonus2_cube.width,
                                                     self.__bonus2_cube.y + 16)

        bonus3_detector1 = self.window.get_object_at(self.__bonus3_cube.x, self.__bonus3_cube.y + 16)
        bonus3_detector2 = self.window.get_object_at(self.__bonus3_cube.x + self.__bonus3_cube.width / 2,
                                                     self.__bonus3_cube.y + 16)
        bonus3_detector3 = self.window.get_object_at(self.__bonus3_cube.x + self.__bonus3_cube.width,
                                                     self.__bonus3_cube.y + 16)
        if self.__catch_bonus:
            if self.__bonus1_cube.y + self.__bonus1_cube.height > self.paddle.y - 10 and self.__bonus1_cube.y > 400:
                if bonus1_detector1 is not None and bonus1_detector1.height == self._paddle_height:
                    self.window.remove(self.__bonus1_cube)
                    self.__trigger_bonus1 = True
                elif bonus1_detector2 is not None and bonus1_detector2.height == self._paddle_height:
                    self.window.remove(self.__bonus1_cube)
                    self.__trigger_bonus1 = True
                elif bonus1_detector3 is not None and bonus1_detector3.height == self._paddle_height:
                    self.window.remove(self.__bonus1_cube)
                    self.__trigger_bonus1 = True
            elif self.__bonus1_cube.y > self.window.height:
                self.window.remove(self.__bonus1_cube)

            if self.__bonus2_cube.y + self.__bonus2_cube.height > self.paddle.y - 10 and self.__bonus2_cube.y > 400:
                if bonus2_detector1 is not None and bonus2_detector1.height == self._paddle_height:
                    self.window.remove(self.__bonus2_cube)
                    self.__trigger_bonus2 = True
                elif bonus2_detector2 is not None and bonus2_detector2.height == self._paddle_height:
                    self.window.remove(self.__bonus2_cube)
                    self.__trigger_bonus2 = True
                elif bonus2_detector3 is not None and bonus2_detector3.height == self._paddle_height:
                    self.window.remove(self.__bonus2_cube)
                    self.__trigger_bonus2 = True
            elif self.__bonus2_cube.y > self.window.height:
                self.window.remove(self.__bonus2_cube)

            if self.__bonus3_cube.y + self.__bonus3_cube.height > self.paddle.y - 10 and self.__bonus3_cube.y > 400:
                if bonus3_detector1 is not None and bonus3_detector1.height == self._paddle_height:
                    self.window.remove(self.__bonus3_cube)
                    self.__trigger_bonus3 = True
                elif bonus3_detector2 is not None and bonus3_detector2.height == self._paddle_height:
                    self.window.remove(self.__bonus3_cube)
                    self.__trigger_bonus3 = True
                elif bonus3_detector3 is not None and bonus3_detector3.height == self._paddle_height:
                    self.window.remove(self.__bonus3_cube)
                    self.__trigger_bonus3 = True
            elif self.__bonus3_cube.y > self.window.height:
                self.window.remove(self.__bonus3_cube)
                self.__bonus_ball_exist = False

    def trigger_bonus(self):
        """
        Trigger bonus corresponding to condition number.
        """
        if self.__trigger_bonus1:
            self.__catch_bonus = False
            self.__trigger_bonus1 = False
            self.__bonus_time_counter = True
            self.window.remove(self.paddle)
            self._paddle_width += 100
            self.paddle = GRect(self._paddle_width, self._paddle_height)
            self.paddle.filled = True
            self.paddle.fill_color = 'black'
            self.window.add(self.paddle, (self.window.width - self.paddle.width) / 2,
                            self.window.height - self._paddle_offset)

        elif self.__trigger_bonus2:
            self.__catch_bonus = False
            self.__trigger_bonus2 = False
            self.__game_lives += 1
            if self.__game_lives == 2:
                self.window.add(self.__lives2, self.window.width - self.__game_lives * 25, 8)
            elif self.__game_lives == 3:
                self.window.add(self.__lives3, self.window.width - self.__game_lives * 25, 8)
            elif self.__game_lives == 4:
                self.window.add(self.__lives4, self.window.width - self.__game_lives * 25, 8)
            elif self.__game_lives == 5:
                self.window.add(self.__lives5, self.window.width - self.__game_lives * 25, 8)
            elif self.__game_lives == 6:
                self.window.add(self.__lives6, self.window.width - self.__game_lives * 25, 8)
            elif self.__game_lives == 7:
                self.window.add(self.__lives7, self.window.width - self.__game_lives * 25, 8)
            elif self.__game_lives == 8:
                self.window.add(self.__lives8, self.window.width - self.__game_lives * 25, 8)
            elif self.__game_lives == 9:
                self.window.add(self.__lives9, self.window.width - self.__game_lives * 25, 8)

        elif self.__trigger_bonus3:
            self.__catch_bonus = False
            self.__trigger_bonus3 = False
            self.window.add(self.bonus_ball, self.paddle.x + (self.paddle.width - self.ball.width) / 2,
                            self.paddle.y - self.bonus_ball.height)
            self.__vx_b = random.randint(self.__total_v - 7, self.__total_v - 5)
            if random.random() > 0.5:
                self.__vx *= -1
            self.__vy_b = -int((self.__total_v ** 2 - self.__vx ** 2) ** 0.5)

    # ------------------------ Attributes ------------------------
    def move_x_left_exceed(self):
        if self.__vx < 0 and 0 > self.ball.x + self.__vx:
            self.__vx *= -1
            return True

        if self.__vx_b < 0 and 0 > self.bonus_ball.x + self.__vx_b:
            self.__vx_b *= -1
            return True

    def move_x_right_exceed(self):
        if self.__vx > 0 and self.ball.x + self.ball.width + self.__vx > self.window.width:
            self.__vx *= -1
            return True

        if self.__vx_b > 0 and self.bonus_ball.x + self.bonus_ball.width + self.__vx_b > self.window.width:
            self.__vx_b *= -1
            return True

    def move_y_up_exceed(self):
        if self.__vy < 0 and self.ball.y + self.__vy < 0:
            self.__vy *= -1
            return True

        if self.__vy_b < 0 and self.bonus_ball.y + self.__vy_b < 0:
            self.__vy_b *= -1
            return True

    def ball_hit_paddle(self):
        if self.ball.y + self.ball.height + self.__vy > self.paddle.y:
            if self.window.get_object_at(self.ball.x + self.ball.width * 0.1,
                                         self.ball.y + self.ball.height + 1) is not None \
                    or self.window.get_object_at(self.ball.x + self.ball.width * 0.2,
                                                 self.ball.y + self.ball.height + 1) is not None or \
                    self.window.get_object_at(self.ball.x + self.ball.width * 0.3,
                                              self.ball.y + self.ball.height + 1) is not None or \
                    self.window.get_object_at(self.ball.x + self.ball.width * 0.4,
                                              self.ball.y + self.ball.height + 1) is not None or \
                    self.window.get_object_at(self.ball.x + self.ball.width * 0.5,
                                              self.ball.y + self.ball.height + 1) is not None or \
                    self.window.get_object_at(self.ball.x + self.ball.width * 0.6,
                                              self.ball.y + self.ball.height + 1) is not None or \
                    self.window.get_object_at(self.ball.x + self.ball.width * 0.7,
                                              self.ball.y + self.ball.height + 1) is not None or \
                    self.window.get_object_at(self.ball.x + self.ball.width * 0.8,
                                              self.ball.y + self.ball.height + 1) is not None or \
                    self.window.get_object_at(self.ball.x + self.ball.width * 0.9,
                                              self.ball.y + self.ball.height + 1) is not None or \
                    self.window.get_object_at(self.ball.x + self.ball.width,
                                              self.ball.y + self.ball.height + 1) is not None:
                if self.get_bonus_time_counter() and self.__bonus_condition == 1 or self.get_bonus_time_counter() \
                        and self.__bonus_condition == 3:
                    self.__bonus_time_remain -= 1
                return True

    def bonus_ball_hit_paddle(self):
        if self.bonus_ball.y + self.bonus_ball.height + self.__vy_b > self.paddle.y:
            if self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.1,
                                         self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.2,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.3,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.4,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.5,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.6,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.7,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.8,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.9,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None or \
                    self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width,
                                              self.bonus_ball.y + self.bonus_ball.height + 1) is not None:

                if self.bonus_ball.y + self.bonus_ball.height <= self.paddle.y:
                    if self.paddle.x + self.paddle.width * 0.5 > self.bonus_ball.x + self.bonus_ball.width / 2 > \
                            self.paddle.x + self.paddle.width * 0.25:
                        self.__vx_b = -random.randint(self.__total_v - 7, self.__total_v - 5)
                    elif self.paddle.x + self.paddle.width * 0.25 > self.bonus_ball.x + self.bonus_ball.width / 2 > \
                            self.paddle.x:
                        self.__vx_b = -random.randint(self.__total_v - 4, self.__total_v - 2)
                    elif self.paddle.x + self.paddle.width * 0.75 > self.bonus_ball.x + self.bonus_ball.width / 2 > \
                            self.paddle.x + self.paddle.width * 0.5:
                        self.__vx_b = random.randint(self.__total_v - 7, self.__total_v - 5)
                    else:
                        self.__vx_b = random.randint(self.__total_v - 4, self.__total_v - 2)
                    self.__vy_b = -int((self.__total_v ** 2 - self.__vx_b ** 2) ** 0.5)

                elif self.bonus_ball.y + self.bonus_ball.height > self.paddle.y:
                    self.__vx_b *= -1

                return True

    def ball_hit_bricks(self):
        # Cut the ball into smaller pixel to prevent the ball get through brick spacing.
        maybe_bricks_top1 = self.window.get_object_at(self.ball.x + self.ball.width * 0.25, self.ball.y)
        maybe_bricks_top2 = self.window.get_object_at(self.ball.x + self.ball.width * 0.5, self.ball.y)
        maybe_bricks_top3 = self.window.get_object_at(self.ball.x + self.ball.width * 0.75, self.ball.y)
        maybe_bricks_top4 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)

        maybe_bricks_right1 = self.window.get_object_at(self.ball.x + self.ball.width,
                                                        self.ball.y + self.ball.height * 0.25)
        maybe_bricks_right2 = self.window.get_object_at(self.ball.x + self.ball.width,
                                                        self.ball.y + self.ball.height * 0.5)
        maybe_bricks_right3 = self.window.get_object_at(self.ball.x + self.ball.width,
                                                        self.ball.y + self.ball.height * 0.75)
        maybe_bricks_right4 = self.window.get_object_at(self.ball.x + self.ball.width,
                                                        self.ball.y + self.ball.height)

        maybe_bricks_bottom1 = self.window.get_object_at(self.ball.x + self.ball.width * 0.75,
                                                         self.ball.y + self.ball.height)
        maybe_bricks_bottom2 = self.window.get_object_at(self.ball.x + self.ball.width * 0.5,
                                                         self.ball.y + self.ball.height)
        maybe_bricks_bottom3 = self.window.get_object_at(self.ball.x + self.ball.width * 0.25,
                                                         self.ball.y + self.ball.height)
        maybe_bricks_bottom4 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)

        maybe_bricks_left1 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height * 0.75)
        maybe_bricks_left2 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height * 0.5)
        maybe_bricks_left3 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height * 0.25)
        maybe_bricks_left4 = self.window.get_object_at(self.ball.x, self.ball.y)

        maybe_bricks_bonus_top1 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.25,
                                                            self.bonus_ball.y)
        maybe_bricks_bonus_top2 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.5,
                                                            self.bonus_ball.y)
        maybe_bricks_bonus_top3 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.75,
                                                            self.bonus_ball.y)
        maybe_bricks_bonus_top4 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width,
                                                            self.bonus_ball.y)

        maybe_bricks_bonus_right1 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width,
                                                              self.bonus_ball.y + self.bonus_ball.height * 0.25)
        maybe_bricks_bonus_right2 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width,
                                                              self.bonus_ball.y + self.bonus_ball.height * 0.5)
        maybe_bricks_bonus_right3 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width,
                                                              self.bonus_ball.y + self.bonus_ball.height * 0.75)
        maybe_bricks_bonus_right4 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width,
                                                              self.bonus_ball.y + self.bonus_ball.height)

        maybe_bricks_bonus_bottom1 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.75,
                                                               self.bonus_ball.y + self.bonus_ball.height)
        maybe_bricks_bonus_bottom2 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.5,
                                                               self.bonus_ball.y + self.bonus_ball.height)
        maybe_bricks_bonus_bottom3 = self.window.get_object_at(self.bonus_ball.x + self.bonus_ball.width * 0.25,
                                                               self.bonus_ball.y + self.bonus_ball.height)
        maybe_bricks_bonus_bottom4 = self.window.get_object_at(self.bonus_ball.x,
                                                               self.bonus_ball.y + self.bonus_ball.height)

        maybe_bricks_bonus_left1 = self.window.get_object_at(self.bonus_ball.x,
                                                             self.bonus_ball.y + self.bonus_ball.height * 0.75)
        maybe_bricks_bonus_left2 = self.window.get_object_at(self.bonus_ball.x,
                                                             self.bonus_ball.y + self.bonus_ball.height * 0.5)
        maybe_bricks_bonus_left3 = self.window.get_object_at(self.bonus_ball.x,
                                                             self.bonus_ball.y + self.bonus_ball.height * 0.25)
        maybe_bricks_bonus_left4 = self.window.get_object_at(self.bonus_ball.x, self.bonus_ball.y)

        if maybe_bricks_top1 is not None and maybe_bricks_top1.height == self._brick_height or \
                maybe_bricks_top2 is not None and maybe_bricks_top2.height == self._brick_height or \
                maybe_bricks_top3 is not None and maybe_bricks_top3.height == self._brick_height or \
                maybe_bricks_top4 is not None and maybe_bricks_top4.height == self._brick_height or \
                maybe_bricks_right1 is not None and maybe_bricks_right1.height == self._brick_height or \
                maybe_bricks_right2 is not None and maybe_bricks_right2.height == self._brick_height or \
                maybe_bricks_right3 is not None and maybe_bricks_right3.height == self._brick_height or \
                maybe_bricks_right4 is not None and maybe_bricks_right4.height == self._brick_height or \
                maybe_bricks_bottom1 is not None and maybe_bricks_bottom1.height == self._brick_height or \
                maybe_bricks_bottom2 is not None and maybe_bricks_bottom2.height == self._brick_height or \
                maybe_bricks_bottom3 is not None and maybe_bricks_bottom3.height == self._brick_height or \
                maybe_bricks_bottom4 is not None and maybe_bricks_bottom4.height == self._brick_height or \
                maybe_bricks_left1 is not None and maybe_bricks_left1.height == self._brick_height or \
                maybe_bricks_left2 is not None and maybe_bricks_left2.height == self._brick_height or \
                maybe_bricks_left3 is not None and maybe_bricks_left3.height == self._brick_height or \
                maybe_bricks_left4 is not None and maybe_bricks_left4.height == self._brick_height:
            return True

        if maybe_bricks_bonus_top1 is not None and maybe_bricks_bonus_top1.height == self._brick_height or \
                maybe_bricks_bonus_top2 is not None and maybe_bricks_bonus_top2.height == self._brick_height or \
                maybe_bricks_bonus_top3 is not None and maybe_bricks_bonus_top3.height == self._brick_height or \
                maybe_bricks_bonus_top4 is not None and maybe_bricks_bonus_top4.height == self._brick_height or \
                maybe_bricks_bonus_right1 is not None and maybe_bricks_bonus_right1.height == self._brick_height or \
                maybe_bricks_bonus_right2 is not None and maybe_bricks_bonus_right2.height == self._brick_height or \
                maybe_bricks_bonus_right3 is not None and maybe_bricks_bonus_right3.height == self._brick_height or \
                maybe_bricks_bonus_right4 is not None and maybe_bricks_bonus_right4.height == self._brick_height or \
                maybe_bricks_bonus_bottom1 is not None and maybe_bricks_bonus_bottom1.height == self._brick_height or \
                maybe_bricks_bonus_bottom2 is not None and maybe_bricks_bonus_bottom2.height == self._brick_height or \
                maybe_bricks_bonus_bottom3 is not None and maybe_bricks_bonus_bottom3.height == self._brick_height or \
                maybe_bricks_bonus_bottom4 is not None and maybe_bricks_bonus_bottom4.height == self._brick_height or \
                maybe_bricks_bonus_left1 is not None and maybe_bricks_bonus_left1.height == self._brick_height or \
                maybe_bricks_bonus_left2 is not None and maybe_bricks_bonus_left2.height == self._brick_height or \
                maybe_bricks_bonus_left3 is not None and maybe_bricks_bonus_left3.height == self._brick_height or \
                maybe_bricks_bonus_left4 is not None and maybe_bricks_bonus_left4.height == self._brick_height:
            return True
