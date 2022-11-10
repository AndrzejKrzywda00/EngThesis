import numpy as np


# Saving position in 3 dimensional space
class Position3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, position3d):
        return np.sqrt(
            np.square(position3d.x - self.x) +
            np.square(position3d.y - self.y) +
            np.square(position3d.z - self.z)
        )

    def set_z(self, newZ):
        self.z = newZ
