import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from lib.sudoku import *
from lib.n_queens import flatten
import unittest

class TestUtilities(unittest.TestCase):

  def setUp(self):
    random.seed(1002341)
    self.board = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                  [6, 7, 2, 1, 9, 5, 3, 4, 8],
                  [1, 9, 8, 3, 4, 2, 5, 6, 7],
                  [8, 5, 9, 7, 6, 1, 4, 2, 3],
                  [4, 2, 6, 8, 5, 3, 7, 9, 1],
                  [7, 1, 3, 9, 2, 4, 8, 5, 6],
                  [9, 6, 1, 5, 3, 7, 2, 8, 4],
                  [2, 8, 7, 4, 1, 9, 6, 3, 5],
                  [3, 4, 5, 2, 8, 6, 1, 7, 9]]
    self.empty_board = empty_board()


  def test_empty_board(self):
    self.assertEqual(9, len(self.empty_board))
    for row in self.empty_board:
      self.assertEqual(row, [None] * 9)

  def test_subgrid_middle(self):
    expected = [[7, 6, 1],
                [8, 5, 3],
                [9, 2, 4]]
    middle = subgrid(3, 5, self.board)
    for i in range(0, 3):
      self.assertEqual(expected[i], middle[i])

  def test_subgrid_upper_right(self):
    expected = [[9, 1, 2],
                [3, 4, 8],
                [5, 6, 7]]
    upper_right = subgrid(8, 0, self.board)
    for i in range(0, 3):
      self.assertEqual(expected[i], upper_right[i])

  def test_allowed_values_on_full_board(self):
    x, y = [2, 3]
    expected = set([self.board[y][x]])
    self.assertEqual(expected, allowed_values_at_coords(x, y, self.board))

  def test_allowed_values_on_empty_board(self):
    self.assertEqual(set(range(1, 10)), allowed_values_at_coords(1, 4, self.empty_board))

  def test_all_column_headers(self):
    self.assertEqual(324, len(column_headers()))

  def test_make_matrix_row_for_move(self):
    row = make_matrix_row_for_move(7, 3, 9)
    self.assertEqual(["9-row-3", "9-col-7", "9-subgrid-5", "7-cell-3"], row)

  # TODO
  def x_test_convert_board_to_matrix(self):
    board_to_matrix(self.empty_board)

  def test_allowed_values_on_partially_filled_board(self):
    partial_board = self.empty_board
    partial_board[0][5] = 1
    partial_board[0][0] = 2 # same subgrid
    partial_board[7][2] = 3 # same column
    partial_board[4][4] = 4
    partial_board[6][1] = 5
    partial_board[1][8] = 6 # same row
    partial_board[7][6] = 7
    partial_board[2][1] = 8 # same subgrid
    partial_board[1][5] = 9 # same row
    self.assertEqual(set([1, 4, 5, 7]), allowed_values_at_coords(2, 1, partial_board))
    partial_board[1][2] = 5
    self.assertEqual(set([1, 4, 5, 7]), allowed_values_at_coords(2, 1, partial_board)) # does not consider value at given coords

  # TODO rewrite once actually randomized again
  def x_test_random_clue_set(self):
    board = random_clue_set()
    expected = [[None, None, 1, None, None, None, None, 8, 9],
                [6, None, None, 1, None, None, None, None, None],
                [None, 4, None, 7, 5, None, None, None, None],
                [None, None, 8, 6, 1, 4, None, None, None],
                [None, 3, 7, None, None, None, None, None, None],
                [None, None, None, None, 9, 3, None, 5, None],
                [None, None, None, 9, None, 7, None, 4, None],
                [9, None, 3, None, None, None, None, None, 7],
                [None, None, None, 3, None, None, None, None, 8]]
    for row in board:
      print(str(row))
    self.assertEqual(flatten(expected), flatten(board))

class TestCreateBoard(unittest.TestCase):

  def setUp(self):
    n = None # to save space
    self.a = 1
    self.clues = [[5,    3,    None, None, 7,    None, None, None, None],
                  [6,    None, None, 1,    9,    5,    None, None, None],
                  [None, 9,    8,    None, None, None, None, 6,    None],
                  [8,    None, None, None, 6,    None, None, None, 3],
                  [4,    None, None, 8,    None, 3,    None, None, 1],
                  [7,    None, None, None, 2,    None, None, None, 6],
                  [None, 6,    None, None, None, None, 2,    8,    None],
                  [None, None, None, 4,    1,    9,    None, None, 5],
                  [None, None, None, None, 8,    None, None, 7,    9]]
    self.solution = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                     [6, 7, 2, 1, 9, 5, 3, 4, 8],
                     [1, 9, 8, 3, 4, 2, 5, 6, 7],
                     [8, 5, 9, 7, 6, 1, 4, 2, 3],
                     [4, 2, 6, 8, 5, 3, 7, 9, 1],
                     [7, 1, 3, 9, 2, 4, 8, 5, 6],
                     [9, 6, 1, 5, 3, 7, 2, 8, 4],
                     [2, 8, 7, 4, 1, 9, 6, 3, 5],
                     [3, 4, 5, 2, 8, 6, 1, 7, 9]]

  def test_clues_are_valid(self):
    solutions = find_n_solutions(self.clues, 2)
    self.assertEqual(flatten(self.solution), flatten(solutions[0])) # TODO

  # TODO
  def x_test_generate_clues(self):
    print(generate_clue_set())
    # TODO
