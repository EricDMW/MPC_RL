import sys
import torch

import matplotlib as plt
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


from System_model.NlFuncGap import NlFuncGap
from light_mappo.envs.env_continuous import ContinuousActionEnv

# def main():
#     env = ContinuousActionEnv()
#     env.reset()
#     start_state = env.env.agent_state
#     agent_num = 3
#     time_step = 800
#     state_record = []
#     state_record.append(start_state[0])
#     dt = 0.2
#     for step in range(time_step):
#         for i in range(agent_num):
#             updated_state = NlFuncGap(dt,start_state[i],0,0,15)
#             start_state[i] = torch.tensor(updated_state)
#         state_record.append(start_state[0])
        
#         print(list(start_state[0]))
        
#     plt.plot(torch.norm())


def main():
    x = torch.tensor([0,0,0,0,15,0,2])
    dt = 0.2
    y = NlFuncGap(dt,x,0,0,15)
    print(y)
        
    
    

if __name__ == '__main__':
    main()