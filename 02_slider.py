"""Make the graphical text slide across the screen"""

import pygame as pg
import config


def effect(my_canvas, text_img):
    """Take the text_img graphic, manipulate it and blit it to my_canvas

 All effect modules have the same function call syntax; name: effect(),
 active drawing surface name: my_canvas, text image to be manipulated: text_img

 This effect makes the text slide across the screen."""

    # go through the text message image, one slice at a time
    for my_x in range(0, config.scrollwid, config.SLICE_SIZE):
        my_y = int(config.imghgt / 2)
        my_xy = (my_x + config.scrollback, my_y + config.Y_OFFSET)
        source_area = pg.Rect((my_x, 0), (config.SLICE_SIZE, config.imghgt))
        my_canvas.blit(text_img, my_xy, source_area)

    return my_canvas, text_img
