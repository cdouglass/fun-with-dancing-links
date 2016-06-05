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
# TODO this way of passing functions to loop_through_circular_list is... ick. Can I replace this somehow?
# does NOT apply fn to given node - ONLY to rest in its loop!
# Root, (fn(Root) -> Root), (fn(Root, [Root]) -> T) -> [T]
  def loop_through_circular_list(self, move, fn):
    current_node  = move(self)
    visited_nodes = [self]
    results = []
    while current_node != self:
      if current_node is None or current_node in visited_nodes:
        raise InvalidLooping
      results.append(fn(current_node)) # ugh
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
  # TODO doesn't include own column but should!
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

# not really using return value here
def find_exact_cover(matrix, full_solutions = [], partial_solution = []):
  if matrix.right == matrix:
    full_solutions.append(partial_solution.copy())
    partial_solution == [] # terminate successfully
  elif matrix.right.up == matrix.right:
    partial_solution == [] # terminate unsuccessfully
  else:
    # TODO this never happens with n queens - the dead end case is happening immediately so the matrix can't be getting set up right!
    column = matrix.right # TODO improve by picking column with fewest elements instead
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
def find_exact_cover_for_rows(names, rows):
  solutions = []
  matrix = make_matrix_from_rows(names, rows)
  find_exact_cover(matrix, solutions)
  return [[node.get_column_names_for_row() for node in sol] for sol in solutions]

# Moving info in and out of matrices

# [Column] -> Root
def make_matrix_from_columns(columns):
  cols = sorted(columns, key = lambda c: c.name) # sorted creates new sorted array; sort modifies in place
  root = Root()
  current = root
  for col in cols:
    current.insert_right(col)
    current = col
  return root

# [str], [[int]] -> Root # old, want below instead
# [str], [[str]] -> Root
def make_matrix_from_rows(names, rows):
  columns = [Column(name) for name in names]
  matrix = make_matrix_from_columns(columns)
  for row in rows:
    nodes = matrix.loop_through_circular_list(lambda x: x.right, lambda x: x.add_node_to_column_if_element_present(row))
    nodes = [n for n in nodes if n is not None]
    if len(nodes) > 0:
      current_node = nodes[0]
      for node in nodes:
        current_node.insert_right(node)
        current_node = node
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
