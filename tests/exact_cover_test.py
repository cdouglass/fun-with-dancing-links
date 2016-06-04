#! /usr/bin/env python

import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import lib # only works when running from same directory

from lib import exact_cover
from lib.exact_cover import *


# Column -> bool
def is_valid_column(column):
  horizontal_moves = [lambda x: x.right, lambda x: x.left]
  vertical_moves = [lambda x: x.down, lambda x: x.up]
  if not all([check_circularity(v_move, column) for v_move in vertical_moves]): # check column is circular both ways
    return False
  else: # moving downward, checks each row is circular both ways
    return all(all(loop_through_circular_list(column, vertical_moves[0], partial(check_circularity, h_move))) for h_move in horizontal_moves)

# does not check name or size attributes
# does not check that lists have same connections in each direction
# Root -> bool
def is_valid_matrix(matrix):
  horizontal_moves = [lambda x: x.right, lambda x: x.left] # why the heck does this fail if I use left and right???
  for h_move in horizontal_moves:
    if not check_circularity(h_move, matrix): # check circularity of headers
      return False
    if not all(loop_through_circular_list(matrix, h_move, is_valid_column)):
      return False
  return True

# Root -> bool
def check_circularity(move, node): # changed order to allow currying
  def null_fn(*args): # silly
    return None
  try:
    loop_through_circular_list(node, move, null_fn) # we don't care about fn here
  except InvalidLooping:
    return False
  return True

class TestHelperFunctions(unittest.TestCase):

  def setUp(self):
    self.root = Root()
    self.column = Column('hello')
    self.node = Node(self.column)

  def test_valid_matrix_passes_minimal(self):
    self.assertTrue(is_valid_matrix(self.root))

  def test_matrix_validation_right_column_only(self):
    self.root.insert_right(self.column)
    self.assertTrue(is_valid_matrix(self.root))
    self.column.right = None
    self.assertFalse(is_valid_matrix(self.root))
    self.column.right = self.column
    self.assertFalse(is_valid_matrix(self.root))

  def test_matrix_validation_left_column_only(self):
    self.root.insert_right(self.column)
    self.assertTrue(is_valid_matrix(self.root))
    self.column.left = None
    self.assertFalse(is_valid_matrix(self.root))
    self.column.left = self.column
    self.assertFalse(is_valid_matrix(self.root))

  def test_matrix_validation_up_with_rows(self):
    self.root.insert_right(self.column)
    self.column.insert_below(self.node)
    self.assertTrue(is_valid_matrix(self.root))
    self.node.up = None
    self.assertFalse(is_valid_matrix(self.root))
    self.node.up = self.node
    self.assertFalse(is_valid_matrix(self.root))
    self.node.up = self.root
    self.assertRaises(AttributeError, is_valid_matrix, self.root)

  def test_matrix_validation_left_with_rows(self):
    self.root.insert_right(self.column)
    self.column.insert_below(self.node)
    self.assertTrue(is_valid_matrix(self.root))
    self.node.left = None
    self.assertFalse(is_valid_matrix(self.root))
    self.node.left = self.column
    self.assertFalse(is_valid_matrix(self.root))

  def test_matrix_validation_down_with_rows(self):
    self.root.insert_right(self.column)
    self.column.insert_below(self.node)
    self.assertTrue(is_valid_matrix(self.root))
    self.node.down = None
    self.assertFalse(is_valid_matrix(self.root))
    self.node.down = self.node
    self.assertFalse(is_valid_matrix(self.root))
    self.node.down = self.root
    self.assertRaises(AttributeError, is_valid_matrix, self.root)

  def test_matrix_validation_right_with_rows(self):
    self.root.insert_right(self.column)
    self.column.insert_below(self.node)
    self.assertTrue(is_valid_matrix(self.root))
    self.node.right = None
    self.assertFalse(is_valid_matrix(self.root))
    self.node.right = self.column
    self.assertFalse(is_valid_matrix(self.root))

class TestMatrixOperations(unittest.TestCase):

  def setUp(self):
    self.names = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    self.rows = [['a', 'd'], ['a', 'd', 'g'], ['b', 'c', 'f'],
            ['b', 'g'], ['c', 'e', 'f'], ['d', 'e', 'g']]
    self.matrix = make_matrix_from_rows(self.names, self.rows)
    return None

  def test_remove_element_horizontally(self):
    col = self.matrix.right
    remove_horizontally(col)
    self.assertTrue(is_valid_matrix(self.matrix))
    self.assertEqual(self.matrix.right, col.right)

  def test_remove_element_vertically(self):
    node = self.matrix.right.down
    remove_vertically(node)
    self.assertEqual(1, self.matrix.right.size)

  def test_cover_column(self):
    col = self.matrix.right
    cover_column(col)
    rows = sorted(make_rows_from_matrix(self.matrix))
    expected_rows = [['b', 'c', 'f'], ['b', 'g'], ['c', 'e', 'f'], ['d', 'e', 'g']]
    self.assertEqual(expected_rows, rows)

  def test_uncover_column(self): # confirm undoes changes
    col = self.matrix.right
    cover_column(col)
    uncover_column(col)
    rows = sorted(make_rows_from_matrix(self.matrix))
    self.assertEqual(rows, self.rows)

  def test_make_matrix_from_columns(self):
    columns = [Column(i) for i in self.names]
    matrix = make_matrix_from_columns(columns)
    self.assertTrue(is_valid_matrix(matrix))
    self.assertEqual('a', matrix.right.name)

  def test_make_matrix_from_rows(self):
    self.assertTrue(is_valid_matrix(self.matrix))
    self.assertEqual(2, self.matrix.right.size)
    self.assertEqual(3, self.matrix.right.right.right.right.size)

  def test_make_rows_from_matrix(self):
    rows = sorted(make_rows_from_matrix(self.matrix))
    self.assertEqual(rows, self.rows)
    rows = sorted(make_rows_from_matrix(self.matrix)) # confirm matrix isn't changed in the process
    self.assertEqual(rows, self.rows)

# given a problem formatted as a matrix, does it yield a proper solution?
class TestAlgorithm(unittest.TestCase):

  def setUp(self):
    self.names = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    self.rows = [['a', 'd'], ['a', 'd', 'g'], ['b', 'c', 'f'],
            ['b', 'g'], ['c', 'e', 'f'], ['d', 'e', 'g']]
    self.matrix = make_matrix_from_rows(self.names, self.rows)

  def test_impossible(self):
    rows = [['a', 'd', 'f'], ['a', 'd', 'g'], ['b', 'c', 'f'],
            ['b', 'g'], ['c', 'e', 'f'], ['d', 'e', 'g']]
    matrix = make_matrix_from_rows(self.names, rows)
    solutions = []
    find_exact_cover(matrix, solutions, [])
    self.assertEqual([], solutions)

  def test_simple_case(self):
    solutions = []
    find_exact_cover(self.matrix, solutions, [])
    pretty_solutions = sorted([[sorted(get_column_names_for_row(row) + [row.column.name]) for row in solution] for solution in solutions])
    self.assertEqual([[['a', 'd'], ['b', 'g'], ['c', 'e', 'f']]], pretty_solutions)
    self.assertEqual(1, len(solutions))
    rows = sorted(make_rows_from_matrix(self.matrix)) # confirm matrix unchanged
    self.assertEqual(rows, self.rows)

  def test_multiple_solutions(self):
    rows = [['c', 'd', 'e'], ['a', 'f'], ['b', 'g'],
            ['a', 'b'], ['f', 'g'], ['b', 'c', 'd', 'e', 'g']]
    multiple_solutions_matrix = make_matrix_from_rows(self.names, rows)
    solutions = []
    find_exact_cover(multiple_solutions_matrix, solutions, [])
    pretty_solutions = sorted([[sorted(get_column_names_for_row(row) + [row.column.name]) for row in solution] for solution in solutions])
    self.assertEqual([[['a', 'b'], ['c', 'd', 'e'], ['f', 'g']], [['a', 'f'], ['b', 'c', 'd', 'e', 'g']], [['a', 'f'], ['b', 'g'], ['c', 'd', 'e']]], pretty_solutions)
    self.assertEqual(3, len(solutions))
