'''
Object to keep track of the board (stacked bricks) game state.

Created on Dec 22, 2011

@author: Dan
'''

import pygame
import math

from brick import Brick
from brick import DoubleBrick
from color import *

class Board:
  """
  Class for play area (stacked bricks).
  """
  
  # Possible brick colors (R, G, B) triplets
  _brick_colors = [red, green, blue, yellow]
  
  # Brick fallspeed (pixels per loop iteration)
  _fallspeed_slow = 1
  _fallspeed_fast = 10
  
  def __init__(self, board_size, brick_size, mixer):
    """
    Default constructor.
    Arguments:
      board_size    number of (columns, rows)
      brick_size    (x, y) pixel size of each brick
      mixer         Pygame mixer object for sound output.
    """
    # Save parameters
    self.num_cols, self.num_rows = self.board_size = board_size
    self.bw, self.bh = self.brick_size = brick_size
    # Column where bricks are spawned (0 indexed)
    self.gen_col = int(math.ceil(self.num_cols/2))
    # Top left corner (pixels) of game board
    self.top, self.left = self.topleft = (self.bw, self.bh)
    # Min, max possible values for brick topleft corner
    self.min_pos_x = self.left
    self.max_pos_x = self.left + self.bw * (self.num_cols - 1)
    self.min_pos_y = self.top
    self.max_pos_y = self.top + self.bh * (self.num_rows - 1)
    
    # Create array of stacked bricks
    self.clear_board()
      
    # Current dropping brick pair
    self.db = None
    
    ## Sounds
    # Directory where sounds are kept
    snd_dir = "../../sounds/"
    # Sound for key press
    self.snd_key = mixer.Sound(snd_dir + "select.wav")
    # Sound for bricks broken
    self.snd_break = mixer.Sound(snd_dir + "break.wav")
    # Sound when brick reaches bottom
    self.snd_drop = mixer.Sound(snd_dir + "drop.wav")
  
  def start(self):
    """
    Reset game state and start new game.
    """
    # Reset game board
    self.clear_board()
    # Drop a new brick
    self.create_brick()    
      
  def clear_board(self):
    """
    Reset game board to all blank bricks and reset all state.
    """
    # Blank all brick spaces
    self.stacked_bricks = [0]*self.num_cols
    for col in range(self.num_cols):
      self.stacked_bricks[col] = [Brick()]*self.num_rows
    # Reset fallspeed
    self.fallspeed = self._fallspeed_slow
    # Reset score
    self.score = 0
      
  def create_brick(self):
    """
    Create a new dropping brick.
    """
    # Create a dropping brick pair
    self.db = DoubleBrick(self._brick_colors, (self.gen_col*self.bw + self.top, self.topleft[1]), self.brick_size)
  
  def col_top(self, col):
    """
    Return the top brick in column col that is not empty.
    Arguments:
      col    column to return top brick of.
    """
    for row in range(self.num_rows):
      if not self.stacked_bricks[col][row].empty():
        return self.stacked_bricks[col][row]
    # If no brick's found
    return None
      
  def col_pix_top(self, col):
    """
    Return top pixel of first (bottom) brick in column col that is empty.
    Arguments:
      col    column to return top pixel of.
    """
    if self.col_top(col):
      return self.col_top(col).rect.top - self.bh
    # No bricks found
    else:
      # Return bottom edge
      return self.max_pos_y
      
  def b1(self):
    """
    Return first (originally top) brick.
    """
    if self.db:
      return self.db.brick1
    else:
      return None
  
  def b2(self):
    """
    Return second (originally bottom) brick.
    """
    if self.db:
      return self.db.brick2
    else:
      return None
  
  def b1_col(self):
    """
    Column of first (originally top) brick.
    """
    return (self.b1().rect.left - self.left)/self.bw

  def b2_col(self):
    """
    Column of second (originally bottom) brick.
    """
    return (self.b2().rect.left - self.left)/self.bw
  
  def move_left(self):
    """
    Move dropping brick to the left.
    """
    if self.db and not self.game_over():
      # Check that there is space on the left
      if self.db.left_edge() > self.min_pos_x and \
        self.db.bottom_edge() < self.col_pix_top(self.b1_col() - 1) and \
        self.db.top_edge() < self.col_pix_top(self.b2_col() - 1):
        # Move both bricks to the left
        self.b1().rect.left -= self.bw
        self.b2().rect.left -= self.bw
        self.snd_key.play()
        
  def move_right(self):
    """
    Move dropping brick to the right.
    """
    if self.db and not self.game_over():
      # Check that there is space on the right
      if self.db.right_edge() < self.max_pos_x and \
        self.db.bottom_edge() < self.col_pix_top(self.b1_col() + 1) and \
        self.db.top_edge() < self.col_pix_top(self.b2_col() + 1):
        self.b1().rect.left += self.bw
        self.b2().rect.left += self.bw
        self.snd_key.play()
  
  def rotate_cw(self):
    """
    Rotate first (originally top) brick clockwise around second brick.
    """
    if self.db and not self.game_over():
      # If first brick above second
      if self.b1().rect.top < self.b2().rect.top and \
        self.db.right_edge() < self.max_pos_x and self.db.bottom_edge() < self.col_pix_top(self.b1_col() + 1):
        self.b1().rect.top += self.bh
        self.b1().rect.left += self.bw
        self.snd_key.play()
      # first brick below second
      elif self.b1().rect.top > self.b2().rect.top and \
        self.db.left_edge() > self.min_pos_x and self.db.top_edge() < self.col_pix_top(self.b1_col() - 1):
        self.b1().rect.top -= self.bh
        self.b1().rect.left -= self.bw
        self.snd_key.play()  
      # first brick to the right of the second
      elif self.b1().rect.left > self.b2().rect.left and \
        self.db.bottom_edge() + self.bh < self.col_pix_top(self.b1_col() - 1):
        self.b1().rect.top += self.bh
        self.b1().rect.left -= self.bw
        self.snd_key.play()
      # first brick to the left of the second
      elif self.b1().rect.left < self.b2().rect.left:
        self.b1().rect.top -= self.bh
        self.b1().rect.left += self.bw
        self.snd_key.play()
  
  def rotate_ccw(self):
    """
    Rotate first (originally top) brick counter-clockwise around second brick.
    """
    if self.db and not self.game_over():
      # If first brick above second
      if self.b1().rect.top < self.b2().rect.top and \
        self.db.left_edge() > self.min_pos_x and self.db.bottom_edge() < self.col_pix_top(self.b1_col() - 1):
        self.b1().rect.top += self.bh
        self.b1().rect.left -= self.bw
        self.snd_key.play()
      # first brick below second
      elif self.b1().rect.top > self.b2().rect.top and \
        self.db.right_edge() < self.max_pos_x and self.db.top_edge() < self.col_pix_top(self.b1_col() + 1):
        self.b1().rect.top -= self.bh
        self.b1().rect.left += self.bw
        self.snd_key.play()
      # first brick to the right of the second
      elif self.b1().rect.left > self.b2().rect.left:
        self.b1().rect.top -= self.bh
        self.b1().rect.left -= self.bw
        self.snd_key.play()
      # first brick to the left of the second
      elif self.b1().rect.left < self.b2().rect.left and \
        self.db.bottom_edge() + self.bh < self.col_pix_top(self.b1_col() + 1):
        self.b1().rect.top += self.bh
        self.b1().rect.left += self.bw
        self.snd_key.play() 
  
  def speed_up(self):
    """
    Increase fallspeed to fast.
    """
    if not self.game_over():
      self.fallspeed = self._fallspeed_fast
  
  def slow_down(self):
    """
    Decrease fallspeed to slow.
    """
    if not self.game_over():
      self.fallspeed = self._fallspeed_slow
    
  def fall_brick(self):
    """
    Drop brick by fallspeed. If the bottom is reached, then spawn a new brick.
    """
    # If the brick pair hasn't reached the bottom,
    if self.b1().rect.top < self.col_pix_top(self.b1_col()) - self.fallspeed and \
      self.b2().rect.top < self.col_pix_top(self.b2_col()) - self.fallspeed:
      # Drop bricks
      self.b1().rect.top += self.fallspeed
      self.b2().rect.top += self.fallspeed
    # Else one of the bricks has reached the top of a column
    # In this case, both bricks are dropped
    else:
      # Sound for brick reaching bottom
      self.snd_drop.play()
          
      # Brick that hits a surface first needs to handled first (in case stacked)
      # Set the one that hits first as b1
      if self.b2().rect.top >= self.col_pix_top(self.b2_col()) - self.fallspeed:
        b2, b1 = self.b1(), self.b2()
        c2, c1 = self.b1_col(), self.b2_col()
        #col_index1, col_index2 = col_index2, col_index1
      else:
        b1, b2 = self.b1(), self.b2()
        c1, c2 = self.b1_col(), self.b2_col()
        # Don't need to do anything, but check that other brick has hit
        #assert(b1.rect.top >= column_top[col_index1] - fallspeed)
      # Drop bottom brick to bottom
      b1.rect.top = self.col_pix_top(c1)
      # Save to array
      self.stacked_bricks[b1.get_col_index()][b1.get_row_index()] = b1
      # Update top position of the column
      #column_top[col_index1] -= self.bh
      # Now the other brick
      #b2.rect.top = column_top[col_index2]
      b2.rect.top = self.col_pix_top(c2)
      #column_top[col_index2] -= bh
      
      self.stacked_bricks[b2.get_col_index()][b2.get_row_index()] = b2
    
      # Handle breaking and update score
      #score = break_bricks(stacked_bricks, column_top, score)
      
      # Create new brick
      self.create_brick()
      
  def break_bricks(self):
    """
    Remove any bricks marked as broken.
    """
    # Run at least once
    broken = True
    
    # Repeatedly break (combo) until no more breaks to be found
    while broken: 
      # If any bricks were broken
      broken = False
      # Scan through array
      for col in range(self.num_cols):
        for row in range(self.num_rows):
          # If breaker is touching a brick with the same color
          if self.stacked_bricks[col][row].breaker:
            breaker_color = self.stacked_bricks[col][row].color
            if (col > 0 and self.stacked_bricks[col-1][row].color == breaker_color) or \
              (col < self.num_cols-1 and self.stacked_bricks[col+1][row].color == breaker_color) or \
              (row > 0 and self.stacked_bricks[col][row-1].color == breaker_color) or \
              (row < self.num_rows-1 and self.stacked_bricks[col][row+1].color == breaker_color):
              # Use spread_break to recursively break proper bricks
              self.spread_break(col, row, breaker_color)
              # Play sound for breaking bricks
              self.snd_break.play()
              # Bricks have been broken
              broken = True
            
      # Collapse bricks from above if any bricks were broken
      if broken:
        # Drop bricks to fill up space
        self.drop_bricks()
        
  def drop_bricks(self):
    """
    Fill in any empty spaces by moving bricks above down.
    """
    # Handle each column individual
    for col in range(self.num_cols):
      # For each row, starting from the top
      for row in range(self.num_rows - 1):
        # If this spot has a brick, and the one below is empty
        if (not self.stacked_bricks[col][row].empty()) and self.stacked_bricks[col][row+1].empty():
          # Move all bricks above down a space, starting from the bottom
          for drop_row in range(row, -1, -1):
            self.stacked_bricks[col][drop_row].rect.top += self.bh
            self.stacked_bricks[col][drop_row + 1] = self.stacked_bricks[col][drop_row]
          # Create an empty brick at the top
          self.stacked_bricks[col][0] = Brick()

  def spread_break(self, col, row, breaker_color):
    """
    Break the brick at col, row and recursively call on surrounding bricks.
    Arguments:
      col               Column index to spread break
      row               Row index to spread break
      breaker_color     Color of break to spread
    """
    # Replace image with a broken brick
    self.stacked_bricks[col][row] = Brick()  
    # Increment score for each brick destroyed
    self.score += 10
  
    # Spread to surrounding blue bricks
    if col > 0 and self.stacked_bricks[col-1][row].color == breaker_color:
      self.spread_break(col-1, row, breaker_color)
    if col < self.num_cols-1 and self.stacked_bricks[col+1][row].color == breaker_color:
      self.spread_break(col+1, row, breaker_color)
    if row > 0 and self.stacked_bricks[col][row-1].color == breaker_color:
      self.spread_break(col, row-1, breaker_color)
    if row < self.num_rows-1 and self.stacked_bricks[col][row+1].color == breaker_color:
      self.spread_break(col, row+1, breaker_color)
    
  def draw_bricks(self, surface):
    """
    Draw all bricks (stacked and dropping) to the passed Pygame Surface.
    """
    if self.db:
      # Dropping brick
      surface.blit(self.b1().image, self.b1().rect)
      surface.blit(self.b2().image, self.b2().rect)
    # Stacked bricks
    for col in range(self.num_cols):
      for row in range(self.num_rows):
        surface.blit(self.stacked_bricks[col][row].image, self.stacked_bricks[col][row].rect)
  
  def draw_score(self, surface):
    """
    Write the current score to the passed surface. Also note whether game is over.
    """
    # Font object for rendering text
    font_obj = pygame.font.Font(None, 28)
    # Location to print score
    topleft = (self.max_pos_x + 2*self.bw, self.min_pos_y + self.bh)
    # Print score to screen
    self.print_surface("Score: %d" % self.score, surface, topleft, font_obj)
    
    # If game is over
    if self.game_over():
      # Location to print to
      topleft = (self.max_pos_x + 2*self.bw, self.min_pos_y + 3*self.bh)
      # Print Game Over
      self.print_surface("Game Over", surface, topleft, font_obj)
    
  def print_surface(self, msg, surface, topleft, font_obj):
    """
    Print the passed msg string to the surface at location specified by topleft.
    Arguments
      msg        String to be displayed.
      surface    Pygame surface to print string to.
      topleft    (x, y) top left corner of location to print to.
      font_obj   Pygame font object for text rendering.
    """
    # Surface containing game over text
    # Do not anti-alias, render in white
    msg_surface = font_obj.render(msg, False, white)
    # Create rect object to specify where to place text
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = topleft
    surface.blit(msg_surface, msg_rect)
    
  def game_over(self):
    """
    Return whether the game is over.
    """
    return self.col_pix_top(self.gen_col) < 3*self.bh
    