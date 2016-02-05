#! /usr/bin/env python
import pygame

# display-related constants
BLACK = 0, 0, 0
GRAY = 200, 200, 200
WHITE = 255, 255, 255

BG_COLOR   = WHITE
TEXT_COLOR = BLACK
BOX_COLOR  = GRAY

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 405

TOP_MARGIN = 100
LEFT_MARGIN = 20
LARGE_BOX_WIDTH = 365
MED_BOX_WIDTH = 120
SMALL_BOX_WIDTH = 35
GUTTER_WIDTH = 5

pygame.init() # is this necessary?
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock() # maintain fixed frame rate

font_obj = pygame.font.SysFont('Lucida', 40)
title_surface = font_obj.render('Sudoku!', True, TEXT_COLOR) # True -> use antialiasing for text
title_box = title_surface.get_rect()
title_box.center = (200, 50)
title_surface.convert()

background = pygame.Surface(screen.get_size())
background.fill(BG_COLOR)

def box_positions():
  y = TOP_MARGIN + GUTTER_WIDTH
  positions = []
  for i in range(1, 10):
    x = LEFT_MARGIN + GUTTER_WIDTH
    for i in range(1, 10):
      positions.append((x, y))
      x += SMALL_BOX_WIDTH + GUTTER_WIDTH
    y += SMALL_BOX_WIDTH + GUTTER_WIDTH
  return(positions)

def draw_blank_board():
  x = LEFT_MARGIN
  y = TOP_MARGIN
  pygame.draw.rect(background, TEXT_COLOR, (x, y, LARGE_BOX_WIDTH, LARGE_BOX_WIDTH), 0)
  for i in box_positions():
    pygame.draw.rect(background, BOX_COLOR, (i[0], i[1], SMALL_BOX_WIDTH, SMALL_BOX_WIDTH), 0) # last arg is line thickness

draw_blank_board()
background = background.convert() # store surface in memory for faster painting. if using transparency, would use .convert_alpha() instead

def draw_numbers():
  return None
  

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

  screen.blit(background, (0, 0)) # coords give position of upper left corner of background surface
  screen.blit(title_surface, title_box)

  pygame.display.update()
