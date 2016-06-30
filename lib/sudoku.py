import random
import lib.exact_cover
from lib.n_queens import flatten

class InvalidBoard(Exception):
  pass

def empty_board():
  board = []
  for i in range(1, 10):
    row = []
    for j in range(1, 10):
      row.append(None)
    board.append(row)
  return board

def subgrid(x, y, board):
  x_min, y_min = [3 * (i // 3) for i in [x, y]]
  return [[val for val in row[x_min:x_min + 3]] for row in board[y_min:y_min + 3]]

def allowed_values_at_coords(x, y, board):
  row = [val for i, val in enumerate(board[y]) if i != x]
  col = [r[x] for i, r in enumerate(board) if i != y]
  sg = subgrid(x, y, board)
  sg[y % 3][x % 3] = None 
  subgrid_values = flatten(sg)
  taken_values = {v for v in row} | {v for v in col} | {v for v in subgrid_values}
  return {i for i in range(1,10) if i not in taken_values}

def all_positions():
  return flatten([[[x, y] for x in range(0, 9)] for y in range(0, 9)])

def make_header(kind, digit, index):
  return "-".join([str(digit), kind, str(index)])

def column_headers():
  random.seed(20) # TODO remove
  secondary_headers = [make_header("cell", x, y) for x, y in all_positions()]
  primary_headers = []
  for kind in ["row", "col", "subgrid"]:
    for digit in range(1, 10):
      for index in range(0, 9):
        primary_headers.append(make_header(kind, digit, index))
  return [primary_headers, secondary_headers]

def make_matrix_row_for_move(x, y, digit):
  subgrid_index = 3 * (y // 3) + x // 3
  return [make_header(kind, digit, index) for kind, index in [["row", y], ["col", x], ["subgrid", subgrid_index]]] + [make_header("cell", x, y)]

def board_to_matrix(board):
  all_coords = all_positions()
  free_coords = [[x, y] for x, y in all_coords if board[y][x] == None]
  filled_coords = [[x, y] for x, y in all_coords if board[y][x] != None]
  primary_headers, secondary_headers = column_headers()
  possible_rows = flatten([[make_matrix_row_for_move(x, y, digit) for digit in allowed_values_at_coords(x, y, board)] for x, y in free_coords])
  filled_columns = flatten([make_matrix_row_for_move(x, y, board[y][x]) for x, y in filled_coords])
  available_columns = [header for header in primary_headers if header not in filled_columns]
  matrix = lib.exact_cover.make_matrix_from_rows(possible_rows, available_columns, secondary_headers)
  return matrix

# TODO test
def nodes_to_board(nodes):
  board = empty_board()
  rows = [node.get_column_names_for_row() for node in nodes]
  for row in rows:
    cell_header = [header for header in row if "cell" in header][0]
    row_header = [header for header in row if "row" in header][0]
    x = int(cell_header.split("-")[0])
    y = int(cell_header.split("-")[2])
    digit = int(row_header.split("-")[0])
    board[y][x] = digit
  return board

# TODO test
def generate_clue_set():
  matrix = board_to_matrix(empty_board())
  clues, solution = [nodes_to_board(lst) for lst in lib.exact_cover.find_random_partial_cover_with_unique_solution(matrix)]
  return [clues, solution]
