'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 3rd, 2024
'''
import numpy as np

def SpdLmtElcMap(s1, v1, a1, s2, ElcMap):
    """
    Calculate the speed limit based on the elevation map.

    Args:
    - s1: Initial position (in kilometers)
    - v1: Initial velocity (in meters per second)
    - a1: Initial acceleration (not used in the calculation)
    - s2: Final position (in kilometers)
    - ElcMap: A numpy array with elevation map data [position, slope, ?, speed_limit]

    Returns:
    - SpdLmt: Speed limit (in meters per second)
    """
    SpdMarg = 3
    umin = -0.8
    L = 94.64

    EndPos = s1 + v1**2 / 2
    StartPos = s2 - L
    HeadPos = s1

    StartFlag, EndFlag, HeadFlag = True, True, True
    i = 1

    while StartFlag or EndFlag:
        if StartFlag and StartPos <= ElcMap[0, i] / 100:
            StartFlag = False
            StartInd = i - 1
        if HeadFlag and HeadPos <= ElcMap[0, i] / 100:
            HeadFlag = False
            HeadInd = i - 1
        if EndFlag and EndPos <= ElcMap[0, i] / 100:
            EndFlag = False
            EndInd = i - 1
        i += 1

    IniSpdLmt = min(ElcMap[3, StartInd:HeadInd + 1]) / 100 - SpdMarg
    SpdLmt = IniSpdLmt

    for i in range(HeadInd + 1, EndInd + 1):
        if ElcMap[3, i] / 100 - SpdMarg < IniSpdLmt:
            SpdLmtAux = np.sqrt((ElcMap[3, i] / 100 - SpdMarg)**2 +
                                ((ElcMap[0, i] / 100 - s1) * 2 * -umin))
            SpdLmt = min(SpdLmtAux, SpdLmt)

    return SpdLmt
