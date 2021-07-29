"""Act like a magnifying glass on the text in the middle of the stream"""
import math
import pygame as pg
import config

MAG_RAD = 80


def effect(my_canvas, text_img):
    """Take the text_img graphic, manipulate it and blit it to my_canvas

    All effect modules have the same function call syntax; name: effect(),
    active drawing surface name: my_canvas, text image to be manipulated: text_img

    This effect makes it look like the text in the middle of the stream is being
    viewed through a magnifying glass.
    """
    # Derive working variables and working surfaces
    (pic_wid, pic_ht) = text_img.get_size()
    cent_x = 250

    tmp_screen = pg.Surface((4, pic_ht))
    tmp_screen2 = pg.Surface((4, pic_ht))

    # go through the text message image, one slice at a time
    for x in range(0, pic_wid, 4):
        tmp_screen.fill((255, 255, 255))
        tmp_screen.blit(text_img, (0, 0), (x, 0, 4, pic_ht))
        tmp_screen.set_colorkey((255, 255, 255))

        trig_x = x + config.scrollback
        my_xy = (trig_x, config.Y_OFFSET + (pic_ht / 2))

        if (trig_x > (cent_x - MAG_RAD)) & (trig_x < (cent_x + MAG_RAD)):

            mag_x = abs(cent_x - trig_x)
            mag_factor = int(math.sin(math.acos(mag_x / MAG_RAD)) * MAG_RAD)

            tmp_screen2 = pg.transform.scale(tmp_screen, (4, mag_factor * 4))
            (tmp_wid, tmp_ht) = tmp_screen2.get_size()
            if tmp_ht < (pic_ht / 2):
                tmp_screen2 = tmp_screen

            my_xy = (trig_x, config.Y_OFFSET - (tmp_ht / 2) + 50)
            my_canvas.blit(tmp_screen2, my_xy)
        else:
            my_canvas.blit(tmp_screen, my_xy)

    return my_canvas, text_img
