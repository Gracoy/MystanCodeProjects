"""
File: anagram.py
Name: 姜佳成
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

from anagrams_gui import FindAnagrams

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
WINDOW_WIDTH = 575            # Optimized window scale
WINDOW_HEIGHT = 630


def main():
    """
    This program finds all the anagrams for the word input.
    User can modify constant 'FILE' to try different dictionary files.
    Enter -1 to exit program.
    """
    all_dict = read_dictionary()
    FindAnagrams(WINDOW_WIDTH, WINDOW_HEIGHT, all_dict)


def read_dictionary():
    """
    Read the file and store all words into a dictionary.
    :return: (dict) Dictionary of all words in the file
    """
    all_dict = {}
    with open(FILE, 'r') as f:
        for line in f:
            new_line = line.strip()
            for i in range(len(new_line)):
                sub_s = new_line[0:i+1]
                if sub_s in all_dict:
                    all_dict[sub_s].append(new_line)
                else:
                    all_dict[sub_s] = [new_line]
    return all_dict  # dict = {'a':['a', 'aa', 'aah', ...], 'aa':['aa','aah', ...], ...}


if __name__ == '__main__':
    main()
