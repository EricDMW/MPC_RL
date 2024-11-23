'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''
import numpy as np
from get_A_leader import get_A_leader

def Distance_leader(p, v, a, es, ElcMap, bcu, peor):
    t = 25  # Total time duration, 25 seconds
    st = 0.05  # Time step, 0.05 seconds

    # Initializing position, velocity, and acceleration lists
    V = [v]
    P = [p]
    A = [get_A_leader(a, 1, P[0], V[0], es, ElcMap, p, v, bcu, peor)]

    for i in range(1, int(t / st)):
        if V[i - 1] <= 0:
            A.append(0)
        else:
            A.append(get_A_leader(a, i, P[i - 1], V[i - 1], es, ElcMap, p, v, bcu, peor))

        if V[i - 1] < 0:
            V[i - 1] = 0

        V.append(V[i - 1] + A[i] * st)
        P.append(P[i - 1] + V[i - 1] * st)

    return np.array(P), np.array(V), np.array(A)

# The function get_A_leader needs to be defined.
