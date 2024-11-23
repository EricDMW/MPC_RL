'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''

import numpy as np

def follower_ResForce(s, smaxhead, ElcMap):
    # Conversion factors
    shead = smaxhead * 100
    stail = s * 100
    j = 0
    
    # Find the index where the tail of the train is located in ElcMap
    tailbuff = None
    for i in range(1, len(ElcMap[0])):
        if stail < ElcMap[0, i]:
            tailbuff = i - 1
            break
    
    # Find the index where the head of the train is located in ElcMap
    headbuff = None
    for i in range(1, len(ElcMap[0])):
        if shead < ElcMap[0, i]:
            headbuff = i - 1
            break

    # Extract slopes between tail and head
    slopebuff = []
    if tailbuff is not None and headbuff is not None:
        for i in range(tailbuff + 1, headbuff):
            slopebuff.append(ElcMap[1, i])
    
    # Calculate tail slope
    if tailbuff == 0:
        tailleft = 0
    else:
        tailleft = abs(ElcMap[1, tailbuff - 1] - ElcMap[1, tailbuff]) * (ElcMap[2, tailbuff] / 20000)

    if tailbuff == len(ElcMap[0]) - 1:
        tailright = 0
    else:
        tailright = abs(ElcMap[1, tailbuff] - ElcMap[1, tailbuff + 1]) * (ElcMap[2, tailbuff] / 20000)

    if stail >= ElcMap[1, tailbuff] and stail < ElcMap[1, tailbuff] + tailleft:
        if ElcMap[1, tailbuff - 1] > ElcMap[1, tailbuff]:
            tailslope = ElcMap[1, tailbuff]
        else:
            tailslope = ElcMap[1, tailbuff] + ((tailleft + stail - ElcMap[0, tailbuff]) / ElcMap[2, tailbuff - 1])
    elif stail >= ElcMap[1, tailbuff + 1] - tailright and stail < ElcMap[1, tailbuff + 1]:
        if ElcMap[1, tailbuff] > ElcMap[1, tailbuff + 1]:
            tailslope = ElcMap[1, tailbuff] + (tailright / ElcMap[2, tailbuff + 1])
        else:
            tailslope = ElcMap[1, tailbuff] + ((tailright + ElcMap[0, tailbuff + 1] - stail) / ElcMap[2, tailbuff + 1])
    else:
        tailslope = ElcMap[1, tailbuff]

    # Calculate head slope
    if headbuff == 0:
        headleft = 0
    else:
        headleft = abs(ElcMap[1, headbuff - 1] - ElcMap[1, headbuff]) * (ElcMap[2, headbuff] / 20000)

    if headbuff == 0:
        headright = 0
    else:
        headright = abs(ElcMap[1, headbuff] - ElcMap[1, headbuff + 1]) * (ElcMap[2, headbuff] / 20000)

    if shead >= ElcMap[1, headbuff] and shead < ElcMap[1, headbuff] + headleft:
        if ElcMap[1, headbuff - 1] > ElcMap[1, headbuff]:
            headslope = ElcMap[1, headbuff] + ((headleft + shead - ElcMap[1, headbuff]) / ElcMap[2, headbuff - 1])
        else:
            headslope = ElcMap[1, headbuff] + (headleft / ElcMap[2, headbuff - 1])
    elif shead >= ElcMap[1, headbuff + 1] - headright and shead < ElcMap[1, headbuff + 1]:
        if ElcMap[1, headbuff] > ElcMap[1, headbuff + 1]:
            headslope = ElcMap[1, headbuff] + (headright / ElcMap[2, headbuff + 1])
        else:
            headslope = ElcMap[1, headbuff] + ((headright + ElcMap[1, headbuff + 1] - shead) / ElcMap[2, headbuff + 1])
    else:
        headslope = ElcMap[1, headbuff]

    slopebuff.extend([tailslope, headslope])

    slope = min(slopebuff) / 10
    if slope > 0:
        slope = 0
    SlpA = 9.81 * slope / 1000
    aF = -SlpA

    return aF
