import random

class InvalidLooping(Exception):
  
  def __init__(self):
    Exception.__init__(self)

class Root:
  def __init__(self):
    self.left  = self
    self.right = self
  def insert_right(self, column):
    column.right    = self.right
    column.left     = self
    self.right.left = column
    self.right      = column
# does NOT apply fn to given node - ONLY to rest in its loop!
# Root, (fn(Root) -> Root), (fn(Root, [Root]) -> T) -> [T]
  def loop_through_circular_list(self, direction, fn):
    move = lambda x: getattr(x, direction)
    current_node  = move(self)
    visited_nodes = [self]
    results = []
    while current_node != self:
      if current_node is None or current_node in visited_nodes:
        raise InvalidLooping
      results.append(fn(current_node))
      visited_nodes.append(current_node)
      current_node = move(current_node)
    return results
  # Root, [header] -> Node
  def add_row(self, row):
    nodes = self.loop_through_circular_list('right', lambda x: x.add_node_to_column_if_element_present(row))
    nodes = [n for n in nodes if n is not None]
    if len(nodes) > 0:
      current_node = nodes[0]
      for node in nodes:
        current_node.insert_right(node)
        current_node = node
    return nodes[0]

class Node(Root):
  def __init__(self, column):
    Root.__init__(self)
    self.column = column
    self.up     = self
    self.down   = self
  def insert_below(self, node):
    node.down    = self.down
    node.up      = self
    self.down.up = node
    self.down    = node
    self.column.size += 1
  def remove_vertically(self):
    self.up.down = self.down
    self.down.up = self.up
    self.column.size -= 1
  def restore_vertically(self):
    self.up.insert_below(self)
  def cover_row(self):
    self.loop_through_circular_list('right', lambda n: n.remove_vertically())
  def uncover_row(self):
    self.loop_through_circular_list('right', lambda x: x.restore_vertically())
  def get_column_names_for_row(self):
    return [self.column.name] + self.loop_through_circular_list('right', lambda x: x.column.name)
  def cover_all_other_columns_in_row(self):
    self.loop_through_circular_list('right', lambda x: x.column.cover_column())
  def uncover_all_other_columns_in_row(self):
    self.loop_through_circular_list('left', lambda x: x.column.uncover_column())

class Column(Node):
  def __init__(self, name):
    self.name   = name
    self.size   = 0
    self.column = self
    Node.__init__(self, self.column)
  def remove_horizontally(self):
    self.left.right = self.right
    self.right.left = self.left
  def make_secondary(self):
    self.remove_horizontally()
    self.left = self
    self.right = self
  def restore_horizontally(self):
    self.left.insert_right(self)
  # Column -> Root
  def cover_column(self):
    self.remove_horizontally()
    # for each non-top-level node in column, remove that node from matrix
    self.loop_through_circular_list('down', lambda x: x.cover_row()) # removing top to bottom (so must uncover bottom to top)
  def uncover_column(self):
    self.loop_through_circular_list('up', lambda x: x.uncover_row())
    self.restore_horizontally()
  # [str], Column -> Node
  def add_node_to_column_if_element_present(self, row):
    if self.name in row:
      node = Node(self)
      self.up.insert_below(node)
      return node

# Algorithm

# TODO most constrained instead
# TODO in that case will using existing order to break ties provide enough randomness?
def next_column(matrix):
  return matrix.right

def is_matrix_empty(matrix):
  return matrix.right == matrix

# TODO test
def find_random_partial_cover_with_unique_solution(matrix):
  full_solutions = [] # initialize here so done() has a handle to it
  current_partial_solution = []
  best_partial_solution = []
  def done():
    if len(full_solutions) == 1:
      print("found a solution")
      solution_set = set(full_solutions[0])
      partial = set(current_partial_solution)
      if partial.issubset(solution_set):
        best_partial_solution[0:len(best_partial_solution)] = current_partial_solution.copy()
    return len(full_solutions) > 1
  solution = find_exact_covers(matrix, full_solutions, current_partial_solution, done)[0]
  return [best_partial_solution, solution]

def find_n_exact_covers(matrix, n):
  full_solutions = [] # initialize here so done() has a handle to it
  done = lambda: len(full_solutions) >= n
  return find_exact_covers(matrix, full_solutions, None, done)

def find_exact_covers(matrix, full_solutions = None, partial_solution = None, done = lambda: False, next_col = next_column):
  if done():
    return full_solutions
  # Python creates default argument objects when function is defined
  if full_solutions is None:
    full_solutions = []
  if partial_solution is None:
    partial_solution = []
  if is_matrix_empty(matrix):
    full_solutions.append(partial_solution.copy())
  elif matrix.right.up != matrix.right:
    column = next_col(matrix)
    column.cover_column()
    rows_in_column = column.loop_through_circular_list('down', lambda x: x) # [Node]
    for row in rows_in_column:
      partial_solution.append(row)
      row.cover_all_other_columns_in_row()
      find_exact_covers(matrix, full_solutions, partial_solution, done, next_col)
      if done(): # lets find_partial_cover return sooner
        return full_solutions
      row.uncover_all_other_columns_in_row()
      partial_solution.pop()
    column.uncover_column() # restore matrix to original state
  return full_solutions

# convenience
# [str], [[str]] -> [[[str]]]
def find_exact_cover_for_rows(rows, primary_headers, secondary_headers=[]):
  matrix = make_matrix_from_rows(rows, primary_headers, secondary_headers)
  solutions = find_exact_covers(matrix)
  return [[node.get_column_names_for_row() for node in sol] for sol in solutions]

# Matrix manipulation

# Only sets up structure of matrix - if columns are populated already, nodes will not get connected correctly
# [Column] -> Root
def make_matrix_from_columns(columns):
  root = Root()
  current = root
  for column in columns:
    current.insert_right(column)
    current = column
  return root

# [str], [[int]] -> Root # old, want below instead
# [str], [[str]] -> Root
def make_matrix_from_rows(rows, primary_headers, secondary_headers=[]):
  primary_columns = [Column(header) for header in primary_headers]
  secondary_columns = [Column(header) for header in secondary_headers]
  matrix = make_matrix_from_columns(primary_columns + secondary_columns)
  for row in rows:
    matrix.add_row(row)
  for column in secondary_columns:
    column.make_secondary() # so find_exact_cover will not waste time covering columns that it's ok to leave uncovered (slight generalization of exact cover problem)
  return matrix

# column names constitute first row
# row order of output is not guaranteed, but we use a list not a set because sets should have immutable elements
# Root -> [str] + [[int]]
def make_rows_from_matrix(matrix):
  rows = []
  columns = []
  while matrix.right != matrix:
    column = matrix.right
    if column.down != column:
      raw_rows = column.loop_through_circular_list('down', lambda x: x.get_column_names_for_row())
      rows += [sorted(r) for r in raw_rows]
    column.cover_column()
    columns.append(column)
  for column in columns[::-1]:
    column.uncover_column() # undo changes to input matrix
  return rows
