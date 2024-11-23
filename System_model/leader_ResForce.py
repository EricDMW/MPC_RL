'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''

import numpy as np

def leader_ResForce(s, smaxhead, ElcMap):
    # Constants and initial values
    shead = smaxhead * 100
    stail = s * 100
    j = 0

    # Find the tail and head buffer indices
    tailbuff = None
    headbuff = None

    for i in range(1, len(ElcMap[0])):
        if stail < ElcMap[0][i]:
            tailbuff = i - 1
            break

    for i in range(1, len(ElcMap[0])):
        if shead < ElcMap[0][i]:
            headbuff = i - 1
            break

    if tailbuff is None or headbuff is None:
        raise ValueError("Could not find appropriate tailbuff or headbuff")

    # Calculate slope buffer values
    slopebuff = []

    for i in range(tailbuff + 1, headbuff):
        slopebuff.append(ElcMap[1][i])
        j += 1

    # Handle tail left and right calculations
    if tailbuff == 0:
        tailleft = 0
    else:
        tailleft = abs(ElcMap[1][tailbuff - 1] - ElcMap[1][tailbuff]) * (ElcMap[2][tailbuff] / 20000)

    if tailbuff == len(ElcMap[0]) - 1:
        tailright = 0
    else:
        tailright = abs(ElcMap[1][tailbuff] - ElcMap[1][tailbuff + 1]) * (ElcMap[2][tailbuff] / 20000)

    # Determine tailslope
    if stail >= ElcMap[1][tailbuff] and stail < ElcMap[1][tailbuff] + tailleft:
        if ElcMap[1][tailbuff - 1] > ElcMap[1][tailbuff]:
            tailslope = ElcMap[1][tailbuff] + ((tailleft + stail - ElcMap[0][tailbuff]) / ElcMap[2][tailbuff])
        else:
            tailslope = ElcMap[1][tailbuff]
    elif stail >= ElcMap[1][tailbuff + 1] - tailright and stail < ElcMap[1][tailbuff + 1]:
        if ElcMap[1][tailbuff] > ElcMap[1][tailbuff + 1]:
            tailslope = ElcMap[1][tailbuff] + ((tailright + ElcMap[0][tailbuff + 1] - stail) / ElcMap[2][tailbuff + 1])
        else:
            tailslope = ElcMap[1][tailbuff] + (tailright / ElcMap[2][tailbuff + 1])
    else:
        tailslope = ElcMap[1][tailbuff]

    # Handle head left and right calculations
    if headbuff == 0:
        headleft = 0
    else:
        headleft = abs(ElcMap[1][headbuff - 1] - ElcMap[1][headbuff]) * (ElcMap[2][headbuff] / 20000)

    if headbuff == len(ElcMap[0]) - 1:
        headright = 0
    else:
        headright = abs(ElcMap[1][headbuff] - ElcMap[1][headbuff + 1]) * (ElcMap[2][headbuff] / 20000)

    # Determine headslope
    if shead >= ElcMap[1][headbuff] and shead < ElcMap[1][headbuff] + headleft:
        if ElcMap[1][headbuff - 1] > ElcMap[1][headbuff]:
            headslope = ElcMap[1][headbuff] + (headleft / ElcMap[2][headbuff - 1])
        else:
            headslope = ElcMap[1][headbuff] + ((headleft + shead - ElcMap[1][headbuff]) / ElcMap[2][headbuff - 1])
    elif shead >= ElcMap[1][headbuff + 1] - headright and shead < ElcMap[1][headbuff + 1]:
        if ElcMap[1][headbuff] > ElcMap[1][headbuff + 1]:
            headslope = ElcMap[1][headbuff] + ((headright + ElcMap[1][headbuff + 1] - shead) / ElcMap[2][headbuff + 1])
        else:
            headslope = ElcMap[1][headbuff] + (headright / ElcMap[2][headbuff + 1])
    else:
        headslope = ElcMap[1][headbuff]

    # Final slope calculation
    slopebuff.append(tailslope)
    slopebuff.append(headslope)

    slope = max(slopebuff) / 10
    if slope < 0:
        slope = 0

    SlpA = 9.81 * slope / 1000
    aF = -SlpA

    return aF

