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
