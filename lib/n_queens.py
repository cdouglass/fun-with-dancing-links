#! /user/bin/env python

import sys
import lib.exact_cover
 
def queen_symbol():
  return '♕'

def format_board(board):
  return [[queen_symbol() if i else " " for i in row] for row in board]

def n_queens(n):
  solution = solve_n_queens(n)
  return format_board(solution)

# TODO real solution
def solve_n_queens(n):
  return get_all_solutions(n)[0]

# TODO this ought to be broken up into more separate functions
# int -> [[[str]]] ie array of solutions, each of which is represented as an array of rows
def get_all_solutions(n):
  # TODO I don't like this! col_id shouldn't need to be called in two places
  # some of these diagonals are useless (just one square), oh well
  column_matchers_with_ids = [[column_matcher(m), col_id("col", m)] for m in range(0, n)] + \
                             [[row_matcher(m), col_id("row", m)] for m in range(0, n)] + \
                             [[forward_diag_matcher(m), col_id("f_diag", m)] for m in range(-n, n)] + \
                             [[reverse_diag_matcher(m), col_id("r_diag", m)] for m in range(-n, n)]
  col_headers  = [item[1] for item in column_matchers_with_ids]
  col_matchers = [item[0] for item in column_matchers_with_ids]
  positions = flatten([[[x, y] for x in range(0, n)] for y in range(0, n)])
  print("positions below!", file=sys.stderr)
  print(positions, file=sys.stderr)
  rows = [[matcher(*pos) for matcher in col_matchers if matcher(*pos)] for pos in positions]
  print("rows below!", file=sys.stderr)
  for r in rows:
    print(r, file=sys.stderr)
  #solution_row_sets = lib.exact_cover.find_exact_cover_for_rows(col_headers, rows)
  # TODO is it a problem that headers are not strings?
  solution_row_sets = lib.exact_cover.find_exact_cover_for_rows([str(h) for h in col_headers], rows)
  print("solution row sets below!", file=sys.stderr)
  print(solution_row_sets, file=sys.stderr)
  solutions = [[row_to_position(row) for row in row_set] for row_set in solution_row_sets]
  return solutions

# TODO if I feed this thingy into the exact cover solver, what pops out is a subset of position rows. they're not directly tagged with position but it can be extracted from the column headers included ("col_1" and "row_3") for instance. but this doesn't feel very clean!


# misc helpers
# TODO this is very repetitive
def column_matcher(n):
  return lambda x, y: col_id("col", n) if n == y else None

def row_matcher(n):
  return lambda x, y: col_id("row", n) if n == x else None

# x-intercept
def forward_diag_matcher(n_x):
  return lambda x, y: col_id("f_diag", n_x) if n_x  == x - y else None

def reverse_diag_matcher(n_x):
  return lambda x, y: col_id("r_diag", n_x) if n_x == y - x else None

def col_id(sym, n1, n2=None):
  return [sym, n1, n2]

# [col_id] -> [int, int]
def row_to_position(row):
  x = (item[1] for item in row if item[0] == "col").next()
  y = (item[1] for item in row if item[0] == "row").next()
  return [x, y]

# stolen from SO
def flatten(lst):
  return [item for sublist in lst for item in sublist]
