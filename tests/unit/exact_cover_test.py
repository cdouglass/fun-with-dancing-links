import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from lib.exact_cover import *
from lib.n_queens import flatten
import unittest

def included_in(elt, lst):
  if len(lst) == 0:
    return False
  elif elt == lst[0]:
    return True
  else:
    return included_in(elt, lst[1:len(lst)])

# Column -> bool
def is_valid_column(column):
  horizontal_moves = ['right', 'left']
  vertical_moves = ['down', 'up']
  if not all([check_circularity(v_move, column) for v_move in vertical_moves]): # check column is circular both ways
    return False
  else: # moving downward, checks each row is circular both ways
    return all(all(column.loop_through_circular_list(vertical_moves[0],
                                                     lambda x: check_circularity(h_move, x)))
              for h_move in horizontal_moves)

# does not check name or size attributes
# does not check that lists have same connections in each direction
# Root -> bool
def is_valid_matrix(matrix):
  horizontal_moves = ['right', 'left']
  for h_move in horizontal_moves:
    if not (check_circularity(h_move, matrix) and
           all(matrix.loop_through_circular_list(h_move, is_valid_column))):
      return False
  return True

# Root -> bool
def check_circularity(move, node):
  try:
    node.loop_through_circular_list(move, lambda *args: None)
  except InvalidLooping:
    return False
  return True

def standardize_solution_set(solutions):
  return sorted([sorted([sorted(row) for row in sol]) for sol in solutions])

class TestMatrixTestHelperFunctions(unittest.TestCase):

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
    self.matrix = make_matrix_from_rows(self.rows, self.names)
    return None

  def test_remove_element_horizontally(self):
    col = self.matrix.right
    col.remove_horizontally()
    self.assertTrue(is_valid_matrix(self.matrix))
    self.assertEqual(self.matrix.right, col.right)

  def test_remove_element_vertically(self):
    node = self.matrix.right.down
    node.remove_vertically()
    self.assertEqual(1, self.matrix.right.size)

  def test_cover_column(self):
    col = self.matrix.right
    col.cover_column()
    rows = sorted(make_rows_from_matrix(self.matrix))
    expected_rows = [['b', 'c', 'f'], ['b', 'g'], ['c', 'e', 'f'], ['d', 'e', 'g']]
    self.assertEqual(expected_rows, rows)

  def test_uncover_column(self): # confirm undoes changes
    col = self.matrix.right
    col.cover_column()
    col.uncover_column()
    rows = sorted(make_rows_from_matrix(self.matrix))
    self.assertEqual(self.rows, rows)

  def test_secondary_column(self):
    col = self.matrix.left
    last_col = col.left
    col.make_secondary()
    self.assertEqual(col, col.left)
    self.assertEqual(col, col.right)
    self.assertEqual(last_col, self.matrix.left)
    self.assertEqual(self.matrix, last_col.right)
    rows = sorted(make_rows_from_matrix(self.matrix))
    self.assertEqual(self.rows, rows) # making a column secondary doesn't interfere with extracting rows from matrix

  def test_cover_and_uncover_all_other_columns_in_row(self):
    row = ['a', 'b', 'g']
    row_node = self.matrix.add_row(row)
    row_node.cover_all_other_columns_in_row()
    expected_rows = [['a', 'd'], ['c', 'e', 'f']]
    self.assertEqual(expected_rows, sorted(make_rows_from_matrix(self.matrix)))
    row_node.uncover_all_other_columns_in_row()
    self.assertEqual(sorted(self.rows + [row]), sorted(make_rows_from_matrix(self.matrix)))

  def test_add_row_to_matrix(self):
    row = ['d', 'f']
    expected_rows = self.rows + [row]
    self.matrix.add_row(row)
    rows = sorted(make_rows_from_matrix(self.matrix))
    self.assertEqual(expected_rows, rows)

  def test_make_matrix_from_columns(self):
    columns = [Column(i) for i in self.names]
    matrix = make_matrix_from_columns(columns)
    self.assertTrue(is_valid_matrix(matrix))
    self.assertEqual('a', matrix.right.name)

  def test_make_matrix_from_rows(self):
    self.assertTrue(is_valid_matrix(self.matrix))
    self.assertEqual(2, self.matrix.right.size)
    self.assertEqual(3, self.matrix.right.right.right.right.size)

  def test_make_matrix_from_single_node_rows(self):
    rows = [['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g']]
    matrix = make_matrix_from_rows(rows, self.names)
    self.assertTrue(is_valid_matrix(matrix))

  def test_make_rows_from_matrix(self):
    rows = sorted(make_rows_from_matrix(self.matrix))
    self.assertEqual(rows, self.rows)
    rows = sorted(make_rows_from_matrix(self.matrix)) # confirm matrix isn't changed in the process
    self.assertEqual(rows, self.rows)

class TestAlgorithm(unittest.TestCase):

  def setUp(self):
    self.names = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    self.unique_solution_rows = [['a', 'd'], ['a', 'd', 'g'], ['b', 'c', 'f'],
            ['b', 'g'], ['c', 'e', 'f'], ['d', 'e', 'g']]
    self.unique_solution_matrix = make_matrix_from_rows(self.unique_solution_rows, self.names)
    self.unique_solution = [[['a', 'd'], ['b', 'g'], ['c', 'e', 'f']]]
    self.multiple_solutions_rows = [['c', 'd', 'e'], ['a', 'f'], ['b', 'g'],
                                    ['a', 'b'], ['f', 'g'], ['b', 'c', 'd', 'e', 'g']]
    self.expected_multiple_solutions = [[['a', 'b'], ['c', 'd', 'e'], ['f', 'g']],
                                        [['a', 'f'], ['b', 'c', 'd', 'e', 'g']],
                                        [['a', 'f'], ['b', 'g'], ['c', 'd', 'e']]]

  def test_algorithm_on_unsolvable_matrix(self):
    rows = [['a', 'd', 'f'], ['a', 'd', 'g'], ['b', 'c', 'f'],
            ['b', 'g'], ['c', 'e', 'f'], ['d', 'e', 'g']]
    matrix = make_matrix_from_rows(rows, self.names)
    solutions = find_exact_covers(matrix)
    self.assertEqual([], solutions)

  def test_finds_solution_on_simple_matrix(self):
    solutions = find_exact_covers(self.unique_solution_matrix)
    pretty_solutions = sorted([sorted([sorted(row.get_column_names_for_row())
                                for row in solution])
                              for solution in solutions])
    self.assertEqual(1, len(solutions))
    self.assertEqual(self.unique_solution, pretty_solutions)
    rows = sorted(make_rows_from_matrix(self.unique_solution_matrix)) # confirm matrix unchanged
    self.assertEqual(rows, self.unique_solution_rows)

  def test_finds_multiple_solutions_on_matrix(self):
    multiple_solutions_matrix = make_matrix_from_rows(self.multiple_solutions_rows, self.names)
    solutions = find_exact_covers(multiple_solutions_matrix)
    solutions_as_row_lists = [[row.get_column_names_for_row() for row in sol] for sol in solutions]
    self.assertEqual(self.expected_multiple_solutions, standardize_solution_set(solutions_as_row_lists))
    self.assertEqual(3, len(solutions))

  def test_finds_solution_for_simple_row_set(self):
    solutions = find_exact_cover_for_rows(self.unique_solution_rows, self.names)
    self.assertEqual(self.unique_solution, standardize_solution_set(solutions))
    self.assertEqual(1, len(solutions))

  def test_finds_multiple_solutions_for_row_set(self):
    solutions = find_exact_cover_for_rows(self.multiple_solutions_rows, self.names)
    self.assertEqual(self.expected_multiple_solutions, standardize_solution_set(solutions))
    self.assertEqual(3, len(solutions))

  def test_finds_solution_for_rows_with_one_node_each(self):
    row_list = [[name] for name in self.names]
    solutions = find_exact_cover_for_rows(row_list, self.names)
    self.assertEqual([row_list], standardize_solution_set(solutions)) 

  # isomorphic to n queens for n = 2 if we ignore the minor diagonal
  # TODO secondary columns
  def test_2_queens(self):
    names = ["r0", "r1", "c0", "c1", "md", "d-", "d+"]
    placements = [["r0", "c0", "md"],
                  ["r0", "c1", "d+"],
                  ["r1", "c0", "d-"],
                  ["r1", "c1", "md"],
                  ["md"],
                  ["d+"],
                  ["d-"]] # diagonals should be covered AT MOST once - these can bring it up to 1
    sols = find_exact_cover_for_rows(placements, names)
    self.assertEqual(1, len(sols))

class TestVariationsOnFindExactCovers(unittest.TestCase):

  def setUp(self):
    self.names = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    self.unique_solution_rows = [['a', 'd'], ['a', 'd', 'g'], ['b', 'c', 'f'],
            ['b', 'g'], ['c', 'e', 'f'], ['d', 'e', 'g']]
    self.unique_solution_matrix = make_matrix_from_rows(self.unique_solution_rows, self.names)
    self.unique_solution = [['a', 'd'], ['b', 'g'], ['c', 'e', 'f']]
    self.multiple_solutions_rows = [['c', 'd', 'e'], ['a', 'f'], ['b', 'g'],
                                    ['a', 'b'], ['f', 'g'], ['b', 'c', 'd', 'e', 'g']]
    self.expected_multiple_solutions = [[['a', 'b'], ['c', 'd', 'e'], ['f', 'g']],
                                        [['a', 'f'], ['b', 'c', 'd', 'e', 'g']],
                                        [['a', 'f'], ['b', 'g'], ['c', 'd', 'e']]]

  def test_find_two_solutions_of_several(self):
    matrix = make_matrix_from_rows(self.multiple_solutions_rows, self.names)
    first_two_solutions = find_n_exact_covers(matrix, 2)
    pretty_solutions = [[sorted(row.get_column_names_for_row()) for row in solution] for solution in first_two_solutions]
    self.assertEqual(2, len(first_two_solutions))
    for sol in pretty_solutions:
      self.assertTrue(included_in(sol, self.expected_multiple_solutions))
