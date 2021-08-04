"""Makes the text graphics move across the screen in a rolling sinewave."""

# Need the math() library for radians and sine functions
import math
import pygame as pg
import config


# sinus(): Make the text scroll, following a sinewave
def effect(my_canvas, text_img):
    """Take the text_img graphic, manipulate it and blit it to my_canvas

 All effect modules have the same function call syntax; name: effect(),
 active drawing surface name: my_canvas, text image to be manipulated: text_img

 This effect makes the text follow a rolling sinewave on the screen"""

    # start_angle in the radial angle of the first blit of the message
    myang = config.start_angle

    # go through the text message image, one slice at a time
    for my_x in range(0, config.scrollwid, config.SLICE_SIZE):
        my_y = int((math.sin(math.radians(myang))) * (config.imghgt / 2))
        my_xy = (my_x + config.scrollback, my_y + config.Y_OFFSET)
        source_area = pg.Rect((my_x, 0), (config.SLICE_SIZE, config.imghgt))
        my_canvas.blit(text_img, my_xy, source_area)
        myang += 4
        if myang > 360:
            myang = 0

    return my_canvas, text_img
