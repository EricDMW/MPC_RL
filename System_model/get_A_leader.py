'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''
from SolverOfThreeOrderFunction import SolverOfThreeOrderFunction
def get_A_leader(a0, t, s, v, es, ElcMap, p0, v0, bcu, peor):
    st = 0.1
    B1 = -2.0221
    B2 = 0.83929
    B3 = 0
    C = 0.05
    amax = 1.2
    K = 1 + es
    T0 = 0.2
    T1 = 1.2
    T2 = 0.2
    T4 = 0
    k1 = 0
    k2 = 1 - k1

    trainlength = 94.64

    if a0 > 0:
        if t <= T0 / st:
            aq = 0
        else:
            aq = 0
    else:
        aq = 0

    if a0 < 0:
        if t <= T2 / st:
            ad = a0 * k1
        else:
            ad = 0
    else:
        ad = 0

    if a0 > 0:
        if t < T1 / st:
            ak = K * (B1 * (t * st) + B2 * (t * st)**2 + B3 * (t * st)**3 + C)
        elif t >= T1 / st and v > 10 / 3.6:
            ak = -1.223 * K
        elif t >= T1 / st and v > 0:
            ak = -1.223 * 1.3
        else:
            ak = 0
    elif a0 == 0:
        if t < T1 / st:
            ak = K * (B1 * (t * st) + B2 * (t * st)**2 + B3 * (t * st)**3 + C)
        elif t >= T1 / st and v > 10 / 3.6:
            ak = -1.223 * K
        elif t >= T1 / st and v > 0:
            ak = -1.223 * 1.3
        else:
            ak = 0
    else:
        # Placeholder for SolverOfThreeOrderFunction
        T3 = SolverOfThreeOrderFunction(K * B3, K * B2, K * B1, K * C - a0 * k2, K)
        if t <= T4 / st:
            ak = a0 * k2
        elif t < (T1 - T3 + T4) / st:
            ak = (K * B1 * (t * st + T3 - T4) + 
                  K * B2 * (t * st + T3 - T4)**2 + 
                  K * B3 * (t * st + T3 - T4)**3)
        elif t >= (T1 - T3 + T4) / st and v > 10 / 3.6:
            ak = -1.223 * K
        elif t >= (T1 - T3 + T4) / st and v > 0:
            ak = -1.223 * 1.3
        else:
            ak = 0

    # Placeholder for leader_ResForce function
    ac = 0

    az = aq + ad + ak + ac

    return az
