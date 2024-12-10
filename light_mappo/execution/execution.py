# -*- coding: utf-8 -*-
import sys
import os
import socket
import setproctitle
import numpy as np
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.io import savemat
# Setting the dir for config
parent_dir = os.path.abspath(os.path.join(os.getcwd(), "."))
print(parent_dir)
sys.path.append(parent_dir)

from pathlib import Path
from light_mappo.config import get_config
from light_mappo.envs.env_wrappers import DummyVecEnv
from light_mappo.envs.env_continuous import ContinuousActionEnv
from light_mappo.algorithms.algorithm.r_actor_critic import R_Actor, R_Critic
from light_mappo.algorithms.algorithm.rMAPPOPolicy import RMAPPOPolicy as Policy
from light_mappo.algorithms.algorithm.r_mappo import RMAPPO as TrainAlgo
import pdb

# add env parameters
def parse_args(args, parser):
    parser.add_argument("--scenario_name", type=str, default="MyEnv", help="Which scenario to run on")
    # parser.add_argument("--num_landmarks", type=int, default=3, hlep="Choose number of landmaks")
    parser.add_argument("--agent_num", type=int, default=3, help="number of agents")

    all_args = parser.parse_known_args(args)[0]

    return all_args
    


def main(args):
    # Configure
    device = torch.device('cpu')

    parser = get_config()
    all_args = parse_args(args, parser)
    

    # set the environment
    envs = ContinuousActionEnv()

    share_observation_space = envs.share_observation_space[0] if all_args.use_centralized_V else envs.observation_space[0]

    policy = []
    for agent_id in range(all_args.agent_num):
            share_observation_space = (
                envs.share_observation_space[agent_id]
                if all_args.use_centralized_V
                else envs.observation_space[agent_id]
            )
            # policy network
            po = Policy(
                all_args,
                envs.observation_space[agent_id],
                share_observation_space,
                envs.action_space[agent_id],
                device=device,
            )
            policy.append(po)

    trainer = []
    for agent_id in range(all_args.agent_num):
        # algorithm
        tr = TrainAlgo(all_args, policy[agent_id], device=device)
        
        share_observation_space = (
            envs.share_observation_space[agent_id]
            if all_args.use_centralized_V
            else envs.observation_space[agent_id]
        )
        
        trainer.append(tr)
    
    #actor[i] is the loaded model for agent i
    actor_load = []
    model_dir = '/home/dongmingwang/project/Data_Driven_MPC/light_mappo/results/MyEnv/MyEnv/mappo/check/run24/models/actor_agent'
    for agent_id in range(all_args.agent_num):
        model = trainer[agent_id].policy.actor
        check_point = torch.load(model_dir+f'{agent_id}.pt',weights_only=True)
        model.load_state_dict(check_point)
        actor_load.append(model)
    

    
    
    rnn_states = torch.zeros((1,64))
    masks = torch.ones((1,6))
    # R_Actor
    obs = envs.env.reset()
    timesteps = 800
    
    rewards = []
    obs_record = []
    for k in range(timesteps):
        actions = []
        for i in range(all_args.agent_num):
            obs_i = torch.tensor(obs[i]).unsqueeze(0)
            action = actor_load[i](obs_i, rnn_states = rnn_states, masks = masks, deterministic=True)[0]
            # act_np = np.squeeze(action[0].detach().numpy())
            action = action.detach().numpy()
            action = np.clip(action, -1, 1)
            actions.append(action)
        obs, reward, dones, infos = envs.env.step(actions)
        obs_record.append(np.array(obs).copy())
        # print(obs[1])
        rewards.append(reward)



    
    savemat('Cruising.mat', {'tensor': obs_record})

    # Set plot labels and title
    plt.figure()
    
    plt.plot(np.array(rewards)[:,0,:])


    # Save the plot as PNG
    
    plt.plot(np.array(rewards)[:,1,:])
    
    plt.plot(np.array(rewards)[:,2,:])
    plt.savefig('agent_trajectories_3.png')
    plt.close()
    
    plt.figure()
    plt.plot(np.array([np.array(obs_record)[:,0,1]]).T)
    plt.plot(np.array([np.array(obs_record)[:,1,1]]).T)
    plt.plot(np.array([np.array(obs_record)[:,2,1]]).T)

    plt.savefig('state_traj_varying_d')
    plt.close()
    
    plt.figure()
    plt.plot(np.array([np.array(obs_record)[:,0,5]]).T)
    plt.plot(np.array([np.array(obs_record)[:,1,5]]).T)
    plt.plot(np.array([np.array(obs_record)[:,2,5]]).T)

    plt.savefig('state_traj_varying_v')
    plt.close()

    

    
    
    

if __name__ == "__main__":
    main(sys.argv[1:])
