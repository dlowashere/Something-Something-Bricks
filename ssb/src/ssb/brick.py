'''
Class for Brick object for Something Something Bricks.

Created on Dec 20, 2011

@author: Dan
'''

import pygame
import math

from color import *

class Brick(pygame.sprite.Sprite):
  """
  Class for a single brick. Extends sprite class.
  """
  
  # Images folder
  _img_dir = "images/"
  # Images for breaker gems
  _img_yellow_breaker = pygame.image.load(_img_dir + "yellow_breaker.png")
  _img_blue_breaker = pygame.image.load(_img_dir + "blue_breaker.png")
  _img_red_breaker = pygame.image.load(_img_dir + "red_breaker.png")
  _img_green_breaker = pygame.image.load(_img_dir + "green_breaker.png")
  _img_breakers = {yellow:_img_yellow_breaker, blue:_img_blue_breaker, red:_img_red_breaker, green:_img_green_breaker}
  # Images for regular bricks
  _img_yellow = pygame.image.load(_img_dir + "yellow_brick.png")
  _img_blue = pygame.image.load(_img_dir + "blue_brick.png")
  _img_red = pygame.image.load(_img_dir + "red_brick.png")
  _img_green = pygame.image.load(_img_dir + "green_brick.png")
  _img_bricks = {yellow:_img_yellow, blue:_img_blue, red:_img_red, green:_img_green}
  # Image for broken brick
  _img_blue_broken = pygame.image.load(_img_dir + "blue_broken.png")
  _img_red_broken = pygame.image.load(_img_dir + "red_broken.png")
  _img_yellow_broken = pygame.image.load(_img_dir + "yellow_broken.png")
  _img_green_broken = pygame.image.load(_img_dir + "green_broken.png")
  _img_broken_bricks = {yellow:_img_yellow_broken, blue:_img_blue_broken, red:_img_red_broken, green:_img_green_broken}
  
  def __init__(self, color=black, initial_position=(0, 0), size=(0,0), breaker=False):
    """
    Default constructor.
    Arguments:
      color             (R, G, B) color triplet
      initial_position  (x, y) topleft corner of brick
      size              (width, height) size of brick 
      breaker           Boolean, whether this brick is a breaker brick
    """
    # Extend sprite class
    pygame.sprite.Sprite.__init__(self)
    
    # Save parameters
    self.bw, self.bh = self.size = size
    self.color = color
    self.breaker = breaker
    
    # Brick broken, but graphic not removed yet
    self.broken = False
    
    # Image for empty brick
    if self.color == black:
      self.image = pygame.Surface(self.size)
    # Image for non-breaker is a filled surface
    elif not breaker:
      self.image = self._img_bricks[color]
    # Image for breakers
    else:
      self.image = self._img_breakers[color]
    
    # Rectangle representing sprite
    self.rect = self.image.get_rect()
    self.rect.topleft = (initial_position)
  
  def get_col_index(self):
    """
    Determine grid index of column where brick is.
    """
    return self.rect.left/self.bw - 1
  
  def get_row_index(self):
    """
    Determine grid index of row where brick is. Uses the bottom grid if split between two grid spaces.
    """
    return int(math.ceil(float(self.rect.top)/self.bh)) + 2
  
  def break_brick(self):
    """
    Replace brick image with a broken brick image.
    """
    # Change image
    self.image = self._img_broken_bricks[self.color]
    # Set color to black so this brick is not "rebroken"
    self.color = black
    self.breaker = False
    # Mark as broken
    self.broken = True
    
  def empty(self):
    """
    Return whether brick is empty (color = black).
    """
    return self.color == black

class DoubleBrick:
  """
  Class for pair of bricks.
  """
  
  def __init__(self, brick_colors, breaker, initial_position, size):
    """
    Default constructor. Bricks are arranged vertically initially.
    Arguments:
      brick_colors      (c1, c2) colors for next brick pair
      breaker           (b1, b2) boolean noting whehter a breaker or not
      initial_position  (x, y) topleft corner of top brick
      size              (width, height) size of each brick
    """  
    self.bw, self.bh = self.size = size
    # Create two single bricks
    self.brick1 = Brick(brick_colors[0], initial_position, size, breaker[0])
    # Position of second brick
    x = initial_position[0]
    y = initial_position[1] + self.bh
    self.brick2 = Brick(brick_colors[1], (x, y), size, breaker[1])
    
  def top_edge(self):
    """
    Return top edge of top brick.
    """
    return min(self.brick1.rect.top, self.brick2.rect.top)
  
  def bottom_edge(self):
    """
    Return top edge of bottom brick.
    """
    return max(self.brick1.rect.top, self.brick2.rect.top)
  
  def left_edge(self):
    """
    Return left edge of left brick.
    """
    return min(self.brick1.rect.left, self.brick2.rect.left)
  
  def right_edge(self):
    """
    Return left edge of right brick.
    """
    return max(self.brick1.rect.left, self.brick2.rect.left)

  def move(self, topleft):
    """
    Move the topleft of this double brick to location topleft. Second brick
    is always placed below.
    Arguments
      topleft    (x, y) new top corner of double brick pair
    """
    self.brick1.topleft = topleft
    self.brick2.topleft = topleft
    
  