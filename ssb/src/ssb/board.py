'''
Object to keep track of the board (stacked bricks) game state.

Created on Dec 22, 2011

@author: Dan
'''

from brick import Brick
from color import *

class Board:
  """
  Class for play area (stacked bricks).
  """
  
  def __init__(self, size):
    """
    Default constructor.
    Arguments:
      size    number of (columns, rows)
    """
    # Save parameters
    self.num_cols, self.num_rows = self.size = size
    
    # Create array of stacked bricks
    self.stacked_bricks = [0]*self.num_cols
    for col in self.num_cols:
      # Intialized bricks are "empty" (color black, no dimensions)
      self.stacked_bricks[col] = [Brick()]*self.num_rows
      
  def col_top(self, col):
    """
    Return the top row in column col that contains a brick.
    Arguments:
      col    column to return top row of
    """
    for row in range(self.num_rows):
      if self.stacked_bricks[col][row] != black:
        return row
