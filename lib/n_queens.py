import lib.exact_cover
 
# only function here that any outside code should see
def n_queens(n):
  solutions = solve_n_queens(n)
  position_lists = solutions if len(solutions) > 0 else []
  return [position_list_to_board(pl, n) for pl in position_lists]

def organ_pipe_ordering(n):
  low = 0
  high = n - 1
  order = []
  while low <= high:
    order.append(low)
    order.append(high)
    low += 1
    high -= 1
  order.reverse()
  return order

def generate_all_column_headers(n):
  diagonals = [col_id("f_diag", m) for m in range(1 - n, n)] + \
              [col_id("r_diag", m) for m in range(1, 2 * n - 2)]
  rows_and_columns = []
  for m in organ_pipe_ordering(n):
    rows_and_columns.append(col_id("col", m))
    rows_and_columns.append(col_id("row", m))
  return rows_and_columns + diagonals

def generate_all_positions_as_rows(n):
  return flatten([[[x, y] for x in range(0, n)] for y in range(0, n)])

# int -> [[[str]]] ie array of solutions, each of which is represented as an array of rows
def solve_n_queens(n):
  col_headers = generate_all_column_headers(n)
  col_matchers = [header_to_matcher(header) for header in col_headers]
  positions = generate_all_positions_as_rows(n)
  rows = [[matcher(*pos) for matcher in col_matchers if matcher(*pos)] for pos in positions]
  diags = [[col_id("f_diag", m)] for m in range(1 - n, n)] + [[col_id("r_diag", m)] for m in range(1, 2 * n - 2)]
  solution_row_sets = lib.exact_cover.find_exact_cover_for_rows(col_headers, rows + diags)
  return [[row_to_position(row) for row in row_set if row_to_position(row)] for row_set in solution_row_sets]

def header_to_matcher(header):
  [direction, n] = header.split(":")
  matcher_dict = { "col": column_matcher,
                   "row": row_matcher,
                   "f_diag": forward_diag_matcher,
                   "r_diag": reverse_diag_matcher }
  return matcher_dict[direction](int(n))

# misc helpers
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
def row_to_position(row):
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
