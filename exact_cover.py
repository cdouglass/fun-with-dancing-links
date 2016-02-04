#! /usr/bin/env python

from functools import partial

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

class Column(Node):
  def __init__(self, name):
    self.name   = name
    self.size   = 0
    self.column = self
    Node.__init__(self, self.column)

# Operations on matrices

# does NOT apply fn to given node - ONLY to rest in its loop!
# Root, (fn(Root) -> Root), (fn(Root, [Root]) -> T) -> [T]
def loop_through_circular_list(node, move, fn):
  current_node  = move(node)
  visited_nodes = [node]
  results = []
  while current_node != node:
    if current_node is None or current_node in visited_nodes:
      raise InvalidLooping
    results.append(fn(current_node)) # ugh
    visited_nodes.append(current_node)
    current_node = move(current_node)
  return results

# when I define a similar fn as an instance method the side effects don't happen
# Column -> Column (but we care more about side effect on surrounding matrix)
def remove_horizontally(column):
  column.left.right = column.right
  column.right.left = column.left
  return column

# Node -> Node
def remove_vertically(node):
  node.up.down = node.down
  node.down.up = node.up
  node.column.size -= 1
  return node

# Node -> Node
def cover_row(node):
  loop_through_circular_list(node, lambda x: x.right, remove_vertically)
  return(node)

# Column -> Root
def cover_column(column):
  remove_horizontally(column)
  # for each non-top-level node in column, remove that node from matrix
  loop_through_circular_list(column, (lambda x: x.down), cover_row) # removing top to bottom (so must uncover bottom to top)
  return(column)

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

# Iterator, Column -> Node
def add_node_to_column_if_element_present(row_iter, column):
  if next(row_iter) != 0:
    node = Node(column)
    column.up.insert_below(node)
    return node
  else:
    return None

# [str], [[int]] -> Root
def make_matrix_from_rows(names, rows):
  columns = [Column(name) for name in names]
  matrix = make_matrix_from_columns(columns)
  for row in rows:
    nodes = loop_through_circular_list(matrix, (lambda x: x.right), partial(add_node_to_column_if_element_present, iter(row)))
    nodes = [n for n in nodes if n is not None]
    if len(nodes) > 0:
      current_node = nodes[0]
      for node in nodes:
        current_node.insert_right(node)
        current_node = node
  return matrix
