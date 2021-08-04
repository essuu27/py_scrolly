""" newstar() generate/return co-ords and details for a 'new' star
Make an "angle" for travel from centre, distance from centre and RGB colours"""

import random


def newstar():
    star_angle = int(random.random() * 360)
    star_radius = int(random.random() * 255)
    star_red = int(random.random() * 255)
    star_blue = int(random.random() * 255)
    star_green = int(random.random() * 100)
    return star_angle, star_radius, star_red, star_blue, star_green
