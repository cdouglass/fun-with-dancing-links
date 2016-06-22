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

def add_random_clue(board):
  try:
    y = random.choice([i for i in range(0, len(board)) if None in board[i]])
    x = random.choice([i for i in range(0, len(board)) if board[y][i] == None])
    options = allowed_values_at_coords(x, y, board)
    board[y][x] = random.choice(list(options))
  except(IndexError):
    raise InvalidBoard

def random_clue_set():
  count = 0
  board = empty_board()
  while count < 25:
    try:
      add_random_clue(board)
      count += 1
    except(InvalidBoard):
      count = 0
      board = empty_board()
  return board

def all_positions():
  return flatten([[[x, y] for x in range(0, 9)] for y in range(0, 9)])

def make_header(kind, digit, index):
  return "-".join([str(digit), kind, str(index)])

def column_headers():
  headers = [make_header("cell", x, y) for x, y in all_positions()] # TODO x isn't a digit, not good naming
  for digit in range(1, 10):
    for index in range(0, 9):
      for kind in ["row", "col", "subgrid"]:
        headers.append(make_header(kind, digit, index))
  return headers

def make_matrix_row_for_move(x, y, digit):
  subgrid_index = 3 * (y // 3) + x // 3
  return [make_header(kind, digit, index) for kind, index in [["row", y], ["col", x], ["subgrid", subgrid_index]]] + [make_header("cell", x, y)]

def board_to_matrix(board):
  all_coords = all_positions()
  free_coords = [[x, y] for x, y in all_coords if board[y][x] == None]
  filled_coords = [[x, y] for x, y in all_coords if board[y][x] != None]
  possible_rows = flatten([[make_matrix_row_for_move(x, y, digit) for digit in allowed_values_at_coords(x, y, board)] for x, y in free_coords])
  filled_columns = flatten([make_matrix_row_for_move(x, y, board[y][x]) for x, y in filled_coords])
  available_columns = [header for header in column_headers() if header not in filled_columns]
  matrix = lib.exact_cover.make_matrix_from_rows(possible_rows, available_columns)
  return matrix

def row_list_to_board(rows):
  board = empty_board()
  for row in rows: # this is giving nodes. i want headers. hmph.
    cell_header = [header for header in row if "cell" in header][0]
    row_header = [header for header in row if "row" in header][0]
    x = int(cell_header.split("-")[0])
    y = int(cell_header.split("-")[2])
    digit = int(row_header.split("-")[0])
    board[y][x] = digit
  return board

def find_all_solutions(board):
  matrix = board_to_matrix(board)
  solutions = []
  lib.exact_cover.find_exact_cover(matrix, solutions)
 # not using find_exact_cover_for_rows as with n_queens so result is in different format - array of nodes, not of header lists
  solutions_as_row_lists = [[node.get_column_names_for_row() for node in soln] for soln in solutions]
  solved_boards = [row_list_to_board(soln) for soln in solutions_as_row_lists]
  # TODO this yields a solution in an improper form, with None in place of all givens
  return solved_boards

def generate_clue_set():
  clues = [[5,    3,    None, None, 7,    None, None, None, None],
           [6,    None, None, 1,    9,    5,    None, None, None],
           [None, 9,    8,    None, None, None, None, 6,    None],
           [8,    None, None, None, 6,    None, None, None, 3],
           [4,    None, None, 8,    None, 3,    None, None, 1],
           [7,    None, None, None, 2,    None, None, None, 6],
           [None, 6,    None, None, None, None, 2,    8,    None],
           [None, None, None, 4,    1,    9,    None, None, 5],
           [None, None, None, None, 8,    None, None, 7,    9]]
  solution = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
              [6, 7, 2, 1, 9, 5, 3, 4, 8],
              [1, 9, 8, 3, 4, 2, 5, 6, 7],
              [8, 5, 9, 7, 6, 1, 4, 2, 3],
              [4, 2, 6, 8, 5, 3, 7, 9, 1],
              [7, 1, 3, 9, 2, 4, 8, 5, 6],
              [9, 6, 1, 5, 3, 7, 2, 8, 4],
              [2, 8, 7, 4, 1, 9, 6, 3, 5],
              [3, 4, 5, 2, 8, 6, 1, 7, 9]]
  return [clues, solution]
