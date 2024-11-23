'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''

def SolverOfThreeOrderFunction(a, b, c, d, K):
    if d >= 1.2179 * K:
        return 1.2
    elif d == 0:
        return 0
    else:
        x1 = 0
        x2 = 1.2

        def cubic_function(x):
            return (a * x + b) * x**2 + c * x + d

        fx1 = cubic_function(x1)
        fx2 = cubic_function(x2)

        flag2 = True
        while flag2:
            x0 = (x1 + x2) / 2
            fx0 = cubic_function(x0)

            if fx0 * fx1 < 0:
                x2 = x0
                fx2 = fx0
            else:
                x1 = x0
                fx1 = fx0

            if abs(fx0) < 1e-2:
                flag2 = False

        return x0


