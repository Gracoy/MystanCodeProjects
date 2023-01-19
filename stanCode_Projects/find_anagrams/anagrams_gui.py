import tkinter as tk
import time


class FindAnagrams:
    def __init__(self, width, height, all_dict):
        self.width = width
        self.height = height
        self.__all_dict = all_dict  # Data type: dict, given by user

        # ------------ Create window ------------
        self.__top = tk.Tk()
        self.__top.wm_title('Find anagrams')
        self.__top.geometry(f'{width}x{height}')

        # Display font
        self.__font = ('Times New Roman', 12, 'bold')

        # ------------ Arrange the format of each area ------------
        self.__space_top = tk.LabelFrame(self.__top, height=5)
        self.__space_top.grid(row=0)

        self.__space_left = tk.LabelFrame(self.__top, width=5)
        self.__space_left.grid(column=0, sticky='w')

        # Label of anagrams entry
        self.__label = tk.Label(self.__top, text="Find anagrams for : ")
        self.__label.grid(row=1, column=1, sticky=tk.SW)

        # Anagrams entry area
        self.__entry = tk.Entry(self.__top, width=40, name='entry', borderwidth=2)
        self.__entry.grid(row=1, column=2, sticky=tk.W)
        self.__entry.focus()

        self.__space_entry_and_result = tk.LabelFrame(self.__top, height=5)
        self.__space_entry_and_result.grid(row=2, sticky=tk.W)

        # Result area of anagrams
        self.__result_area = tk.Text(self.__top, width=70, height=24, name='result', borderwidth=2)
        self.__result_area.config(font=self.__font)
        self.__result_area.grid(row=3, column=1, columnspan=20, sticky=tk.W)
        self.__result_area.insert('insert', 'Welcome to stanCode \"Anagram Generator\" (or -1 to quit)\n\n')

        self.__space_result_and_search = tk.LabelFrame(self.__top, height=5)
        self.__space_result_and_search.grid(row=4, sticky=tk.W)

        # Label of prefix search
        self.__search_label = tk.Label(self.__top, text='Words with prefix : ')
        self.__search_label.grid(row=5, column=1, sticky=tk.NW)

        # Prefix search entry area
        self.__search = tk.Entry(self.__top, width=10, name='search', borderwidth=2)
        self.__search.grid(row=5, column=2, sticky=tk.NW)

        self.__space_search_and_search_result = tk.LabelFrame(self.__top, height=5)
        self.__space_search_and_search_result.grid(row=6, sticky=tk.W)

        # Prefix search result area
        self.__search_result = tk.Text(self.__top, width=70, height=5, name='prefix_result', borderwidth=2)
        self.__search_result.config(font=self.__font)
        self.__search_result.grid(row=7, column=1, columnspan=20, sticky=tk.W)

        # ------------ Functions ------------
        # When <return> key is hit in a text field, connect to the function find_anagrams()
        self.__entry.bind("<Return>", lambda event: self.find_anagrams())

        # When <return> key is hit in a text field, connect to the function find_anagrams()
        self.__search.bind("<Return>", lambda event: self.search_words())
        tk.mainloop()

    def find_anagrams(self):
        """
        This function calls helper function and prints anagrams result on window.
        """
        input_word = self.__entry.get().strip().lower()  # Data type of self.__entry is dict
        if input_word == '-1':
            self.__top.quit()
        else:
            self.__result_area.delete('1.0', tk.END)  # Clear result area
            self.__result_area.insert('end', f'Find anagrams for: {input_word}\n')
            self.__result_area.insert('end', 'Searching...\n')
            start = time.time()
            result = self.find_anagrams_helper(input_word, [], '', [])
            end = time.time()
            symbol = ', '
            self.__result_area.insert('end', f'{len(result)} anagrams: {symbol.join(result)}\n')
            self.__result_area.insert('end', '-'*60)
            self.__result_area.insert('end', f'\nThe speed of your anagram algorithm: {end-start} seconds.\n')
            self.__result_area.insert('end', f'Try another anagram or -1 to quit.\n\n')
            self.__result_area.see('end')  # Scroll to last line

    def find_anagrams_helper(self, input_word, idx_list, current_str, current_result):
        """
        This function prints all the anagrams found and returns result list of anagrams.
        :param input_word: (str) The word to find anagrams
        :param idx_list: (list) The index list of string under current cycle
        :param current_str: (str) The string under current cycle
        :param current_result: (list) All anagrams found under current cycle
        :return: (list) List of all the anagrams found in dictionary. ['anagram1', 'anagram2', ...]
        """
        if len(current_str) == len(input_word):
            if current_str not in current_result and current_str in self.__all_dict[current_str]:
                current_result.append(current_str)
                self.__result_area.insert('end', f'Found: {current_str}\n')
                self.__result_area.insert('end', 'Searching...\n')
        else:
            for idx, ch in enumerate(input_word):
                if idx in idx_list:
                    pass
                else:
                    idx_list.append(idx)
                    current_str += ch
                    if self.has_prefix(current_str):
                        self.find_anagrams_helper(input_word, idx_list, current_str, current_result)
                    idx_list.pop()
                    current_str = current_str[:-1]
        return current_result

    def has_prefix(self, sub_s):
        """
        This function checks if current sub-string generated by find_anagrams_helper function
        meets any word prefix in the dictionary.
        :param sub_s: Current sub-string generated by find_anagrams_helper function
        :return: If sub-string meets any word prefix in the dictionary, return True
        """
        if sub_s in self.__all_dict:
            return True

    def search_words(self):
        """
        This function displays words with input prefix on search result area.
        """
        search_prefix = self.__search.get().strip().lower()
        self.__search_result.delete('1.0', tk.END)
        if len(search_prefix) < 2:
            self.__search_result.insert('1.0', 'Please give prefix with at least 2 letters.')
        elif search_prefix in self.__all_dict:
            symbol = ', '
            self.__search_result.insert('end', symbol.join(self.__all_dict[search_prefix]))
            self.__search_result.see('end')
        else:
            self.__search_result.insert('1.0', f'No word with prefix \'{search_prefix}\'.')
