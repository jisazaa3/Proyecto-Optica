import os
import time

import matplotlib.pyplot as plt
import matplotlib.image as img
from matplotlib_scalebar.scalebar import ScaleBar, SI_LENGTH
import numpy as np

class OpticalSystem:

    def _init(self):
        self.A = [0, 0, 0]
        self.A[0] = np.eye(2)
        self.A[1] = np.eye(2)
        self.A[2] = np.eye(2)

        self.d0 = None

    def load(self, image_name, image_height  = 6000000):
        