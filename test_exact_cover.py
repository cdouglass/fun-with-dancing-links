#! /usr/bin/env python

import unittest
from exact_cover import *

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
  def null_fn(*args): # TODO get rid of this
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
    arr = [[0, 0, 1, 0, 1, 1, 0], [1, 0, 0, 1, 0, 0, 1], [0, 1, 1, 0, 0, 1, 0],
           [1, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 1], [0, 0, 0, 1, 1, 0, 1]] # example from figure
    self.matrix = make_matrix_from_rows(self.names, arr)
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
    self.assertTrue(is_valid_matrix(self.matrix))
    self.assertEqual('b', self.matrix.right.name)
    self.assertEqual(1, self.matrix.right.right.right.size)

  def test_uncover_column(self):
    col = self.matrix.right
    cover_column(col)
    uncover_column(col)
    self.assertTrue(is_valid_matrix(self.matrix))
    self.assertEqual('a', self.matrix.right.name)
    self.assertEqual(3, self.matrix.right.right.right.right.size)

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
    self.assertEqual(6, len(rows))
    self.assertTrue(['c', 'e', 'f'] in rows)
    self.assertTrue(['a', 'd', 'g'] in rows)
    self.assertTrue(['b', 'c', 'f'] in rows)
    self.assertTrue(['a', 'd'] in rows)
    self.assertTrue(['b', 'g'] in rows)
    self.assertTrue(['d', 'e', 'g'] in rows)

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
