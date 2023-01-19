"""
File: boggle.py
Name: 姜佳成
----------------------------------------
This program computes Boggle game.
"""

import time
import tkinter as tk

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'

# Constants
WINDOW_WIDTH = 750      # Optimized window size
WINDOW_HEIGHT = 636
SHORTEST_LENGTH = 4     # Shortest word length to find
BOARD_OFFSET = 12       # Start point of checkerboard on canvas
BOARD_LENGTH = 420      # Length of checkerboard


class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False


class Boggle:
    def __init__(self):
        # ------------ DS to store all words ------------
        self.dict_root = TrieNode()
        self.load_dictionary(FILE)

        # ------------ Variables ------------
        self.__board_dimension = 4
        self.__row_number = 0
        self.__letter_array = []

        # ------------ Make GUI ------------
        self.__top = tk.Tk()
        self.__top.wm_title('Boggle')
        self.__top.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        self.__space_top = tk.LabelFrame(self.__top, height=5)
        self.__space_top.grid(row=0, sticky=tk.W)

        self.__space_left = tk.LabelFrame(self.__top, width=5)
        self.__space_left.grid(column=0, sticky=tk.W)

        self.__input_label = tk.Label(self.__top, text='Row of letters : ')
        self.__input_label.grid(row=1, column=1, columnspan=3, sticky=tk.SW)

        self.__input_entry = tk.Entry(self.__top, width=18, name='entry', borderwidth=2)
        self.__input_entry.grid(row=1, column=4, columnspan=20, sticky=tk.SW)
        self.__input_entry.focus()

        self.__set_dimension_label = tk.Label(self.__top, text='Dimension : ')
        self.__set_dimension_label.grid(row=1, column=10, columnspan=6)

        self.__set_entry = tk.Entry(self.__top, width=16, name='set_dimension', borderwidth=2)
        self.__set_entry.grid(row=1, column=14, columnspan=8)

        self.__space_entry_and_display = tk.LabelFrame(self.__top, height=5)
        self.__space_entry_and_display.grid(row=2, sticky=tk.W)

        self.__font = 'Times New Roman', 12, 'bold'

        self.__display_area = tk.Text(self.__top, width=54, height=8, borderwidth=2)
        self.__display_area.config(font=self.__font)
        self.__display_area.grid(row=3, column=1, columnspan=20, sticky=tk.W)

        self.__board_canvas = tk.Canvas(self.__top, width=450, height=450)
        self.__board_canvas.grid(row=4, column=1, columnspan=20, sticky=tk.W)

        self.__result = tk.Text(self.__top, width=35, height=32, borderwidth=2)
        self.__result.config(font=self.__font)
        self.__result.grid(row=1, column=22, rowspan=200, sticky=tk.W)

        # ------------ Call functions ------------
        self.draw_board()                                                              # Default size is 4x4
        self.__input_entry.bind('<Return>', lambda event: self.give_letter_array())    # Obtain array of letters
        self.__set_entry.bind('<Return>', lambda event: self.set_board_dimension())    # Set dimension of letter board

        tk.mainloop()

    def load_dictionary(self, file):
        """
        This function stores all words in the file into TrieNode data structure: self.dict_root.
        :param file: (file path) Dictionary file.
        :return: (TrieNode) Tree-like TrieNode data structure of all words in file.
        """
        with open(file, 'r') as f:
            for line in f:
                cur = self.dict_root
                new_line = line.strip()
                for ch in new_line:
                    if ch in cur.children:
                        cur = cur.children[ch]
                    else:
                        cur.children[ch] = TrieNode()
                        cur = cur.children[ch]
                cur.end = True

    def draw_board(self):
        """
        This function draws blank checkerboard corresponding to letter board dimension.
        """
        self.__board_canvas.delete('all')
        for i in range(self.__board_dimension + 1):
            space = round(i * (BOARD_LENGTH / self.__board_dimension))
            self.__board_canvas.create_line(BOARD_OFFSET + space, BOARD_OFFSET,
                                            BOARD_OFFSET + space, BOARD_OFFSET + BOARD_LENGTH, width=2)
            self.__board_canvas.create_line(BOARD_OFFSET, BOARD_OFFSET + space,
                                            BOARD_OFFSET + BOARD_LENGTH, BOARD_OFFSET + space, width=2)

    def set_board_dimension(self):
        """
        This function resets the dimension of letter board and draws a new blank checkerboard.
        """
        self.__row_number = 0
        self.__letter_array = []
        self.__board_dimension = int(self.__set_entry.get().strip())
        self.draw_board()

    def give_letter_array(self):
        """
        This function collects input letters into a list for the following find_word function.
        """
        self.__display_area.see('end')
        # ------------ Clear display area when last game is finished or dimension is reset ------------
        if self.__row_number == 0:
            self.__display_area.delete('1.0', tk.END)
            self.draw_board()
        # ------------ Convert user input into proper data format ------------
        row_i = self.__input_entry.get().lower().split(' ')      # Input: _a_b__c_d___, ap__p_l_e_ (_ = space)
        row_i = [ch for ch in row_i if ch and len(ch) == 1]      # Obtained: ['a', 'b', 'c', 'd', ...], ['p', 'l', 'e']
        symbol = ' '
        if len(row_i) != self.__board_dimension:
            example = list('arbkgkslqw')
            self.__display_area.insert('end', f'Illegal input ! Ex: {symbol.join(example[:self.__board_dimension])}\n')
        else:
            self.__letter_array.append(row_i)
            self.__row_number += 1
            self.__display_area.insert('end', f'{self.__row_number} row of letters : {symbol.join(row_i)}\n')
            space = round(BOARD_LENGTH / self.__board_dimension)
            y_position = BOARD_OFFSET + round(space / 2) + round((self.__row_number-1) * space)
            text_size = 72 - (self.__board_dimension * 6)        # (Dimension:Text size) = (3:54), (4:48), (5:42), ...
            for i in range(len(row_i)):                          # Insert input letter into checkerboard
                x_position = BOARD_OFFSET + round(space / 2) + round(i * space)
                self.__board_canvas.create_text(x_position, y_position, text=row_i[i],
                                                font=('Times New Roman', text_size, 'bold'))
        self.__input_entry.delete(0, 'end')                      # Clear entry area after every input
        # ------------ If the number of input row reached the setting dimension, start the game ------------
        if self.__row_number == self.__board_dimension:
            self.find_words()

    def find_words(self):
        """
        This function follows rule of boggle game to find every words with length >= SHORTEST_LENGTH.
        """
        self.__result.delete('1.0', tk.END)
        ans = []
        start = time.time()
        for i in range(len(self.__letter_array)):
            for j in range(len(self.__letter_array[0])):
                cur_root = self.dict_root
                self.find_words_helper(cur_root, i, j, '', ans)
        end = time.time()
        # ------------ Reset variables after finished ------------
        self.__row_number = 0
        self.__letter_array = []
        # ------------ Display result ------------
        self.__result.insert('end', f'\nThere are {len(ans)} words in total.\n')
        self.__result.insert('end', f'\nThe speed of your boggle algorithm:\n {end - start} seconds.')
        self.__result.see('end')

    def find_words_helper(self, cur_root, current_i, current_j, current_str, ans):
        """
        :param cur_root: (TrieNode) Node of last ch in current_str.
        :param current_i: (int) Current i_index to link next str.
        :param current_j: (int) Current j_index to link next str.
        :param current_str: (str) Prefix of the possible word.
        :param ans: (list) List of all word found.
        """
        # ------------ Success condition ------------
        if len(current_str) >= SHORTEST_LENGTH and cur_root.end:
            if current_str not in ans:
                self.__result.insert('end', f'Found: {current_str}\n')
                ans.append(current_str)
        # ------------ Un_choose condition_1 : Index out of range ------------
        if current_i >= len(self.__letter_array) or current_i < 0 or \
                current_j >= len(self.__letter_array[0]) or current_j < 0:
            return
        node_str = self.__letter_array[current_i][current_j]
        # ------------ Un_choose condition_2 : Letter has been used or wrong prefix ------------
        if node_str not in cur_root.children:
            return
        # ------------ Choose ------------
        cur_root = cur_root.children[node_str]                # Go to next node
        self.__letter_array[current_i][current_j] = '*'       # Used letter turn into '*'
        # ------------ Explore ------------
        self.find_words_helper(cur_root, current_i - 1, current_j - 1, current_str + node_str, ans)
        self.find_words_helper(cur_root, current_i - 1, current_j + 0, current_str + node_str, ans)
        self.find_words_helper(cur_root, current_i - 1, current_j + 1, current_str + node_str, ans)
        self.find_words_helper(cur_root, current_i + 0, current_j - 1, current_str + node_str, ans)
        self.find_words_helper(cur_root, current_i + 0, current_j + 1, current_str + node_str, ans)
        self.find_words_helper(cur_root, current_i + 1, current_j - 1, current_str + node_str, ans)
        self.find_words_helper(cur_root, current_i + 1, current_j + 0, current_str + node_str, ans)
        self.find_words_helper(cur_root, current_i + 1, current_j + 1, current_str + node_str, ans)
        self.__letter_array[current_i][current_j] = node_str  # Recover used letter after checking every path


Boggle()
