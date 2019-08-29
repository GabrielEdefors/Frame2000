import math
import numpy as np
import tkinter as tk

from geometry_calculations import coordinates_parallel_line

def transversal_load(x1, y1, x2, y2, magnitude, direction, length, canvas_load):

    # The offset is proportional to the magnitude of the load
    k = 1
    offset = magnitude * k

    # Distance between load arrows
    dist_arrow = 1

    # Calculate the end coordinates for a parallel line with the offset deterimined by the magnitude of the load
    x1_loadline, y1_loadline, x2_loadline, y2_loadline, dummy, dummy = coordinates_parallel_line(x1, y1, x2, y2, length, offset, length)

    # Calculate how many arrows fit the element
    n_arrows = math.floor(length / dist_arrow)

    # Create equally spaced coordinates along the element length
    x_start_arrows = np.linspace(x1_loadline, x2_loadline, n_arrows)
    y_start_arrows = np.linspace(y1_loadline, y2_loadline, n_arrows)

    x_end_arrows = np.linspace(x1, x2, n_arrows)
    y_end_arrows = np.linspace(y1, y2, n_arrows)

    # Draw an arrow between each coordinate pair of the arrays created
    for i in range(0,n_arrows):
        canvas_load.create_line(x_start_arrows[i], y_start_arrows[i], x_end_arrows[i], y_end_arrows[i], arrow=tk.LAST)





