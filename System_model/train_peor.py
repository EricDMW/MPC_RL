'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 3rd, 2024
'''
import numpy as np

def train_peor(shead, ydq):
    """
    Calculate a value based on the given position 'shead' and the array 'ydq'.

    Args:
    - shead: The current position.
    - ydq: A 2D numpy array where the first row contains positions.

    Returns:
    - aF: Calculated value based on 'shead' and 'ydq'.
    """
    minpeor = 1.1  # Minimum value
    peor = minpeor
    
    for i in range(1, ydq.shape[1]):
        if shead <= ydq[0, i]:
            peor = minpeor + (shead - ydq[0, i-1]) * 0.02
            break
        if shead >= ydq[0, -1]:
            peor = minpeor + (shead - ydq[0, -2]) * 0.02
            break
    
    aF = peor
    return aF
