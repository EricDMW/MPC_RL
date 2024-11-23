'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 3rd, 2024
'''
import numpy as np

def ResForce(s, v, ElcMap):
    """
    TBD: Explaination of this code
    """
    m = 160000  # Mass in kg

    # Coefficients
    a = 3.558
    b = 0.02143
    c = 0.00065

    # Find index SInd where ElcMap[0, :] <= s * 100
    SInd = np.where(ElcMap[0, :] <= s * 100)[0][-1]

    # Calculate resistance forces
    EssA = (a + b * v * 3.6 + c * (v * 3.6)**2) * 1000 / m
    SlpA = 9.81 * ElcMap[1, SInd] / 1000
    CrvA = 6.38 / (max(ElcMap[2, SInd] * 100, 300) - 55)

    # Total resistance force
    aF = -(EssA + SlpA + CrvA)

    return aF
