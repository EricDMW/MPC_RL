'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 1st, 2024
'''
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
# sys.path.append(str(Path(__file__).resolve().parent.parent))
# from light_mappo.envs.env_continuous import ContinuousActionEnv
# from System_model.NlFuncGap import NlFuncGap
from centralized_env.env_continuous import ContinuousActionEnv

def env_built():
    # env = gym.make('LunarLanderContinuous-v2')
    env = ContinuousActionEnv()
    return env

def get_args(device):
    
    # maintain loss at around 20: norm of control error smaller than 1, training time 6h
    config_1 = {
        'dim_obs': 33,
        'dim_action': 3,
        'dims_hidden_neurons': (128,256,512,512,256,128), # lower capacity, higher convergence speed
        'lr_actor': 0.00001,#0.0001
        'lr_critic': 0.00001,#0.0001
        'smooth': 0.99,
        'discount': 0.99,
        'sig': 0.9,# 0.9 # define the exploration
        'batch_size': 128,
        'replay_buffer_size': 50000,
        'seed': 7,
        'max_episode': 500,
        'device':device,
        'reward_scale': 1,
        'tau':0.005

    }
    
    # maintain loss at around 12: norm of control error smaller than .5, training time 17h
    # Attention: perform relatively worse at beginning, but better after about 250 epoches
    config_2 = {
        'dim_obs': 33,
        'dim_action': 3,
        'dims_hidden_neurons': (64,128,256,256,256,512,512,256,256,256,128,64), # higher capacity, lower convergence speed
        'lr_actor': 0.000001, # very sensitive, influence convergence
        'lr_critic': 0.000001, # very sensitive, influence convergence
        'smooth': 0.99,
        'discount': 0.99,
        'sig': 0.9,# define the exploration
        'batch_size': 128,
        'replay_buffer_size': 50000, # sensitive, influence convergence
        'seed': 7,
        'max_episode': 500,
        'device':device,
        'reward_scale': 1,
        'tau':0.005 # not very sensitive, influcence convergence

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
    
    return config_1


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
    
    # environment building    
    env = env_built()
    
    # traning parameters
    config = get_args(device)
    
    # training agent
    ddpg = DDPG(config).to(device)
    buffer = ReplayBuffer(config)
    
    # Define the log directory
    log_dir = 'tensorboard/ddpg'
    # Create the directory if it does not exist
    os.makedirs(log_dir, exist_ok=True)
    train_writer = SummaryWriter(log_dir=log_dir)
    
    # record the return
    episodic_return = []
    # output flag

    
    for i_episode in trange(config['max_episode']):
        # obs = env.reset()[0]
        obs = env.reset()
        done = False
        truncated = False
        
        # decay exploration
        if i_episode % 100 == 0:
            ddpg.sig *= 0.4
            tqdm.write('exploration rate updated, current exploration rate {}'.format(ddpg.sig))
        
        # use dedayed learning rate or not    
        # if (i_episode + 1) % 200 == 0:
        #     ddpg.lr_actor /= 10 
        #     tqdm.write('current actor leaning rate {}'.format(ddpg.lr_actor))
            
        #     ddpg.lr_critic /= 10 
        #     tqdm.write('critic actor leaning rate {}'.format(ddpg.lr_critic))
        
 
        ret = 0.
        flag_lenth = 0
        while done is False and truncated is False:
            
            # use render or not
            # env.render()


            obs_tensor = torch.tensor(obs).type(Tensor).to(device)

            action = ddpg.act_probabilistic(obs_tensor[None, :]).detach().cpu().numpy()[0, :]

            next_obs, reward, done, truncated, info = env.step(action)

            buffer.append_memory(obs=obs_tensor,
                                action=torch.from_numpy(action),
                                reward=torch.from_numpy(np.array([reward])),
                                next_obs=torch.from_numpy(np.array(next_obs)).type(Tensor),
                                done=done)
            
            ddpg.update(buffer) 
            
            flag_lenth += 1

            ret += reward

            obs = copy.deepcopy(next_obs)

            if done or truncated:
                tqdm.write("Episode {} return {} steps {}".format(i_episode, ret/env.env.step_lenth, env.env.step_lenth))
        
           
        train_writer.add_scalar('Performance/episodic_return', ret/flag_lenth, i_episode)
        episodic_return.append(ret)
    ddpg.save_model()

    env.close()
    train_writer.close()

    
    

    
    
    
    
    
    
    

if __name__ == "__main__":
    main()


