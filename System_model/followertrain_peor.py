'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''
def followertrain_peor(shead, ydq):
    minpeor = 1.17  # Minimum peor value
    
    # Initialize peor
    peor = minpeor

    # Determine peor based on shead position
    for i in range(1, len(ydq[0])):
        if shead <= ydq[0, i]:
            peor += (shead - ydq[0, i - 1]) * 0.02
            break
        elif shead >= ydq[0, -1]:
            peor += (shead - ydq[0, -1]) * 0.02
            break

    return peor
