'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''

import numpy as np
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'System_model')))


from dEBI import dEBI
from NlFunc import NlFunc


def NlFuncGap(dt, x, w, u, v_r):
    # ElcMap as defined in the MATLAB code
    ElcMap = np.array([[0, 0, 0, 2222], [298303, 0, 0, 2222]]).T
    
    # Initialize
    xl = x.clone()
    
    
    w = float(w)
    u = float(u)
    ul = np.array([w, u])

    
    # Iteratively compute the next state
    for _ in range(int(dt / 0.05)):
        xl = NlFunc(0.05, xl, ul, ElcMap, v_r)
    
    dx = xl
    
    return dx

