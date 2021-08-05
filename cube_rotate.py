"""A minor reworking of the wonderful code supplied by GitHub:Magoninho"""
import pygame
import numpy as np
from math import *
import config


# Draw the edges between vertices
def connect_points(my_canvas, i, j, points):
    pygame.draw.line(
        my_canvas, (255, 255, 255), (points[i][0], points[i][1]),
        (points[j][0], points[j][1]))


def cube_rotate(my_canvas):
    """Rotate the 3D wireframe cube"""

    rotation_z = np.array([
        [cos(config.angle), -sin(config.angle), 0],
        [sin(config.angle), cos(config.angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.array([
        [cos(config.angle), 0, sin(config.angle)],
        [0, 1, 0],
        [-sin(config.angle), 0, cos(config.angle)],
    ])

    rotation_x = np.array([
        [1, 0, 0],
        [0, cos(config.angle), -sin(config.angle)],
        [0, sin(config.angle), cos(config.angle)],
    ])
    config.angle += 0.01

    # drawing stuff

    i = 0
    for point in config.points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(config.projection_matrix, rotated2d)

        x = int(projected2d[0][0] * config.scale) + config.cent_xy[0]
        y = int(projected2d[1][0] * config.scale) + config.cent_xy[1]

        config.projected_points[i] = [x, y]
        i += 1

    for p in range(4):
        connect_points(my_canvas, p, (p + 1) % 4, config.projected_points)
        connect_points(my_canvas,
                       p + 4, ((p + 1) % 4) + 4, config.projected_points)
        connect_points(my_canvas, p, (p + 4), config.projected_points)

    return 0
