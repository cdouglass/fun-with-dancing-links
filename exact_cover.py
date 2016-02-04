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
    self.column.size += 1

class Column(Node):
  def __init__(self, name):
    self.name   = name
    self.size   = 0
    self.column = self
    Node.__init__(self, self.column)

# Column -> Root
def cover_column(column)
  # removes reference to column from its matrix; does not modify column
  column.left.right = column.right
  column.right.left = column.left
  # for each OTHER node in column, remove that ROW from its surrounding matrix but do NOT modify column's association with it








# [Column] => Root
def make_matrix_from_columns(columns):
  cols = sorted(columns, key = lambda c: c.name) # sorted creates new sorted array; sort modifies in place
  root = Root()
  current = root
  for col in cols:
    current.insert_right(col)
    current = col
  return root

# [str], [[int]] => Root
def make_matrix_from_rows(names, rows):
  columns = [Column(name) for name in names]
  matrix = make_matrix_from_columns(columns)
  for row in rows:
    print("processing row {}".format(row))
    nodes = []
    names_for_row = [names[i] for i in range(0,len(row)) if row[i] != 0]
    col = matrix.right
    n = 0
    while col != matrix:
      if row[n] != 0:
        print("inserted element into column {}".format(col.name))
        node = Node(col)
        col.up.insert_below(node)
        nodes.append(node)
      n += 1
      col = col.right

    if len(nodes) > 0:
      current_node = nodes[0]
      for node in nodes:
        current_node.insert_right(node)
        current_node = node
  return matrix
