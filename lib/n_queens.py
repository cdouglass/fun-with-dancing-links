# TODO have this return an actual solution

def queen_symbol():
  return '♕'

def n_queens(n):
  result = []
  for i in range(n):
    row = []
    for j in range(n):
      if (i == j):
        row.append(queen_symbol())
      else:
        row.append(' ')
    result.append(row)
  return result
