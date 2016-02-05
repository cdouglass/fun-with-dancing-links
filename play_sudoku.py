#! /usr/bin/env python
import pygame
import sudoku

# display-related constants
BLACK = 0, 0, 0
GRAY = 200, 200, 200
WHITE = 255, 255, 255

BG_COLOR   = WHITE
TEXT_COLOR = BLACK
BOX_COLOR  = GRAY

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 381

TOP_MARGIN = 100
LEFT_MARGIN = 20
LARGE_BOX_WIDTH = 341
SMALL_BOX_WIDTH = 35
GUTTER_WIDTH = 2

pygame.init() # is this necessary?
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock() # maintain fixed frame rate

title_font = pygame.font.SysFont('Sans', 40)
title_surface = title_font.render('Sudoku!', True, TEXT_COLOR) # True -> use antialiasing for text
title_box = title_surface.get_rect()
title_box.center = (200, 50)
title_surface.convert()

main_font = pygame.font.SysFont('Helvetica', 30)

background = pygame.Surface(screen.get_size())
background.fill(BG_COLOR)

def boxes(box_width, box_num, grouping):
  y = TOP_MARGIN + 2 * GUTTER_WIDTH
  boxes = []
  for i in range(1, box_num + 1):
    x = LEFT_MARGIN + 2 * GUTTER_WIDTH
    for j in range(1, box_num + 1):
      boxes.append(pygame.Rect(x, y, box_width, box_width))
      x += box_width + GUTTER_WIDTH
      if j % grouping == 0:
        x += GUTTER_WIDTH / 2
    y += box_width + GUTTER_WIDTH
    if i % grouping == 0:
      y += GUTTER_WIDTH / 2
  return(boxes)

small_boxes = boxes(SMALL_BOX_WIDTH, 9, 3)

def draw_blank_board():
  x = LEFT_MARGIN
  y = TOP_MARGIN
  pygame.draw.rect(background, TEXT_COLOR, (x, y, LARGE_BOX_WIDTH, LARGE_BOX_WIDTH), 0)
  for i in small_boxes:
    pygame.draw.rect(background, BOX_COLOR, i, 0) # last arg is line thickness - 0 means fill box instead of drawing outline

draw_blank_board()
background = background.convert() # store surface in memory for faster painting. if using transparency, would use .convert_alpha() instead

# pygame can't draw text on an existing surface, must create new one
def blit_numbers(board):
  for (index, box) in enumerate(small_boxes): # i is a tuple (position, index)
    number = board[index]
    if number != 0:
      box_center = box.center
      number_surface = main_font.render(str(number), True, TEXT_COLOR)
      surface_box = number_surface.get_rect()
      surface_box.center = box_center
      screen.blit(number_surface, surface_box)
  
board = sudoku.get_board()
mainloop = True

while mainloop == True:
  clock.tick(30)

  # process any events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      mainloop = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        mainloop = False # allows nicer teardown than sys.exit()
      elif event.key == pygame.K_n: # TODO button-click instead
        board = sudoku.get_board()

  screen.blit(background, (0, 0)) # coords give position of upper left corner of background surface
  screen.blit(title_surface, title_box)
  blit_numbers(board)

  pygame.display.update()
