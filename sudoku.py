#! /usr/bin/env python
from itertools import cycle

board_a = [5, 3, 0, 0, 7, 0, 0, 0, 0,
           6, 0, 0, 1, 9, 5, 0, 0, 0,
           0, 9, 8, 0, 0, 0, 0, 6, 0,
           8, 0, 0, 0, 6, 0, 0, 0, 3,
           4, 0, 0, 8, 0, 3, 0, 0, 1,
           7, 0, 0, 0, 2, 0, 0, 0, 6,
           0, 6, 0, 0, 0, 0, 2, 8, 0,
           0, 0, 0, 4, 1, 9, 0, 0, 5,
           0, 0, 0, 0, 8, 0, 0, 7, 9]

board_b = [1, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 2, 0, 0, 6, 7, 8, 9, 0,
           3, 0, 0, 0, 4, 0, 0, 0, 0,
           0, 4, 0, 0, 3, 0, 0, 0, 0,
           0, 0, 0, 0, 2, 1, 6, 7, 0,
           0, 6, 0, 0, 0, 0, 0, 8, 0,
           0, 0, 7, 0, 0, 0, 0, 4, 0,
           0, 8, 0, 0, 9, 3, 7, 2, 0,
           0, 0, 9, 0, 0, 0, 0, 0, 0]

boards = cycle([board_a, board_b])

def get_new_board():
  return(next(boards))

def get_empty_board():
  return([0] * 81)

# TODO
  # GUI to get new board
  # GUI to add numbers
  # GUI to remove numbers
