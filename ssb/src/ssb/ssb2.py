'''
Something Something Bricks

Super Puzzle Fighter clone using pygame.

Created on Dec 20, 2011

@author: Daniel Lo
'''

import pygame
import sys

from board import Board
from color import *
from menu2 import Menu

## Size parameters  
# number of rows and columns in play area
board_size = num_cols, num_rows = 6, 15
# Block width, used to space out objects
brick_size = bw, bh = (32, 32)

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
  
# Screen shot counter
screen_shot_count = 0

# State of the game: playing or in menu
game_state = "menu"

# Create game board object
game_board = Board(board_size, brick_size, pygame.mixer)

# topleft corner of where to display menu
menu_topleft = (game_board.max_pos_x + 2*game_board.bw, game_board.min_pos_y + 5*game_board.bh)
# Create menu object
menu_obj = Menu(menu_topleft, pygame.mixer)

# Directory where sounds are kept
snd_dir = "../../sounds/"
# Background music
#snd_background = pygame.mixer.Sound(snd_dir + "fkobbe-121111final.wav")
#snd_background.play(loops=-1)

# Main loop
while True:
    
  # Event Handler
  for event in pygame.event.get():
    # Keypresses
    if event.type == pygame.KEYDOWN:
      # Key down handling for all states
      # Quit game
      if event.key == pygame.K_ESCAPE:
        sys.exit()
      # Save a screen cap when I is pressed
      elif event.key == pygame.K_i:
        pygame.image.save(screen, "screenshot_%d.png" % screen_shot_count)
        screen_shot_count += 1

      elif event.key == pygame.K_r:
        game_board.start()
        game_state = "play"
      elif event.key == pygame.K_m:
        game_state = "menu"
        
      else:
        # Key down handling specific to play state
        if game_state == "play":
          # Move brick left (subtract from x coordinate)
          if event.key == pygame.K_LEFT:
            game_board.move_left()
          # Move brick right (add to x coordinate)
          elif event.key == pygame.K_RIGHT:
            game_board.move_right()
          # Increased fall speed when DOWN is held
          elif event.key == pygame.K_DOWN:
            game_board.speed_up()
          # On rotation, always first (top) brick that moves
          # Rotate clockwise
          elif event.key == pygame.K_e:
            game_board.rotate_cw()
          # Rotate counter-clockwise
          elif event.key == pygame.K_q:
            game_board.rotate_ccw()
            
        # Key down handling specific to menu state
        elif game_state == "menu":
          # Move down in menu
          if event.key == pygame.K_DOWN:
            menu_obj.menu_down()
          # Move up in menu
          elif event.key == pygame.K_UP:
            menu_obj.menu_up()
          # Execute selected menu item
          elif event.key == pygame.K_RETURN:
            # Play game
            if menu_obj.selected == "Play":
              # Change program state to play mode
              game_state = "play"
              # Start game
              game_board.start()
            # Exit game
            elif menu_obj.selected == "Exit":
              sys.exit()
            else:
              raise Exception("Unknown menu item.")
            
        else:
          raise Exception("Unknown game state.")            
        
    elif event.type == pygame.KEYUP:
      # Key up handling when in play state
      if game_state == "play":
        # Decrease fall speed once DOWN is released
        if event.key == pygame.K_DOWN:
          game_board.slow_down()
        
    # Quit game
    elif event.type == pygame.QUIT:
      sys.exit()
      
  # Blank screen
  screen.fill(black)
  
  # Draw walls
  pygame.draw.line(screen, white, (bw, bh), (bw, (num_rows+1)*bh), 1)
  pygame.draw.line(screen, white, (bw, (num_rows+1)*bh), ((num_cols+1)*bw, (num_rows+1)*bh), 1)
  pygame.draw.line(screen, white, ((num_cols+1)*bw, bh), ((num_cols+1)*bw, (num_rows+1)*bh), 1)
  # Generation line
  pygame.draw.line(screen, white, (bw, bh), ((num_cols+1)*bw, bh))
  # Game over line
  pygame.draw.line(screen, gray, (bw, 3*bh), ((num_cols+1)*bw, 3*bh))
  """
  # Draw vertical grid lines
  for x in range(5):
    pygame.draw.line(screen, gray, ((2+x)*bw, bh), ((2+x)*bw, 21*bh), 1)
  # Draw horizontal grid lines
  for y in range(19):
    pygame.draw.line(screen, gray, (bw, (2+y)*bh), (7*bw, (2+y)*bh), 1)
  """

  # Draw falling and stacked bricks
  game_board.draw_bricks(screen)
  # Draw score
  game_board.draw_score(screen)

  # Draw menu
  if game_state == "menu":
    menu_obj.draw_menu(screen)
  elif game_state == "play":
    # If the game is not over
    if not game_board.game_over():
      # Advance game
      game_board.update()
    # If the game is over, return to menu
    else:
      game_state = "menu"
  else:
    raise Exception("Unknown game state")
  
  # Refresh display
  pygame.display.update()    
  # Ensure 60 FPS
  fps_clock.tick(60)
  