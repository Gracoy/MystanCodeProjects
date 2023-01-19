"""
File: babygraphics.py
Name: 姜佳成
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    return GRAPH_MARGIN_SIZE + round(((width-2*GRAPH_MARGIN_SIZE)/len(YEARS))*year_index, 0)


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
                       CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)

    for idx, year in enumerate(YEARS):
        x = get_x_coordinate(CANVAS_WIDTH, idx)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)
        canvas.create_text(x+TEXT_DX, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, text=year, anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #
    for name_idx, name in enumerate(lookup_names):
        color = COLORS[name_idx % len(COLORS)]
        for idx, year in enumerate(YEARS):
            if idx > 0:
                # The y position of text and line are normalized by (Grid height / MAX RANK)
                # --------------- Start point of line ---------------
                x1 = get_x_coordinate(CANVAS_WIDTH, idx-1)
                if str(YEARS[idx-1]) in name_data[name]:
                    rank1 = name_data[name][str(YEARS[idx-1])]
                    y1 = int(rank1) * ((CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)/MAX_RANK) + GRAPH_MARGIN_SIZE
                else:
                    rank1 = '*'
                    y1 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                # --------------- End point of line ---------------
                x2 = get_x_coordinate(CANVAS_WIDTH, idx)
                if str(year) in name_data[name]:
                    rank2 = name_data[name][str(year)]
                    y2 = int(rank2) * ((CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)/MAX_RANK) + GRAPH_MARGIN_SIZE
                else:
                    rank2 = '*'
                    y2 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                # --------------- Draw lines and put texts on canvas ---------------
                canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=color)
                if idx-1 == 0:  # Consider 1st point of line as special case to prevent text double created
                    canvas.create_text(x1+TEXT_DX, y1, text=f'{name} {rank1}', anchor=tkinter.SW, fill=color)
                canvas.create_text(x2+TEXT_DX, y2, text=f'{name} {rank2}', anchor=tkinter.SW, fill=color)


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
