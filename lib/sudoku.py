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

# TODO test
def merge_boards(a, b):
  board = empty_board()
  for x, y in all_positions():
    board[y][x] = a[y][x] or b[y][x]
  return board

def find_n_solutions(board, n):
  matrix = board_to_matrix(board)
  solutions = []
  lib.exact_cover.find_n_exact_covers(matrix, n, solutions)
 # not using find_exact_cover_for_rows as with n_queens so result is in different format - array of nodes, not of header lists
  solutions_as_row_lists = [[node.get_column_names_for_row() for node in soln] for soln in solutions]
  solved_boards = [merge_boards(board, row_list_to_board(soln)) for soln in solutions_as_row_lists]
  return solved_boards

def random_clue_set(n = 25):
  matrix = board_to_matrix(empty_board())
  partial_board_row_list = [node.get_column_names_for_row() for node in lib.exact_cover.find_partial_cover(matrix, n)] # TODO pull out method for this
  return row_list_to_board(partial_board_row_list)

def random_empty_coords(board):
  y = random.choice([i for i in range(0, len(board)) if None in board[i]])
  x = random.choice([i for i in range(0, len(board)) if board[y][i] == None])
  return [x, y]

# currently takes about 1:15
def generate_clue_set():
  clues = []
  solutions = []
  while len(solutions) != 1:
    clues = random_clue_set(25)
    solutions = find_n_solutions(clues, 2) # only need to know existence and uniqueness
    while len(solutions) > 1:
      goal = solutions[0] 
      x, y = random_empty_coords(clues)
      clues[y][x] = goal[y][x] # TODO covering this way is silly - why not stay as matrix all along?
      solutions = find_n_solutions(clues, 2)
  return [clues, solutions[0]]
