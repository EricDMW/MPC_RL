'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''
def get_leaderhead(s, v, peor, trainlength):
    slope = -28.5  # The slope of the incline (negative indicates a downhill slope)
    a = 0.8 - 9.81 * slope / 1000
    head = s + trainlength + v**2 / (2 * a) + 2 * peor
    return head

