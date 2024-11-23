'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''
import numpy as np
from get_A_follower import get_A_follower

def Distance_follower(p, v, a, es, ElcMap, p1, v1, bcu, peor, StpFlag):
    t = 25  # Total time duration, 25 seconds
    st = 0.05  # Time step, 0.05 seconds

    # Initializing position, velocity, and acceleration lists
    V = [v]
    P = [p]
    A = []

    for i in range(1, int(t / st)):
        if V[i - 1] <= 0:
            A.append(0)
        else:
            A.append(get_A_follower(a, i - 1, P[i - 1], V[i - 1], es, ElcMap, p1, p, bcu, peor))

        if V[i - 1] < 0:
            V[i - 1] = 0

        V.append(V[i - 1] + A[-1] * st)
        P.append(P[i - 1] + V[i - 1] * st)

    A.append(A[-1])

    return np.array(P), np.array(V), np.array(A)

# The function get_A_follower needs to be defined.
