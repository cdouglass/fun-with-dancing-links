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
  def loop_through_circular_list(self, move, fn):
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
    self.loop_through_circular_list(lambda x: x.right, lambda n: n.remove_vertically())
  def uncover_row(self):
    self.loop_through_circular_list(lambda x: x.right, lambda x: x.restore_vertically())
  def get_column_names_for_row(self):
    return [self.column.name] + self.loop_through_circular_list(lambda x: x.right, lambda x: x.column.name)

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
    self.loop_through_circular_list(lambda x: x.down, lambda x: x.cover_row()) # removing top to bottom (so must uncover bottom to top)
  def uncover_column(self):
    self.loop_through_circular_list(lambda x: x.up, lambda x: x.uncover_row())
    self.restore_horizontally()
  # [str], Column -> Node
  def add_node_to_column_if_element_present(self, row):
    if self.name in row:
      node = Node(self)
      self.up.insert_below(node)
      return node

# Algorithm

def find_exact_cover(matrix, full_solutions = [], partial_solution = []):
  if matrix.right == matrix:
    full_solutions.append(partial_solution.copy())
    partial_solution == [] # terminate successfully
  elif matrix.right.up == matrix.right:
    partial_solution == [] # terminate unsuccessfully
  else:
    column = matrix.right
    column.cover_column()
    rows_in_column = column.loop_through_circular_list(lambda x: x.down, lambda x: x) # [Node]
    for row in rows_in_column:
      partial_solution.append(row)
      row.loop_through_circular_list(lambda x: x.right, lambda x: x.column.cover_column())
      find_exact_cover(matrix, full_solutions, partial_solution)
      row.loop_through_circular_list(lambda x: x.left, lambda x: x.column.uncover_column())
      partial_solution.pop()
    column.uncover_column() # restore matrix to original state

# convenience
# [str], [[str]] -> [[[str]]]
def find_exact_cover_for_rows(rows, primary_headers, secondary_headers=[]):
  solutions = []
  matrix = make_matrix_from_rows(rows, primary_headers, secondary_headers)
  find_exact_cover(matrix, solutions)
  return [[node.get_column_names_for_row() for node in sol] for sol in solutions]

# Moving info in and out of matrices

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
    nodes = matrix.loop_through_circular_list(lambda x: x.right, lambda x: x.add_node_to_column_if_element_present(row))
    nodes = [n for n in nodes if n is not None]
    if len(nodes) > 0:
      current_node = nodes[0]
      for node in nodes:
        current_node.insert_right(node)
        current_node = node
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
      raw_rows = column.loop_through_circular_list(lambda x: x.down, lambda x: x.get_column_names_for_row())
      rows += [sorted(r) for r in raw_rows]
    column.cover_column()
    columns.append(column)
  for column in columns[::-1]:
    column.uncover_column() # undo changes to input matrix
  return rows
