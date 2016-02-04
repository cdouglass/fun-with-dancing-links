#! /usr/bin/env python

import unittest
from exact_cover import *

# does not check name or size attributes
def is_valid_matrix(matrix):
  # check circularity of headers
  horizontal_moves = [lambda x: x.right, lambda x: x.left]
  vertical_moves = [lambda x: x.down, lambda x: x.up]
  if not all(check_circularity(matrix, fn) for fn in horizontal_moves):
    return False

  # for each column, check circularity of the column and of each non-column node (use type == to avoid rechecking)
  # this doesn't feel compact enough to me, oh well, fix it later
  # I feel like a lot of this would be nicer if I knew how to use iterators better
  columns = []
  cn = matrix.right
  while cn != matrix and cn not in columns:
    columns.append(cn)

  for column in columns:
    if not all(check_circularity(column, fn) for fn in vertical_moves):
      return False
    rows = []
    cr = column.down
    while cr != column and cr not in rows:
      rows.append(cr)
      if not all(check_circularity(cr, fn) for fn in horizontal_moves):
        return False

  return True

# OK I've THREE TIMES done the thing where I iterate through every element in a linked list, I need to abstract this shit.

def check_circularity(node, fn):
  root = node
  visited_nodes = []
  current_node = fn(node)
  while current_node != root:
    if current_node is None or current_node in visited_nodes:
      return False
    visited_nodes.append(current_node)
    current_node = fn(current_node)
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

  def test_make_matrix_from_columns(self):
    names = ['a', 'b', 'c', 'd', 'e']
    columns = [Column(i) for i in names]
    matrix = make_matrix_from_columns(columns)
    self.assertTrue(is_valid_matrix(matrix))
    self.assertEqual('a', matrix.right.name)

  def test_make_matrix_from_arrays(self):
    names = ['a', 'b', 'c', 'd', 'e']
    arr = [[1, 0, 0, 1, 0], [0, 0, 1, 0, 1], [1, 0, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0]]
    matrix = make_matrix_from_rows(names, arr)
    self.assertTrue(is_valid_matrix(matrix))
    self.assertEqual(2, matrix.right.size)
    self.assertEqual(0, matrix.right.right.size)
    self.assertEqual(3, matrix.right.right.right.right.size)

  def test_make_arrays_from_matrix(self):
    return None
    # TODO

  def test_add_row_to_matrix(self):
    return None
    # TODO
  
  def test_remove_row_from_matrix(self):
    return None
    # TODO

  def test_restore_row_to_matrix(self):
    return None
    # TODO

  def test_add_column_to_matrix(self):
    return None
    # TODO

  def test_remove_column_from_matrix(self):
    return None
    # TODO

  def test_restore_column_to_matrix(self):
    return None

# given a problem formatted as a matrix, does it yield a proper solution?
class TestAlgorithm(unittest.TestCase):

  def test_backtrack(self):
    return None
  # TODO break this up?

  def test_impossible(self):
    return None
  # TODO

  def test_simple_case(self):
    return None
  # TODO

  def test_four_queens(self):
    return None
  # TODO


if __name__ == '__main__':
  unittest.main()
