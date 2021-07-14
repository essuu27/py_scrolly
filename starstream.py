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
    screen_x = screen_x + int(my_canvas.get_width() / 2)
    screen_y = screen_y + int(my_canvas.get_height() / 2) - 250
    for i in range(0, config.NUM_STARS):
        starang = stars[i][0]
        starrad = stars[i][1]
        stars[i][1] = starrad * 1.05
        starx = int((math.cos(math.radians(starang)) * starrad)) + screen_x
        stary = int((math.sin(math.radians(starang)) * starrad)) + screen_y
        if (starx < 0) or (starx > 500) or (stary < 0) or (stary > 500):
            (r1, r2, r3, r4, r5) = newstar()
            stars[i] = [r1, 10, r3, r4, r5]
            starx = stary = 1

        pg.draw.circle(my_canvas, (stars[i][2], stars[i][3], stars[i][4]), (starx, stary), 2)

    return my_canvas
