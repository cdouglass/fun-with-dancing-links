#! /usr/bin/env python

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

class Column(Node):
  def __init__(self, name):
    Node.__init__(self, self.column)
    self.name   = name
    self.size   = 0
    self.column = self

# [Column] => Root
def make_matrix_from_columns(columns):
  cols = sorted(columns, key = lambda c: c.name) # sorted creates new sorted array; sort modifies in place
  root = Root.new()
  current = root
  for col in cols:
    current.insert_right(col)
    current = col
  current.insert_right(root)
  return root

# [str], [[int]] => Root
def make_matrix_from_rows(names, rows):
  matrix = make_matrix_from_columns(names.map(lambda x: Column.new(x))) # just column objects so far
  for row in rows:
    nodes = []
    names_for_row = [names[i] for i in range(0,len(row)) if row[i] != 0]
    col = matrix.right
    for name names_for_row:
      if col.name == name:
        node = Node.new(col)
        col.up.insert_below(node)
        nodes.append(node)
    # now that all nodes have been created, link them up
    first_node = nodes[0]
    current_node = nodes[0]
    for node in nodes[1:]:
      current_node.insert_right(node)
      current_node = node
    current_node.insert_right(first_node)
  return matrix
