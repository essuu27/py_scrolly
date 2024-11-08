#!python
"""
py-scrolly: v1.0 - A screen "toy" that juggles textual graphics onscreen.

Requires the pygame module [https://www.pygame.org/]. It takes no inputs and
should be run as a script. It will output a pretty screen and great music,
though.
"""

import os
import os.path
import time
import sys
import importlib
import glob
import random
import webbrowser

import pygame as pg
from pygame import (mixer, DOUBLEBUF, RESIZABLE)
from starstream import starstream
import cube_rotate
import config

# Load 'built-in' effects. The modnames array lists the effects to be included.
modnames = ('01_sinus', '02_slider')

# NUM_STARS sets the number of stars streaming on the background
NUM_STARS = 20


# Define all the functions

# screendrift handles the directional drifting of the background stars
# screen_x, screen_y set how much the screen drifts on the X- and Y- axis.
def screendrift(screen_x, screen_y):
    """Handles the X/Y co-ord drifting of the screen background"""
    # config.scrndrft is the overall, general part of the drift sequence
    tmpx = config.scrndrft[0]
    if tmpx in (0, 7):
        screen_x -= 1
        screen_y -= 1
    elif tmpx in (1, 6):
        screen_x += 1
        screen_y -= 1
    elif tmpx in (2, 5):
        screen_x += 1
        screen_y += 1
    elif tmpx in (3, 4):
        screen_x -= 1
        screen_y += 1

    return screen_x, screen_y


# print the messages at the bottom(foot) of the screen
def footer(my_canvas, font2):
    """Prints the command menu at the foot of the screen"""
    footmsg = '[f]ullscreen on/off ' + '[m]ute [q]uit'

    # 'Draw' the text as a graphical 'Surface'
    text = font2.render(footmsg, True, config.COLRED)
    # Find XY dimensions of 'text', centre on X-axis and move it on the Y
    text_rect = text.get_rect(center=(int(my_canvas.get_width() / 2),
                                      my_canvas.get_height() - 80))
    # Now blast/blit the 'text' Surface onto 'my_canvas' Surface
    my_canvas.blit(text, text_rect)

    footmsg = '[space] pause scrolling ' + '[bkspc] hide menu'

    # Render the footmsg into the 'text' Surface
    text = font2.render(footmsg, False, config.COLRED)
    # Get 'text' Surface dimensions, centre on X, move 50 units from bottom
    text_rect = text.get_rect(center=(int(my_canvas.get_width() / 2),
                                      my_canvas.get_height() - 50))
    # Now, blit the 'text' Surface to 'my_canvas' Surface
    my_canvas.blit(text, text_rect)


# main() starts here. Did this really need commenting?
def main():
    """This is where all the action kicks off"""

# Go through the modnames array
    effectmods = [importlib.import_module(modname, package='effects')
                  for modname in modnames]

    # The 'effects' directory holds any 'extra' text effects. Find them
    # and load them dynamically.
    # Get the fullpath for the 'effects' subdirectory
    my_effdir = os.path.join(os.getcwd(), 'effects')

    # Does the 'effects' directory exist?
    if os.path.isdir(my_effdir):

        # List all the effects files in my_cwd.
        valid_fnames = filter(lambda fname: fname.endswith('.py'),
                              os.listdir(my_effdir))

        # OK, make up the module name for importing
        # Stick a period (.) at the start of the module name.
        effect_modnames = (f".{fname[:-3]}" for fname in valid_fnames)

        # Now, import that puppy!!!!
        # Add the imported modules descriptor to the effectmods array.
        effectmods += [importlib.import_module(modname, package='effects')
                       for modname in effect_modnames]

    # Initialise pygame
    pg.init()
    # Set the window's caption
    pg.display.set_caption("py-scrolly")

    # Read the message file into a list
    msg_file = 'message.txt'

    # Check that the message.txt file exists
    try:
        # If 'message.txt' file exists, open and, read into msg_lines array.
        with open(msg_file) as f:
            msg_lines = f.read().splitlines()
    except OSError:
        # ERROR! No message.txt file. Danger, Will Robinson! Carp about it.
        msg_lines = ['message.txt file not found. Oops!']

    # Get fullscreen info
    screen_info = pg.display.Info()

    # Set up the starting draw surface
    # 'screen' is displayed Surface, 'my_canvas' is the Surface to be drawn to.
    screen = pg.display.set_mode([500, 500], DOUBLEBUF | RESIZABLE)
    my_canvas = screen.copy()

    # Generate a field of stars in the far background
    back_stars = [(int(random.random() * 600) - 75,
                  int(random.random() * 600) - 75)
                  for _ in range(0, 101)]

    # Initialise pygame's music library, set the volume to be "not too loud!"
    mixer.init()
    mixer.music.set_volume(0.7)

    # Load in the background music. The distributed tune is 'Mellow strain'
    # by U4iaF8 (thanks Jim!). However, the script will find any MP3 file
    # in the directory and play it.
    # Look for a filename ending with '.mp3'
    music_files = glob.glob('*.mp3')
    # If one has been found, load it.
    if len(music_files) > 0:
        mixer.music.load(music_files[0])
        # Start playing the music, on a loop
        mixer.music.play(-1)

    # effect_selected holds value of text effect that is currently being used.
    effect_selected = 0

    # Make font objects, use a "non busy", sanserif font
    # Safely load the font. First, is the font already installed on the system?
    if pg.font.match_font("Rubik"):
        font1 = pg.font.SysFont("Rubik", 48)
    else:
        # OK, the font is not a system font. Try loading the local font file
        # Check if the font file is present? If it is, then load it.
        if os.path.exists("Rubik.ttf"):
            font1 = pg.font.Font("Rubik.ttf", 48)
        else:
            # OK, can't find a system font or a font file. Use a default font
            font1 = pg.font.SysFont("Lucida", 48)

    font3 = pg.font.SysFont("Lucida", 22)

    # Load a system font to render the footer menu
    font2 = pg.font.SysFont("Gadugi", 24)

    # Get the 'top'/first line of text from the list. This shortens the list.
    msg_txt = msg_lines.pop(0) + ' '  # Naughty hack to stop text "bleeding"
    # Stick this line back at the end of the list, makes the list 'loop'
    msg_lines.append(msg_txt)

    # Make up the first line of graphical text
    text_img = font1.render(msg_txt, False, config.COLBLUE)

    font3.set_underline(True)
    bragtext = font3.render('GitHub:@essuu27', False, config.COLRED)
    font3.set_underline(False)

    # config.scrollwid holds how much horizontal distance is left until
    # the end of message line
    config.scrollwid = text_img.get_size()[0]
    config.imghgt = text_img.get_size()[1]

    # Run until the user asks to quit
    running = True

    # clock is a PyGame Clock object
    clock = pg.time.Clock()
    # mouse_time holds the last time the mouse pointer was moved
    mouse_time = time.time()
    mouse_hide = False
    footer_on = True

    # Startup values for runtime variables
    screen_x = screen_y = 1
    config.start_angle = 0
    full_screen = False
    text_scrolling = 1
    drift_time = 0
    music_vol = True

    # Everything should be initialised by now, run the main program loop
    while running:
        # Get the current time, use this for hiding the cursor
        now_time = time.time()

        # Render the screen image. Start with a blank canvas
        my_canvas.fill((10, 10, 10))

        # Now paint the background stars onto the canvas
        for tmpx, tmpy in back_stars:
            my_canvas.set_at(
                (
                    (tmpx + int(screen_x * 1.5)) % 500,
                    (tmpy + int(screen_y * 1.5)) % 500,
                ),
                config.COLWHITE
            )

        # Put the streaming stars onto the canvas
        my_canvas = starstream(my_canvas, screen_x, screen_y)

        # Draw the spinning cube
        cube_rotate.cube_rotate(my_canvas)

        # Juggle the graphical text with the 'effect' currently selected
        my_canvas, text_img = effectmods[effect_selected].effect(my_canvas,
                                                                 text_img)

        # Is the text supposed to be scrolling, or paused?
        if text_scrolling:
            # Shift the text image left by 2 pixels
            if config.scrollback > 0:
                config.scrollback -= 2
            else:
                text_img.scroll(-2, 0)
                config.scrollwid = config.scrollwid - 2

            if config.scrollwid < 1:
                # Get the first line from the list. This shortens the list.
                msg_txt = msg_lines.pop(0) + ' '  # Stop text "bleeding"
                # Put line back at the end of the list, makes the list 'cycle'
                msg_lines.append(msg_txt)

                # 'Draw' the line of text as an image
                text_img = font1.render(msg_txt, False, config.COLBLUE)
                # Get the width and height of the text graphic
                config.scrollwid = text_img.get_size()[0]
                config.imghgt = text_img.get_size()[1]
                # config.scrollback is a 'pause' to give the last line
                # a chance to get clear of the screen.
                config.scrollback = 500

                # New line? Change to the next text effect
                effect_selected += 1
                # How many text effects do we have loaded?
                lenmods = len(effectmods) - 1
                # If at end of the effects list, roll back to the start
                if effect_selected > lenmods:
                    effect_selected = 0

        # Put the footer message on the canvas
        if footer_on:
            footer(my_canvas, font2)

        hotzone = my_canvas.blit(bragtext, (360, 480))

        # Now handle any user input
        for event in pg.event.get():
            # Was a 'quit' event raised?
            if event.type == pg.QUIT:
                running = False

            # Process key presses. First, check if a key has been pressed.
            if event.type == pg.KEYDOWN:
                # Key 'F' toggles fullscreen on/off
                if event.key == pg.K_f:
                    full_screen = not full_screen
                    if full_screen:
                        screen_res = (screen_info.current_w,
                                      screen_info.current_h)
                        screen = pg.display.set_mode(screen_res, DOUBLEBUF |
                                                     pg.FULLSCREEN)
                    else:
                        screen_res = (500, 500)
                        pg.display.toggle_fullscreen()
                        screen = pg.display.set_mode(screen_res, DOUBLEBUF |
                                                     RESIZABLE)

                # Key 'q' quits the program
                if event.key == pg.K_q:
                    running = 0

                # Key 'm' mutes/unmutes the sound
                if event.key == pg.K_m:
                    music_vol = not music_vol
                    if music_vol is True:
                        pg.mixer.music.set_volume(0.70)
                    else:
                        pg.mixer.music.set_volume(0)

                # 'spacebar' starts/stops text scrolling, but not animating
                if event.key == pg.K_SPACE:
                    text_scrolling = not text_scrolling

                # 'backspace' toggles the footer bar
                if event.key == pg.K_BACKSPACE:
                    footer_on = not footer_on

            # Un-hide the mouse pointer if it moves
            if event.type == pg.MOUSEMOTION and mouse_hide is True:
                mouse_time = now_time
                mouse_hide = False
                pg.mouse.set_visible(True)

            # if mouse pressed get pos. of cursor in screen coords##
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Get current screen width and height
                scr_w, scr_h = pg.display.get_surface().get_size()
                # Mouse coords are returned in real world values
                mouse_x, mouse_y = event.pos
                # Scale mouse coords from real world vals to surface frame
                mouse_x = int((mouse_x / scr_w) * 500)
                mouse_y = int((mouse_y / scr_h) * 500)
                # Repack the mouse coord tuple
                pos = (mouse_x, mouse_y)

                # Check if mouse pointer is in our 'hotzone'
                if hotzone.collidepoint(pos):
                    # It is, so launch a web browser.
                    webbrowser.open('https://github.com/essuu27/py_scrolly')

        # If the mouse pointer doesn't move for 10 seconds, hide it
        if mouse_hide is False and (now_time - mouse_time) > 10:
            mouse_hide = True
            mouse_time = now_time
            pg.mouse.set_visible(False)

        #  Determine the current canvas geometry
        canvas_xy = (0, 0)
        if full_screen:
            canvas_res = (screen_info.current_w, screen_info.current_h)
        else:
            canvas_res = (500, 500)

        # Scale canvas to required geometry, then 'blit' it to the display
        screen.blit(pg.transform.scale(my_canvas, canvas_res), canvas_xy)

        # Now present the finished image to the display
        pg.display.flip()

        # Manipulate the screen's geometry
        (screen_x, screen_y) = screendrift(screen_x, screen_y)

        # Move the textbox along
        config.start_angle -= 2
        if config.start_angle < 0:
            config.start_angle = 360

        # Control the backdrop/star drift.
        drift_time -= 1
        if drift_time < 1:
            drift_time = 90
            tmpx = config.scrndrft[0] + 1
            if tmpx > 8:
                tmpx = 0
            config.scrndrft[0] = tmpx

        # Delay the program to make a reasonably viewable display
        clock.tick(60)

    # Done! Time to quit.
    pg.quit()
    sys.exit()


# This kicks the program off
if __name__ == '__main__':
    main()
