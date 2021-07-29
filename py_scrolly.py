#!python
"""
py-scrolly: v1.0 - A screen "toy" that juggles textual graphics onscreen.

It requires the pygame module [https://www.pygame.org/]. It takes no inputs and
should be run as a standard script. It will output a pretty screen and great music,
though.
"""

import os
import os.path
import importlib
import glob

from pygame import mixer
from pygame.locals import *
from starstream import *
import cube_rotate
import time
import config
import sys

# effectsmods is a list to hold the module descriptors.
effectmods = []

# Load in 'built-in' text effects. The modnames array lists the effects always to be included.
modnames = ('01_sinus', '02_slider')

# Here be local variables. NUM_STARS sets the number of stars streaming on the background
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
    # Compose the first/top line of the footer message
    footmsg = '[f]ullscreen on/off '
    footmsg = footmsg + '[m]ute [q]uit'
    # 'Draw' the text as a graphical 'Surface'
    text = font2.render(footmsg, True, config.COLRED)
    # Find the XY dimensions of the 'text' Surface, centre it on the X-axis and move it up on the Y
    text_rect = text.get_rect(center=(int(my_canvas.get_width() / 2), my_canvas.get_height() - 80))
    # Now blast/blit the 'text' Surface onto 'my_canvas' Surface
    my_canvas.blit(text, text_rect)

    # Reuse the footmsg variable to make up the next line of text to display.
    footmsg = '[space] pause scrolling '
    footmsg = footmsg + '[bkspc] hide menu'

    # Render the footmsg into the 'text' Surface
    text = font2.render(footmsg, False, config.COLRED)
    # Get 'text' Surface dimensions, centre on X-axis and move 50 units from the bottom.
    text_rect = text.get_rect(center=(int(my_canvas.get_width() / 2), my_canvas.get_height() - 50))
    # Now, blit the 'text' Surface to 'my_canvas' Surface
    my_canvas.blit(text, text_rect)


# main() starts here. Did this really need commenting?
def main():
    """This is where all the action kicks off"""
    # Go through the modnames array
    for modname in modnames:
        # Import the 'modname' module
        mymod = importlib.import_module(modname, package='effects')
        # After the module's descriptor/handle to the effectmods array, to be used later.
        effectmods.append(mymod)

    # The 'effects' directory holds any 'extra' text effects. Find them
    # and load them dynamically.
    # Get the fullpath for the 'effects' subdirectory
    my_effdir = os.path.join(os.getcwd(), 'effects')

    # Does the 'effects' directory exist?
    if os.path.isdir(my_effdir):

        # List all the effects files in my_cwd.
        for fname in os.listdir(my_effdir):

            # Is it a '.py' file? OK, I could've done this with glob() but....
            if fname.endswith('.py'):
                # OK, make up the module name for importing
                modname = fname[:-3]
                # Stick a period (.) at the start of the module name.
                modname = f".{modname}"

                # Now, import that puppy!!!!
                mymod = importlib.import_module(modname, package='effects')
                # Add the imported module's descriptor to the effectmods array.
                effectmods.append(mymod)

    # Initialise pygame
    pg.init()
    # Set the window's caption
    pg.display.set_caption("py-scrolly")

    # Read the message file into a list
    msg_file = 'message.txt'

    # Check that the message.txt file exists
    if os.path.exists(msg_file):
        # If the 'message.txt' file exists, open it and, read it into msg_lines array.
        with open(msg_file) as f:
            msg_lines = f.read().splitlines()
    else:
        # ERROR! No message.txt file. Danger, Will Robinson! Carp about it.
        msg_lines = ['message.txt file not found. Oops!']

    # Get fullscreen info
    screen_info = pg.display.Info()
    # Set up the starting draw surface
    # 'screen' is the displayed Surface and 'my_canvas' is the Surface to be drawn to.
    screen = pg.display.set_mode([500, 500], DOUBLEBUF | RESIZABLE)
    my_canvas = screen.copy()

    # Generate a field of stars in the far background
    back_stars = []
    # Make up a cluster of 100 randomly generated stars.
    for tmp_i in range(0, 101):
        tmpx = int(random.random() * 600) - 75
        tmpy = int(random.random() * 600) - 75
        back_stars.append((tmpx, tmpy))

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

    # effect_selected is a generic local var that says which text effect is currently being used.
    effect_selected = 0

    # Make font objects, use a "non busy", sanserif font, keeps the text readable when scrolling
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
            font1 = pg.font.SysFont("Gadugi", 48)

    # Load a system font to render the footer menu
    font2 = pg.font.SysFont("Gadugi", 24)

    # Get the 'top'/first line of text from the list. This shortens the list.
    msg_txt = msg_lines.pop(0) + ' '  # Naughty hack to stop text bleeding on the screen
    # Stick this line back at the end of the list, makes the list 'loop'
    msg_lines.append(msg_txt)

    # Make up the first line of graphical text
    text_img = font1.render(msg_txt, False, config.COLBLUE)
    # config.scrollwid holds much much horizontal distance is left until the end of message line
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
        tmp_i = 0
        while tmp_i < 100:
            (tmpx, tmpy) = back_stars[tmp_i]
            tmpx = tmpx + int(screen_x * 1.5)
            if tmpx > 500:
                tmpx = tmpx - 500
            if tmpx < 1:
                tmpx = tmpx + 500

            tmpy = tmpy + int(screen_y * 1.5)
            if tmpy > 500:
                tmpy = tmpy - 500
            if tmpy < 1:
                tmpy = tmpy + 500

            my_canvas.set_at((tmpx, tmpy), config.COLWHITE)
            tmp_i += 1

        # Put the streaming stars onto the canvas
        my_canvas = starstream(my_canvas, screen_x, screen_y)

        # Draw the spinning cube
        cube_rotate.cube_rotate(my_canvas)

        # Juggle the graphical text with the 'effect' currently selected
        my_canvas, text_img = effectmods[effect_selected].effect(my_canvas, text_img)

        # Is the text supposed to be scrolling, or paused?
        if text_scrolling:
            # Shift the text image left by 2 pixels
            if config.scrollback > 0:
                config.scrollback -= 2
            else:
                text_img.scroll(-2, 0)
                config.scrollwid = config.scrollwid - 2

            if config.scrollwid < 1:
                # Get the 'top'/first line of text from the list. This shortens the list.
                msg_txt = msg_lines.pop(0) + ' '  # Naughty hack to stop text bleeding on the screen
                # Stick this line back at the end of the list, makes the list 'cycle'
                msg_lines.append(msg_txt)

                # 'Draw' the line of text as an image
                text_img = font1.render(msg_txt, False, config.COLBLUE)
                # Get the width and height of the text graphic
                config.scrollwid = text_img.get_size()[0]
                config.imghgt = text_img.get_size()[1]
                # config.scrollback is a 'pause' to give the last line a chance to
                # get clear of the screen.
                config.scrollback = 500

                # New line? Change to the next text effect
                effect_selected += 1
                # How many text effects do we have loaded?
                lenmods = len(effectmods) - 1
                # If we've got to the end of the effects list, roll back to the start
                if effect_selected > lenmods:
                    effect_selected = 0

        # Put the footer message on the canvas
        if footer_on:
            footer(my_canvas, font2)

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
                        screen_res = (screen_info.current_w, screen_info.current_h)
                        screen = pg.display.set_mode(screen_res, DOUBLEBUF | pg.FULLSCREEN)
                    else:
                        screen_res = (500, 500)
                        pg.display.toggle_fullscreen()
                        screen = pg.display.set_mode(screen_res, DOUBLEBUF | RESIZABLE)

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

                # 'spacebar' starts/stops the text from scrolling, but not animations
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

        # Scale the canvas to the required geometry, then 'blit' it to the display
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
