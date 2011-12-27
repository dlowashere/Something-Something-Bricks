'''
Created on Dec 26, 2011

Something Something Bricks menu system.

@author: Daniel Lo
'''

import pygame
import sys
import os

from color import *

def print_surface(msg, surface, topleft, font_obj):
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

def menu_execute(menu_state):
  """
  Execute the menu item selected.
    menu_state    Menu item selected.
  """
  if menu_state == "Play":
    
    os.system("ssb.py")
    sys.exit()
  elif menu_state == "Exit":
    sys.exit()

## Pygame initialization
# Reduce sound buffer size (4096 to 512) to reduce lag
pygame.mixer.pre_init(44100, -16, 2, 512)
# Initialize Pygame    
pygame.init()
# Window size
size = width, height = 370, 180
# Initialize window
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Something Something Bricks')
# Font object for rendering text
font_large = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 28)

# Possible menu items
menu = {"Play":(150, 80), "Exit":(150, 120)}
# Where the menu cursor is
menu_state = "Play"

# Main loop
while True:
  
  # Event Handler
  for event in pygame.event.get():
    # Keypresses
    if event.type == pygame.KEYDOWN:
      # Quit game
      if event.key == pygame.K_ESCAPE:
        sys.exit()
      
      # Down in menu selection
      if event.key == pygame.K_DOWN:
        menu_state = "Exit"
      elif event.key == pygame.K_UP:
        menu_state = "Play"
      elif event.key == pygame.K_RETURN:
        menu_execute(menu_state)
  
  # Blank screen
  screen.fill(black)      
  
  # Game title
  print_surface("Something Something Bricks", screen, (10, 20), font_large)
  # Display menu items
  for key in menu.keys():
    print_surface(key, screen, menu[key], font_small)
  # Display rectangle to indicate current selection
  pygame.draw.rect(screen, white, pygame.rect.Rect(menu[menu_state], (50, 30)), 1)
  
  
  # Update display
  pygame.display.update()
  