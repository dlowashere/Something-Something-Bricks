'''
Menu object for Something Somethin Bricks.

Created on Dec 27, 2011

@author: Dan
'''

import pygame

from color import *

class Menu:
  
  def __init__(self, topleft = (0, 0), mixer=None):
    """
    Default constructor.
      topleft    (x, y) top left corner of location for menu
      mixer      Pygame mixer object for sounds
    """
    # Top left corner of menu
    self.left, self.top = self.topleft = topleft
    # Pixels between top of each line
    self.linespacing = 30
    # Which item is selected
    self.selected = "Play"
    
    # Add sounds
    if mixer:
      # Directory where sounds are kept
      snd_dir = "../../sounds/"
      # Sound for key press
      self.snd_key = mixer.Sound(snd_dir + "select.wav")
      self.snd_key.set_volume(0.1)
  
  def draw_menu(self, surface):
    """
    Draw menu to the passed surface starting at the topleft corner passed.
      surface    Surface to draw menu to.
    """
    font_obj = pygame.font.Font(None, 28)
    self.print_surface("Play", surface, (self.left + 5, self.top + 5), font_obj)
    self.print_surface("Exit", surface, (self.left + 5, self.top + self.linespacing + 5), font_obj)
    # Draw selection cursor
    if self.selected == "Play":
      pygame.draw.rect(surface, white, pygame.rect.Rect(self.topleft, (100, self.linespacing)), 2)
    elif self.selected == "Exit":
      pygame.draw.rect(surface, white, pygame.rect.Rect((self.left, self.top + self.linespacing), (100, self.linespacing)), 2)
    else:
      raise Exception("Unknown menu state.")
    
  def menu_up(self):
    """
    Move up in the menu selections.
    """
    if self.selected == "Exit":
      self.selected = "Play"
      self.snd_key.play()
    
  
  def menu_down(self):
    """
    Move down in the menu selections.
    """
    if self.selected == "Play":
      self.selected = "Exit"
      self.snd_key.play()

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
    msg_surface = font_obj.render(msg, True, white)
    # Create rect object to specify where to place text
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = topleft
    surface.blit(msg_surface, msg_rect)