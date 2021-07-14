import pygame as pg
import config


# slider(): Make the text slide across the screen
def effect(my_canvas, text_img):
    # go through the text message image, one slice at a time
    for my_x in range(0, config.scrollwid, config.SLICE_SIZE):
        my_y = int(config.imghgt / 2)
        my_xy = (my_x + config.scrollback, my_y + config.Y_OFFSET)
        source_area = pg.Rect((my_x, 0), (config.SLICE_SIZE, config.imghgt))
        my_canvas.blit(text_img, my_xy, source_area)

    return my_canvas, text_img
