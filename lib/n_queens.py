#! /user/bin/env python

import sys
import lib.exact_cover
 
def queen_symbol():
  return '♕'

def format_board(board):
  return [[queen_symbol() if i else " " for i in row] for row in board]

def n_queens(n):
  solution = solve_n_queens(n)
  return format_board(position_list_to_board(solution, n))

def solve_n_queens(n):
  solutions = get_all_solutions(n)
  i = 1
  return solutions[i] if len(solutions) > i else []

def generate_all_column_headers_and_matchers(n):
  return None

def generate_all_possible_queen_positions_as_rows(n):
  return None

# TODO this ought to be broken up into more separate functions
# int -> [[[str]]] ie array of solutions, each of which is represented as an array of rows
def get_all_solutions(n):
  # TODO I don't like this! col_id shouldn't need to be called in two places
  # some of these diagonals are useless (just one square), oh well
  column_matchers_with_ids = [[column_matcher(m), col_id("col", m)] for m in range(0, n)] + \
                             [[row_matcher(m), col_id("row", m)] for m in range(0, n)] + \
                             [[forward_diag_matcher(m), col_id("f_diag", m)] for m in range(1 - n, n)] + \
                             [[reverse_diag_matcher(m), col_id("r_diag", m)] for m in range(1, 2 * n - 2)]
  col_headers = [item[1] for item in column_matchers_with_ids]
  col_matchers = [item[0] for item in column_matchers_with_ids]
  positions = flatten([[[x, y] for x in range(0, n)] for y in range(0, n)])
  rows = [[matcher(*pos) for matcher in col_matchers if matcher(*pos)] for pos in positions]
  diags = [col_id("f_diag", m) for m in range(1 - n, n)] + [col_id("r_diag", m) for m in range(1 - n, n)] # TODO clean up (this is to allow diagonals to be covered by EITHER 1 or 0 actual queens)
  print("rows below!", file=sys.stderr)
  for r in rows:
    print(r, file=sys.stderr)
  solution_row_sets = lib.exact_cover.find_exact_cover_for_rows(col_headers, rows + diags)
  print("solution row sets below!", file=sys.stderr)
  print(solution_row_sets, file=sys.stderr)
  # TODO stop repeating
  solutions = [[row_to_position(row) for row in row_set if row_to_position(row)] for row_set in solution_row_sets]
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
  return lambda x, y: col_id("r_diag", n_x) if n_x == x + y else None

def col_id(sym, m):
  return ":".join([sym, str(m)])

# [col_id] -> [int, int]
# TODO this is really repetitive
def row_to_position(row):
  if len(row) > 1:
    x = [item.split(":")[1] for item in row if item.split(":")[0] == "col"][0]
    y = [item.split(":")[1] for item in row if item.split(":")[0] == "row"][0]
    return [int(x), int(y)]
  else:
    return None

def position_list_to_board(points, n):
  print("the following list of points is being made into a board", sys.stderr)
  for p in points:
    print(",".join(str(i) for i in p), sys.stderr)
  board = []
  for i in range(0, n):
    board += [[0] * n]
  for point in points:
    x = point[0]
    y = point[1]
    board[y][x] = 1
  print("and the board looks like this:", sys.stderr)
  for r in board:
    print(",".join(str(i) for i in r), sys.stderr)
  return board

# stolen from SO
def flatten(lst):
  return [item for sublist in lst for item in sublist]
