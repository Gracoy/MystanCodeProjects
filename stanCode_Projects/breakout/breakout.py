"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10        # 100 frames per second


vx = 0
vy = 0


def main():
    global vx, vy
    game = BreakoutGraphics()

    while True:
        # ------------ Set game menu ------------
        if game.get_if_game_menu() and not game.get_if_game_start():
            game.set_game_menu()  # Click to close menu
        # ------------ Set all objects for the game ------------
        if not game.get_if_game_menu() and not game.get_if_game_start():
            game.set_game()  # Click to start game
        # ------------ Start the game ------------
            while True:
                vx, vy = game.get_vx(), game.get_vy()
                vx_b, vy_b = game.get_vx_b(), game.get_vy_b()
        # ------------ Game over and set score board ------------
                if game.get_game_lives_remain() == 0 or game.get_brick_remain() == 0:
                    game.set_game_result()  # Click to back to game menu
                    break
        # ------------ When ball hits boundary ------------
                if game.move_x_left_exceed():
                    vx, vx_b = game.get_vx(), game.get_vx_b()
                elif game.move_x_right_exceed():
                    vx, vx_b = game.get_vx(), game.get_vx_b()
                elif game.move_y_up_exceed():
                    vy, vy_b = game.get_vy(), game.get_vy_b()
                elif game.ball_hit_paddle():
                    game.reset_velocity()  # Reset velocity according to the position on paddle that the ball hit
                    vx, vy = game.get_vx(), game.get_vy()
                if game.bonus_ball_hit_paddle():
                    vx_b, vy_b = game.get_vx_b(), game.get_vy_b()
                if game.ball_hit_bricks():
                    game.break_bricks_and_bound()
        # ------------ Moving objects during the game ------------
                if game.get_if_ball_exist():
                    game.ball.move(vx, vy)
                    game.bonus_ball.move(vx_b, vy_b)
        # ------------ Bonus conditions ------------
                game.drop_bonus()  # Drop bonus cube
                game.get_bonus1_cube().move(0, 5)  # Longer paddle and reset after ball hits paddle for 5 times
                game.get_bonus2_cube().move(0, 5)  # One more life
                game.get_bonus3_cube().move(0, 5)  # Extra ball
                game.catch_bonus()
                game.trigger_bonus()  # If catch bonus cube, trigger bonus
        # ------------ Reset the game in the conditions below ------------
                if game.get_bonus_time_remain() == 0:
                    game.set_reset_bonus()  # Reset paddle length

                if game.ball.y > game.window.height + 10:
                    game.set_restart_game()
                    game.set_remove_bonus_ball()

                if game.bonus_ball.y > game.window.height + 10:
                    game.set_remove_bonus_ball()

                pause(FRAME_RATE)
        # ------------ Reset the game in the conditions below ------------
        if game.get_if_score_history():
            game.set_score_history()  # Every life remain will get 500 score


if __name__ == '__main__':
    main()
