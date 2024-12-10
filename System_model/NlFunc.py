'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''
import numpy as np
from dEBI import dEBI

def NlFunc(dt, x, u, ElcMap, v_r):
    # prestabilized controller
    # K=[0.01,0.1,0.15,0.6,0,0,0]
    # u_pre=K[0] * x[0] + K[1] * x[1] + K[2] * x[2] + K[3] * x[3] + K[4] * (v_r - x[4]) + K[5] * x[5] + K[6] * x[6]  #TODO
    u_pre = 0
    # Unpack state vector and inputs
    v1 = x[1] + x[4]
    v2 = x[4]
    f1 = x[3] + x[6]
    f2 = x[6]
    a1 = x[2] + x[5]
    a2 = x[5]

    # Compute the derivatives
    dx = np.zeros(7)
    
    dx[6] = x[6] + dt * (u[1] + u_pre)
    dx[5] = x[5] + dt * (x[6] - x[5]) / 0.7
    dx[4] = x[4] + dt * x[5]
    dx[3] = x[3] + dt * (u[0] - (u[1] + u_pre))

    dx[2] = x[2] + dt * (x[3] - x[2]) / 0.7

    dx[1] = x[1] + dt * x[2]

    # Compute the new velocities, forces, and accelerations
    dv1 = dx[1] + dx[4]
    dv2 = dx[4]
    df1 = dx[3] + dx[6]
    df2 = dx[6]
    da1 = dx[2] + dx[5]
    da2 = dx[5]

    # Compute the disturbances
    d = dEBI(1000, v1, v2 + 5 / 3.6, a1, a2, 0.23, 0, ElcMap, 0)
    dd = dEBI(1000, dv1, dv2 + 5 / 3.6, da1, da2, 0.23, 0, ElcMap, 0)
    
    # Update state vector
    # TODO: update the model by a linear version
    # dx[0] = x[0] + d - dd + dt * x[1]
    dx[0] = x[0] + dt * x[1]

    return dx

# Example usage
# dt = 0.1
# x = np.array([0, 0, 0, 0, 0, 0, 0])
# u = np.array([0, 0])
# ElcMap = np.array([...])  # Define your ElcMap as needed
# dx = NlFunc(dt, x, u, ElcMap)

