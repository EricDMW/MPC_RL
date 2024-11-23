'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''
import numpy as np

def leadertrain_peor(shead, ydq):
    minpeor = 0.58  # Minimum peor value
    
    # Find the appropriate peor value based on shead
    for i in range(1, len(ydq[0])):
        if shead <= ydq[0][i]:
            peor = minpeor + (shead - ydq[0][i - 1]) * 0.02
            break
   
        if shead >= ydq[0][-1]:
            peor = minpeor + (shead - ydq[0][-2]) * 0.02
            break

    return peor


