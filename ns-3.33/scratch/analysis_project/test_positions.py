import math
import random as random

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    positions_x = []
    positions_y = []
    num = 1000
    rad = 0.003

    t = np.random.uniform(0.0, 2.0 * np.pi, num)
    r = rad * np.sqrt(np.random.uniform(0.0, 1.0, num))
    x = r * np.cos(t)
    y = r * np.sin(t)

    plt.scatter(x, y)
    plt.xlim(-2 * rad, 2 * rad)
    plt.ylim(-2 * rad, 2 * rad)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.show()
