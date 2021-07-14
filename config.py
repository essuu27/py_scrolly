import numpy as np
# == Global constants ==
# Some universal colour definitions (array)
COLWHITE = [255, 255, 255]
COLBLUE = [0, 0, 255]
COLRED = [255, 0, 0]
COLGREY = [192, 192, 192]

# NUM_STARS(int) sets the number of stars that 'stream' from the screen centre
NUM_STARS = 20

# screen_x(int), screen_y(int) are the 'centre point' of the window
screen_x = 250
screen_y = 250

# Y_OFFSET(int), set how far down the window the text image should appear
Y_OFFSET = 200

# SLICE_SIZE(int) is the width in dots of the text image 'slice' that is processed.
# Smaller SLICE_SIZE makes smoother images but slower processing
SLICE_SIZE = 4

# scrollback(int) is the 'backoff' period before the scrolling text is affected
scrollback = 500

# Setup holders and definitions for stars and, cube vertices and edges
stars = []
vertices = [[-50, -50, -50], [-50, -50, 50], [-50, 50, -50],
            [-50, 50, 50], [50, -50, -50], [50, -50, 50],
            [50, 50, -50], [50, 50, 50]]
edges = [[0, 1], [0, 3], [0, 4], [2, 1], [2, 3], [2, 7], [6, 3],
         [6, 4], [6, 7], [5, 1], [5, 4], [5, 7]]

# == Global variables ==
# scrndrfy(array) is an array that controls the drifting of the backdrop
scrndrft = [1, 0, 0, 0, 50]

# drift_time(int) sets how long the backdrop should 'drift' before changing direction
drift_time = 90

# scrollwid(int), start_angle(int), imghgt(int), declarations to make these vars 'global'
scrollwid = 0
start_angle = 0
imghgt = 0

# User-controlled variables
# text_scrolling(bool), is the text scrolling?
text_scrolling = True
# full_screen(bool), is the display fullscreen?
full_screen = False
# music_vol(bool), is the music playing(True) or muted(False)?
music_vol = True

scale = 30

cent_xy = [100, 100]

angle = 0

# all the cube vertices
points = np.array([[-1, -1, 1], [1, -1, 1], [1,  1, 1], [-1, 1, 1],
                   [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]])

projection_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0]
])

projected_points = [
    [n, n] for n in range(len(points))
]
