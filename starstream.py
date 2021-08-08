"""starstream(): Handles the movement of the stars streaming from the centre
of the screen."""
import math
import pygame as pg
import config
from newstar import *

# Generate a starting group of stars
stars = []
for i in range(0, config.NUM_STARS):
    (s_r1, s_r2, s_r3, s_r4, s_r5) = newstar()
    stars.append([s_r1, s_r2, s_r3, s_r4, s_r5])


def starstream(my_canvas, screen_x, screen_y):
    """Make the stars stream from the centre of my_canvas."""
    screen_x = screen_x + int(my_canvas.get_width() / 2)
    screen_y = screen_y + int(my_canvas.get_height() / 2) - 250
    # Step through the array of stars[]
    for i in range(0, config.NUM_STARS):
        # starang is the angle (in radians) of travel from the centre of the screen
        starang = stars[i][0]
        # starrad is the 'radius'/'distance' of the 'star' from the screen centre
        starrad = stars[i][1]
        # Make the 'star' move exponentially away from screen centre
        stars[i][1] = starrad * 1.05
        # Work out the screen X/Y co-ords for the 'star'
        starx = int((math.cos(math.radians(starang)) * starrad)) + screen_x
        stary = int((math.sin(math.radians(starang)) * starrad)) + screen_y
        # If the 'star' has travelled off-screen, make a new 'star'
        if (starx < 0) or (starx > 500) or (stary < 0) or (stary > 500):
            (r1, r2, r3, r4, r5) = newstar()
            stars[i] = [r1, 10, r3, r4, r5]
            starx = stary = 1

        # Now draw what you've got onto the active drawing surface, my_canvas
        pg.draw.circle(my_canvas, (stars[i][2], stars[i][3], stars[i][4]), (starx, stary), 2)

    # When we're done return the finished active drawing surface, my_canvas
    return my_canvas
