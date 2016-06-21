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

  def test_add_random_clue_with_space(self):
    board = self.empty_board
    for i in range(1, 10):
      add_random_clue(board)
    expected = empty_board()
    expected[0][7] = 8
    expected[1][0] = 6
    expected[2][1] = 4
    expected[2][3] = 7
    expected[3][5] = 4
    expected[4][1] = 3
    expected[5][7] = 5
    expected[6][5] = 7
    expected[8][3] = 3
    self.assertEqual(flatten(expected), flatten(board))

  def test_add_random_clue_raises_exception_for_full_board(self):
    with self.assertRaises(InvalidBoard):
      add_random_clue(self.board)

  def test_random_clue_set(self):
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
    self.assertEqual(flatten(expected), flatten(board))