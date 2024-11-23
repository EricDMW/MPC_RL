
import numpy as np
import sys
from pathlib import Path
import torch

# Add the parent directory to the sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from System_model.NlFuncGap import NlFuncGap


# from System_model.NlFuncGap import NlFuncGap


# Example usage
# x = np.zeros(7)
# w = -1
# u = 1
# dt = 0.2

# # Compute the next state
# x_next = NlFuncGap(dt, x, w, u)
# print(x_next)
a = torch.zeros(7)
print(a)
a[4] += 5
print(a)



# x = torch.zeros([2,3])
# print(x)
# x = x.flatten()
# print(x)

# x = [[1,2],[3,4]]

# x = torch.tensor(x)
# y = torch.flatten(x)
# print(y)