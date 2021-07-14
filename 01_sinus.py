import pygame as pg
import config

# Need the math() library for radians and sine functions
from math import *


# sinus(): Make the text scroll, following a sinewave
def effect(my_canvas, text_img):

    # start_angle in the radial angle of the first blit of the message
    myang = config.start_angle

    # go through the text message image, one slice at a time
    for my_x in range(0, config.scrollwid, config.SLICE_SIZE):
        my_y = int((sin(radians(myang))) * (config.imghgt / 2))
        my_xy = (my_x + config.scrollback, my_y + config.Y_OFFSET)
        source_area = pg.Rect((my_x, 0), (config.SLICE_SIZE, config.imghgt))
        my_canvas.blit(text_img, my_xy, source_area)
        myang += 4
        if myang > 360:
            myang = 0

    return my_canvas, text_img
