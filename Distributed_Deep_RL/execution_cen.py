#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File   : execution_cen.py
@Author : Dongming Wang
@Email  : dongming.wang@email.ucr.edu
@Project: MPC
@Date   : 11/26/2024
@Time   : 20:16:10
@Info   : for execution
"""

import numpy as np
import sys
import torch 
import os
import torch.nn as nn
import datetime
import copy
import numpy.random as nr
import numpy as np
import gymnasium as gym
from torch.utils.tensorboard import SummaryWriter
from typing import Tuple
from collections import namedtuple
from collections import deque
from ddpg import DDPG
from replaybuffer import ReplayBuffer
from tqdm import tqdm
from tqdm import trange
from pathlib import Path

import matplotlib.pyplot as plt
import tqdm
from tqdm import tqdm
from tqdm import trange

sys.path.append(str(Path(__file__).resolve().parents[2]))

# from light_mappo.envs.env_continuous import ContinuousActionEnv
# from System_model.NlFuncGap import NlFuncGap
from centralized_env.env_continuous import ContinuousActionEnv

def env_built():
    # env = gym.make('LunarLanderContinuous-v2')
    env = ContinuousActionEnv()
    return env

def get_args(device):


    config = {
        'dim_obs': 33,
        'dim_action': 3,
        'dims_hidden_neurons': (128,256,512,512,256,128),
        'lr_actor': 0.0001,
        'lr_critic': 0.0001,
        'smooth': 0.99,
        'discount': 0.99,
        'sig': 0.9,# define the exploration
        'batch_size': 128,
        'replay_buffer_size': 50000,
        'seed': 7,
        'max_episode': 500,
        'device':device,
        'reward_scale': 1,
        'tau':0.005

    }
    config_3 = {
        'dim_obs': 33,
        'dim_action': 3,
        'dims_hidden_neurons': (128,256,256,128), # lower capacity, higher convergence speed
        'lr_actor': 0.0001,
        'lr_critic': 0.0001,
        'smooth': 0.99,
        'discount': 0.99,
        'sig': 0.9,# define the exploration
        'batch_size': 128,
        'replay_buffer_size': 50000,
        'seed': 7,
        'max_episode': 500,
        'device':device,
        'reward_scale': 1,
        'tau':0.005

    }
    return config


def main():
    # Choose the device 
    if torch.cuda.is_available():
        os.environ["CUDA_VISIBLE_DEVICES"]="0"
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')
    print('Found device at: {}'.format(device))
    
    # ensure tensor
    
    Tensor = torch.DoubleTensor
    torch.set_default_tensor_type(Tensor)
    
    config = get_args(device)
    
    # environment building    
    env = env_built()
    
    ddpg = DDPG(config).to(device)
    
    policy = ddpg.actor
    policy.load_state_dict(torch.load("/home/dongmingwang/project/Data_Driven_MPC/Distributed_Deep_RL/model/actor.pt", map_location=device,weights_only=True))
    
    obs = env.env.reset()
    
    record = []
    for _ in trange(1000):
        
        obs_tensor = torch.tensor(obs).type(Tensor).to(device)
        action = ddpg.act_deterministic(obs_tensor[None, :]).detach().cpu().numpy()[0, :]
        next_obs, reward, done, truncated, info = env.step(action)
        if truncated:
            breakpoint()
        
        obs = next_obs.copy()
        
        
        record.append(np.array(obs[1]).copy())

    plt.plot(record)
    plt.savefig('record_trace.png')
    plt.show()
    
if __name__ == "__main__":
    main()