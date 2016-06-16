import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from lib.n_queens import *
import unittest

class TestMatchers(unittest.TestCase):

  def test_column_matcher(self):
    matcher = column_matcher(2)
    self.assertTrue(matcher(2, 10))
    self.assertFalse(matcher(0, 2))

  def test_row_matcher(self):
    matcher = row_matcher(2)
    self.assertTrue(matcher(10, 2))
    self.assertFalse(matcher(2, 0))

  def test_forward_diagonal_matcher_major_diagonal(self):
    matcher = forward_diag_matcher(0)
    self.assertTrue(matcher(0, 0))
    self.assertTrue(matcher(8, 8))
    self.assertFalse(matcher(8, 7))

  def test_forward_diagonal_matcher_positive(self):
    matcher = forward_diag_matcher(2)
    self.assertTrue(matcher(2, 0))
    self.assertTrue(matcher(3, 1))
    self.assertFalse(matcher(3, 0))

  def test_forward_diagonal_matcher_negative(self):
    matcher = forward_diag_matcher(-2)
    self.assertTrue(matcher(0, 2))
    self.assertTrue(matcher(1, 3))
    self.assertFalse(matcher(0, 3))

  def test_reverse_diagonal_matcher(self):
    matcher = reverse_diag_matcher(5)
    self.assertTrue(matcher(5, 0))
    self.assertTrue(matcher(0, 5))
    self.assertTrue(matcher(3, 2))
    self.assertFalse(matcher(3, 1))
    self.assertFalse(matcher(3, 3))

  def test_col_id(self):
    self.assertEqual("row:3", col_id("row", 3))

  def test_generate_primary_headers(self):
    headers = primary_column_headers(2)
    expected_headers = ["col:1", "row:1", "col:0", "row:0"]
    self.assertEqual(expected_headers, headers)

  def test_generate_primary_headers(self):
    headers = secondary_column_headers(2)
    expected_headers = ["f_diag:-1", "f_diag:0", "f_diag:1", "r_diag:1"]
    self.assertEqual(expected_headers, headers)

  def test_header_to_matcher(self):
    headers = ["col:2", "row:2", "f_diag:-2", "r_diag:5"]
    matchers = [header_to_matcher(header) for header in headers]
    self.assertTrue(matchers[0](2, 10))
    self.assertTrue(matchers[1](10, 2))
    self.assertTrue(matchers[2](0, 2))
    self.assertTrue(matchers[3](5, 0))

class TestOtherUtilities(unittest.TestCase):

  def test_generate_all_possible_queen_positions(self):
    # TODO
    return None

  def test_position_to_row(self):
    # TODO
    return None

  def test_row_to_position(self):
    # TODO
    return None

  def test_position_list_to_board(self):
    # TODO
    return None

  def test_format_board(self):
    # TODO
    return None

  def test_flatten(self):
    # TODO
    return None

class testEndpoint(unittest.TestCase):

  def test_n_queens_with_no_solutions(self):
    result = n_queens(3)
    self.assertEqual([], result)

  def test_n_queens_with_two_solutions(self):
    solution = n_queens(4)[0]
    expected = [0] * 16
    for i in [2, 4, 11, 13]:
      expected[i] = 1
    self.assertEqual(expected, flatten(solution))

class testSolvers(unittest.TestCase):

  def test_solve_n_queens(self):
    # TODO
    return None

  def test_get_all_solutions(self):
    # TODO
    return None
