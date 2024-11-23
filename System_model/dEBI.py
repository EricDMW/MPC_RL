'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''

import numpy as np
from Distance_leader import Distance_leader
from Distance_follower import Distance_follower


def dEBI(p1, v1, v2, a1, a2, es, peor, ElcMap, bcu):
    veor = 2.6  # Speed error in ‰ (per mile)
    inveor = 0.26  # Fixed speed error in m/s
    aeor = 0.31  # Acceleration error in m/s²

    p1 = p1 - peor
    v1 = v1 * (1 - veor / 1000) - inveor
    v2 = v2 * ((1000 + veor) / 1000) + inveor

    a1 = a1 - 0.332
    a2 = a2 + 0.240

    es_leader = 0.123
    trainlength = 94.64

    P1, V1, A1 = Distance_leader(p1, v1, a1, es_leader, ElcMap, bcu, peor)
    dis = 100
    dis_l = 0
    dis_h = 100
    f = 1
    Sm = 0
    StpFlag = 0

    
    P2, V2, A2 = Distance_follower(p1 - dis, v2, a2, es, ElcMap, P1[-1], v1, bcu, peor, StpFlag)
    d = np.array(P1) - np.array(P2)
    min_d = np.min(d)

    if (min_d - Sm < 0.01 and min_d >= Sm) or dis <= 0.01:
        f = 0
    else:
        dis += (Sm - min_d)

    headway = dis + 2 * peor
    return headway

# The following functions need to be defined:
# - Distance_leader
# - Distance_follower
