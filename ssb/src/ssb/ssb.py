'''
Something Something Bricks

Super Puzzle Fighter clone using pygame.

Created on Dec 20, 2011

@author: Daniel Lo
'''

import pygame
import sys

from brick import DoubleBrick
from brick import Brick
from color import *

def spread_break(stacked_bricks, column_top, col, row, breaker_color, score):
  """
  Break the brick at col, row and recursively call on surrounding bricks.
  Arguments:
    stacked_bricks    Array of brick objects that are stacked
    column_top        Top pixel of each column
    col               Column index to spread break
    row               Row index to spread break
    breaker_color     Color of break to spread
    score             Current score
  """
  # Replace image with a broken brick
  #stacked_bricks[col][row].break_brick()
  stacked_bricks[col][row] = Brick()
  # Decrease top of column      
  column_top[col] += bh  
  # Increment score for each brick destroyed
  score += 10

  # Spread to surrounding blue bricks
  if col > 0 and stacked_bricks[col-1][row].color == breaker_color:
    score = spread_break(stacked_bricks, column_top, col-1, row, breaker_color, score)
  if col < num_cols-1 and stacked_bricks[col+1][row].color == breaker_color:
    score = spread_break(stacked_bricks, column_top, col+1, row, breaker_color, score)
  if row > 0 and stacked_bricks[col][row-1].color == breaker_color:
    score = spread_break(stacked_bricks, column_top, col, row-1, breaker_color, score)
  if row < num_rows-1 and stacked_bricks[col][row+1].color == breaker_color:
    score = spread_break(stacked_bricks, column_top, col, row+1, breaker_color, score)

  return score

def drop_bricks(stacked_bricks, column_top):
  """
  Fill in any empty spaces by moving bricks above down.
  Arguments:
    stacked_bricks    Array of brick objects already stacked
    column_top        Top pixel of each column
  """
  # Handle each column individual
  for col in range(num_cols):
    # For each row, starting from the top
    for row in range(num_rows - 1):
      # If this spot has a brick, and the one below is empty
      if stacked_bricks[col][row].color != black and stacked_bricks[col][row+1].color == black:
        # Move all bricks above down a space, starting from the bottom
        for drop_row in range(row, -1, -1):
          stacked_bricks[col][drop_row].rect.top += bh
          stacked_bricks[col][drop_row + 1] = stacked_bricks[col][drop_row]
        # Create an empty brick at the top
        stacked_bricks[col][0] = Brick()
        
def break_bricks(stacked_bricks, column_top, score):
  """
  Remove any bricks marked as broken.
  Arguments:
    stacked_bricks    Array of brick objects already stacked
    column_top        Top pixel of each column    
    score             Current score
  """
  # Run at least once
  broken = True
  
  # Repeatedly break (combo) until no more breaks to be found
  while broken: 
    # If any bricks were broken
    broken = False
    # Scan through array
    for col in range(num_cols):
      for row in range(num_rows):
        # If breaker is touching a brick with the same color
        if stacked_bricks[col][row].breaker:
          breaker_color = stacked_bricks[col][row].color
          if (col > 0 and stacked_bricks[col-1][row].color == breaker_color) or \
            (col < num_cols-1 and stacked_bricks[col+1][row].color == breaker_color) or \
            (row > 0 and stacked_bricks[col][row-1].color == breaker_color) or \
            (row < num_rows-1 and stacked_bricks[col][row+1].color == breaker_color):
            # Use spread_break to recursively break proper bricks
            score = spread_break(stacked_bricks, column_top, col, row, breaker_color, score)
            # Play sound for breaking bricks
            snd_break.play()
            # Bricks have been broken
            broken = True
          
    # Collapse bricks from above if any bricks were broken
    if broken:
      # Drop bricks to fill up space
      drop_bricks(stacked_bricks, column_top)
      
  return score

## Size parameters  
# number of rows and columns in play area
num_rows = 14
num_cols = 6
# Column to generate bricks in (0 indexed)
gen_col = 3
# Block width, used to space out objects
block_size = bw, bh = (32, 32)
# Min, max position of block's left edge
max_pos_x = bw*num_cols;
min_pos_x = bw;
# Lowest/highest position of block's top edge
max_pos_y = bh*num_rows;
min_pos_y = bh;

## Pygame initialization
# Reduce sound buffer size (4096 to 512) to reduce lag
pygame.mixer.pre_init(44100, -16, 2, 512)
# Initialize Pygame    
pygame.init()
# Window size
size = width, height = (num_cols+2)*2*bw, (num_rows+2)*bh
# Initialize window
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Something Something Bricks')

# Clock for keeping track of fps
fps_clock = pygame.time.Clock()

# Possible brick colors
brick_colors = [red, blue, green, yellow]
# Brick fall speed
fallspeed_slow = 1
fallspeed_fast = 10
fallspeed = fallspeed_slow

# Create first brick
db = DoubleBrick(brick_colors, ((gen_col+1)*bw, bh), block_size)
bricks_list = [db]
# First brick in pair 
b1 = db.brick1
# Second brick in pair
b2 = db.brick2

## Game state
# keep track of top of each column
column_top = [max_pos_y]*num_cols
# Array keeping track of stacked bricks (column from left, row from top)
stacked_bricks = [0]*num_cols
for i in range(num_cols):
  stacked_bricks[i] = [Brick()]*num_rows
# Initialize score
score = 0
# Font object for rendering text
font_obj = pygame.font.Font(None, 28)
  
## Sounds
# Directory where sounds are kept
snd_dir = "../../sounds/"
# Sound for key press
snd_key = pygame.mixer.Sound(snd_dir + "select.wav")
# Sound for bricks broken
snd_break = pygame.mixer.Sound(snd_dir + "break.wav")
# Sound when brick reaches bottom
snd_drop = pygame.mixer.Sound(snd_dir + "drop.wav")
# Background music
#snd_background = pygame.mixer.Sound(snd_dir + "fkobbe-121111final.wav")
#snd_background.play(loops=-1)
  
# Screen shot counter
screen_shot_count = 0

# Main loop
while True:
    
  # Which column the falling block is in
  col_index1 = b1.rect.left/bw - 1
  col_index2 = b2.rect.left/bw - 1
  # Edges of brick pair
  # Note these aren't strictly the pixel edges. The right and bottom are actually shifted in by bw, bh respectively.
  left_edge = min(b1.rect.left, b2.rect.left)
  top_edge = min(b1.rect.top, b2.rect.top)
  bottom_edge = max(b1.rect.top, b2.rect.top)
  right_edge = max(b1.rect.left, b2.rect.left)
    
  # Event Handler
  for event in pygame.event.get():
    # Keypresses
    if event.type == pygame.KEYDOWN:
      # Quit game
      if event.key == pygame.K_ESCAPE:
        sys.exit()
        
      # Move brick left (subtract from x coordinate)
      elif event.key == pygame.K_LEFT:
        # Bound by left edge
        if left_edge > min_pos_x and bottom_edge < column_top[col_index1-1] and top_edge < column_top[col_index2-1]:
          b1.rect.left -= bw
          b2.rect.left -= bw
          snd_key.play()
        
      # Move brick right (add to x coordinate)
      elif event.key == pygame.K_RIGHT:
        # Bound by right edge
        if right_edge < max_pos_x and bottom_edge < column_top[col_index1+1] and top_edge < column_top[col_index2+1]:
          b1.rect.left += bw
          b2.rect.left += bw
          snd_key.play()
        
      # Increased fall speed when DOWN is held
      elif event.key == pygame.K_DOWN:
        fallspeed = fallspeed_fast
        
      # On rotation, always first (top) brick that moves
      # Rotate clockwise
      elif event.key == pygame.K_e:
        # If first brick above second
        if b1.rect.top < b2.rect.top and right_edge < max_pos_x and bottom_edge < column_top[col_index1 + 1]:
          b1.rect.top += bh
          b1.rect.left += bw
          snd_key.play()
        # first brick below second
        elif b1.rect.top > b2.rect.top and left_edge > min_pos_x and top_edge < column_top[col_index1 - 1]:
          b1.rect.top -= bh
          b1.rect.left -= bw
          snd_key.play()  
        # first brick to the right of the second
        elif b1.rect.left > b2.rect.left and bottom_edge + bh < column_top[col_index1 -1]:
          b1.rect.top += bh
          b1.rect.left -= bw
          snd_key.play()
        # first brick to the left of the second
        elif b1.rect.left < b2.rect.left:
          b1.rect.top -= bh
          b1.rect.left += bw
          snd_key.play()
      # Rotate counter-clockwise
      elif event.key == pygame.K_q:
        # If first brick above second
        if b1.rect.top < b2.rect.top and left_edge > min_pos_x and bottom_edge < column_top[col_index1 - 1]:
          b1.rect.top += bh
          b1.rect.left -= bw
          snd_key.play()
        # first brick below second
        elif b1.rect.top > b2.rect.top and right_edge < max_pos_x and top_edge < column_top[col_index1 + 1]:
          b1.rect.top -= bh
          b1.rect.left += bw
          snd_key.play()
        # first brick to the right of the second
        elif b1.rect.left > b2.rect.left:
          b1.rect.top -= bh
          b1.rect.left -= bw
          snd_key.play()
        # first brick to the left of the second
        elif b1.rect.left < b2.rect.left and bottom_edge + bh < column_top[col_index1 + 1]:
          b1.rect.top += bh
          b1.rect.left += bw
          snd_key.play()     
        
      # Save a screen cap when I is pressed
      elif event.key == pygame.K_i:
        pygame.image.save(screen, "screenshot_%d.png" % screen_shot_count)
        screen_shot_count += 1
        
    elif event.type == pygame.KEYUP:
      # Decrease fall speed once DOWN is released
      if event.key == pygame.K_DOWN:
        fallspeed = fallspeed_slow
    # Quit game
    elif event.type == pygame.QUIT:
      sys.exit()
      
    # Update column indices after any possible key presses
    # Which column the falling block is in
    col_index1 = b1.rect.left/bw - 1
    col_index2 = b2.rect.left/bw - 1
    # Edges of brick pair
    # Note these aren't strictly the pixel edges.
    # The right and bottom are actually shifted in by bw, bh respectively.
    left_edge = min(b1.rect.left, b2.rect.left)
    top_edge = min(b1.rect.top, b2.rect.top)
    bottom_edge = max(b1.rect.top, b2.rect.top)
    right_edge = max(b1.rect.left, b2.rect.left)
    
  # Blank screen
  screen.fill(black)
  
  ## Write score
  # String for score information
  score_msg = "Score: %d" % score
  # Surface containing score text
  score_surface = font_obj.render(score_msg, True, white)
  # Create rect object to specify where to place text
  score_rect = score_surface.get_rect()
  score_rect.topleft = (max_pos_x + 2*bw, 2*bh)
  screen.blit(score_surface, score_rect)
  
  # Draw walls
  pygame.draw.line(screen, white, (bw, bh), (bw, (num_rows+1)*bh), 1)
  pygame.draw.line(screen, white, (bw, (num_rows+1)*bh), ((num_cols+1)*bw, (num_rows+1)*bh), 1)
  pygame.draw.line(screen, white, ((num_cols+1)*bw, bh), ((num_cols+1)*bw, (num_rows+1)*bh), 1)
  # Generation line
  pygame.draw.line(screen, white, (bw, bh), ((num_cols+1)*bw, bh))
  # Game over line
  pygame.draw.line(screen, gray, (bw, 2*bh), ((num_cols+1)*bw, 2*bh))
  """
  # Draw vertical grid lines
  for x in range(5):
    pygame.draw.line(screen, gray, ((2+x)*bw, bh), ((2+x)*bw, 21*bh), 1)
  # Draw horizontal grid lines
  for y in range(19):
    pygame.draw.line(screen, gray, (bw, (2+y)*bh), (7*bw, (2+y)*bh), 1)
  """

  # If the brick pair hasn't reached the bottom,
  if b1.rect.top < column_top[col_index1] - fallspeed and \
    b2.rect.top < column_top[col_index2] - fallspeed:
    # Drop bricks
    b1.rect.top += fallspeed
    b2.rect.top += fallspeed
  # Else one of the bricks has reached the top of a column
  # In this case, both bricks are dropped
  else:
    # Sound for brick reaching bottom
    snd_drop.play()
    
    # Brick that hits a surface first needs to handled first (in case stacked)
    # Set the one that hits first as b1
    if b2.rect.top >= column_top[col_index2] - fallspeed:
      b2, b1 = b1, b2
      col_index1, col_index2 = col_index2, col_index1
    else:
      # Don't need to do anything, but check that other brick has hit
      assert(b1.rect.top >= column_top[col_index1] - fallspeed)
    # Drop bottom brick to bottom
    b1.rect.top = column_top[col_index1]
    
    # Update top position of the column
    column_top[col_index1] -= bh
    # Now the other brick
    b2.rect.top = column_top[col_index2]
    column_top[col_index2] -= bh
    # Save to array
    stacked_bricks[b1.get_col_index()][b1.get_row_index()] = b1
    stacked_bricks[b2.get_col_index()][b2.get_row_index()] = b2
    
    # Handle breaking and update score
    score = break_bricks(stacked_bricks, column_top, score)
    
    # Create new brick
    db = DoubleBrick(brick_colors, ((gen_col+1)*bw, bh), block_size)
    # Add to list of existing bricks
    bricks_list.append(db)
    # First brick in pair 
    b1 = db.brick1
    # Second brick in pair
    b2 = db.brick2
    
  # Draw falling brick
  screen.blit(b1.image, b1.rect)
  screen.blit(b2.image, b2.rect)
  # Draw stacked bricks
  for col in range(num_cols):
    for row in range(num_rows):
      screen.blit(stacked_bricks[col][row].image, stacked_bricks[col][row].rect)
      
  # Check for game over condition
  if column_top[gen_col] < 3*bh:
    ## Write Game Over to screen
    # String for score information
    gameover_msg = "Game Over"
    # Surface containing game over text
    gameover_surface = font_obj.render(gameover_msg, True, white)
    # Create rect object to specify where to place text
    gameover_rect = gameover_surface.get_rect()
    gameover_rect.topleft = (max_pos_x + 2*bw, 4*bh)
    screen.blit(gameover_surface, gameover_rect)
    pygame.display.update()
    
    # Delay 5 seconds, and then exit game
    pygame.time.delay(5000)
    sys.exit()

  # Refresh display
  pygame.display.update()    
  # Ensure 60 FPS
  fps_clock.tick(60)
  # print fps_clock.get_fps()
  