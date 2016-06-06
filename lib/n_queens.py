import lib.exact_cover
 
def queen_symbol():
  return '♕'

def format_board(board):
  return [[queen_symbol() if i else " " for i in row] for row in board]

# only function here that any outside code should see
def n_queens(n):
  solutions = solve_n_queens(n)
  position_lists = solutions if len(solutions) > 0 else [[]]
  return [format_board(position_list_to_board(pl, n)) for pl in position_lists]

def generate_all_column_headers(n):
  return  [col_id("col", m) for m in range(0, n)] + \
          [col_id("row", m) for m in range(0, n)] + \
          [col_id("f_diag", m) for m in range(1 - n, n)] + \
          [col_id("r_diag", m) for m in range(1, 2 * n - 2)]

# TODO
def generate_all_possible_queen_positions_as_rows(n):
  return None

# TODO this ought to be broken up into more separate functions
# int -> [[[str]]] ie array of solutions, each of which is represented as an array of rows
def solve_n_queens(n):
  # some of these diagonals are useless (just one square), oh well
  col_headers = generate_all_column_headers(n)
  col_matchers = [header_to_matcher(header) for header in col_headers]
  positions = flatten([[[x, y] for x in range(0, n)] for y in range(0, n)])
  rows = [[matcher(*pos) for matcher in col_matchers if matcher(*pos)] for pos in positions]
  diags = [[col_id("f_diag", m)] for m in range(1 - n, n)] + [[col_id("r_diag", m)] for m in range(1, 2 * n - 2)] # TODO clean up (this is to allow diagonals to be covered by EITHER 1 or 0 actual queens)
  solution_row_sets = lib.exact_cover.find_exact_cover_for_rows(col_headers, rows + diags)
  # TODO stop repeating
  solutions = [[row_to_position(row) for row in row_set if row_to_position(row)] for row_set in solution_row_sets]
  return solutions

# TODO if I feed this thingy into the exact cover solver, what pops out is a subset of position rows. they're not directly tagged with position but it can be extracted from the column headers included ("col_1" and "row_3") for instance. but this doesn't feel very clean!
# IMPROVEMENT: add a way to tag rows? might be messy though

def header_to_matcher(header):
  [direction, n] = header.split(":")
  matcher_dict = { "col": column_matcher,
                   "row": row_matcher,
                   "f_diag": forward_diag_matcher,
                   "r_diag": reverse_diag_matcher }
  return matcher_dict[direction](int(n))

# misc helpers
# TODO this is very repetitive
def row_matcher(n):
  return lambda x, y: col_id("col", n) if n == y else None

def column_matcher(n):
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
  # this is getting rows that list two diagonals and nothing else, wtf
  cols = [item.split(":")[1] for item in row if item.split(":")[0] == "col"]
  rows = [item.split(":")[1] for item in row if item.split(":")[0] == "row"]
  if len(cols) > 0 and len(rows) > 0:
    return [int(cols[0]), int(rows[0])]
  else:
    return None

def position_list_to_board(points, n):
  board = []
  for i in range(0, n):
    board += [[0] * n]
  for point in points:
    x = point[0]
    y = point[1]
    board[y][x] = 1
  return board

# stolen from SO
def flatten(lst):
  return [item for sublist in lst for item in sublist]
