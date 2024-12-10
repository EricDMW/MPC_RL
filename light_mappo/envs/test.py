import numpy as np
import sys
from pathlib import Path
import random
import time

# Add the parent directory to the sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from System_model.NlFuncGap import NlFuncGap


# from System_model.NlFuncGap import NlFuncGap


a = np.array([0,0,0])
b = np.array([])

b = np.append(b,a)
print(a)



# Example usage
x = [1000,0,0,0,15,0,0.5]
w = -1
u = 1
dt = 0.2


# # Compute the next state
# start = time.time()
# x_next = NlFuncGap(dt, x, w, u)
# end = time.time()
# print(start-end)
# print(x_next)

y = [1,1,1,1,1,1,1]
result = [a * b for a,b in zip(x, y)]
print(result)

test = (2>1)*5
print(test)
print(20e4)
# vr_range = [i for i in range(10,21)]
# sub_agent_obs = []
# v_r = random.choice(vr_range)
# x_0 = np.array([0,0,0,0,v_r,0,0])
# print(type(x_0))
        
# for i in range(3):
#     sub_agent_obs.append(x_0)

# dt = [.2]

# x = [0,1]
# print(dt+x)


# def f(x):
#     return x**2

# b = [f(i) for i in range(5)]


# a = -np.random.rand(5,)
# print(np.linalg.norm(a))

