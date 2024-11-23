'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''

import numpy as np
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'System_model')))

from NlFuncGap import NlFuncGap


# from System_model.NlFuncGap import NlFuncGap


# Example usage
x = np.zeros(7)
w = -1
u = 1
dt = 0.2

# Compute the next state
x_next = NlFuncGap(dt, x, w, u)
print(x_next)
