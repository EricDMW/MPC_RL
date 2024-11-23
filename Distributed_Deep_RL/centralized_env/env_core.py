import numpy as np
import random
import torch
import sys
from pathlib import Path
from tqdm import tqdm


# Add the parent directory to the sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from System_model.NlFuncGap import NlFuncGap

class EnvCore(object):
    """
    # setting of agents
    """

    def __init__(self):
        self.agent_num = 3  # Number of Ageents: setted as 3 with communication structure 1->2->3
        self.obs_dim = 11  # Observation Space: [dt = 0.2, x\in R^7,
                         #target value = range(10,20), neighbors control input: 1, self control input:1] = 1+7+1+1+1=11
                         
        self.action_dim = 1  # Control Input: dimension 1
        
        self.control_withhold = 0.05
        
        self.state_dim = 7
        
        self.v_r = 15
        
        self.weight = [1, 10, 20, 30, 10, 20, 30]
        
        
            
        
        # parameters of env
        self.dt = 0.2
        # record the process of training
        self.done = False
        # give the truncated condition
        self.Truncated = False
        # self.w = -1
        self.step_lenth = 0
        self.boundaray_step_lenth = 600
        
        
        # in case of blow up
        self.upper_bound = 100
        
        # bonus withold
        self.bonus_withhould = 0.05
        # bonus value
        self.bonus = 10
       
        
        self.vr_range = [i for i in range(10,21)]
        
        
        
        self.initial_control_input = torch.zeros(self.agent_num,)
        

    def reset(self):
        
        # reset the parameters
        self.v_r = random.choice(self.vr_range)
        self.step_lenth = 0
        self.target = torch.zeros(self.state_dim)
        self.target[4] += self.v_r
        
        # reset the agent state
        self.agent_state = torch.zeros([self.agent_num,self.state_dim]) # 3*7
        
        for i in range(self.agent_num):
            self.agent_state[i][0] = 10
            self.agent_state[i][-3] = self.v_r
            
        sub_agent_obs = []
        
        for i in range(self.agent_num):
            current_agent_obs = []
            current_agent_obs.append(self.dt) # dt = 0.2
            # changing: v_r not equal to real v_r
            
            
            for elements in self.agent_state[i]:# states \in \mathbb{R}^7
                current_agent_obs.append(elements)
            current_agent_obs.append(self.v_r)# v_r
            
            if i == 0:
                control_input = 0
            else:
                control_input = self.initial_control_input[i-1]
            
            current_agent_obs.append(control_input)# neighor's control input
            
            current_agent_obs.append(self.initial_control_input[i])# control input
            
            sub_agent_obs.append(current_agent_obs)

        initial_state_detached = [item for sublist in sub_agent_obs for item in sublist]    

            
        return initial_state_detached

    def step(self, actions):
        """
        Update Dimension of agents: 3*11, include the obs of itself and agents
        """
        # sub_agent_done = []
        sub_agent_info = []
        for i in range(self.agent_num):
            # sub_agent_done.append(False)
            sub_agent_info.append({})
        
        # get the reward
        sub_agent_reward = self.get_reward(actions)
        
        # update the obs
        sub_agent_obs = []
        for i in range(self.agent_num):
            if i == 0:
                control_input = 0
            else:
                control_input = float(actions[i-1])
            current_agent_obs = []
            current_agent_obs.append(self.dt) # dt = 0.2
            for elements in self.agent_state[i]:# states \in \mathbb{R}^7
                current_agent_obs.append(elements)
            current_agent_obs.append(self.v_r) # v_r
            current_agent_obs.append(control_input)# neighor's control input
            current_agent_obs.append(float(actions[i]))
            sub_agent_obs.append(current_agent_obs)
            
        truc = self.truncated(sub_agent_obs[0]) or self.truncated(sub_agent_obs[1]) or self.truncated(sub_agent_obs[2])
        
        detached_obs = [item for sublist in sub_agent_obs for item in sublist]
        
        # Flatten the list to get all tensors in a single list
        flattened_reward = [item for sublist in sub_agent_reward for item in sublist]

        # Sum all the tensors in the flattened list
        total_reward = torch.sum(torch.stack(flattened_reward))

        done = self.if_done()
        
        # if done:
        #     tqdm.write('current step {}'.format(self.step_lenth))
        
        # blow up punishment
        if truc:
            # tqdm.write('state norm {}, {}, {}'.format(torch.norm(torch.tensor(sub_agent_obs[0])),torch.norm(torch.tensor(sub_agent_obs[1])),torch.norm(torch.tensor(sub_agent_obs[2]))))
            # total_reward -= (1-self.step_lenth / self.boundaray_step_lenth) * 3 * 10**2
            total_reward -= 300 * (self.boundaray_step_lenth-self.step_lenth)
        else:
            # total_reward += 3 * 100 * self.step_lenth/self.boundaray_step_lenth
            total_reward += 3 * 10
        
        
        if done:
            total_reward += 3 * 1000  
            
        return [detached_obs, total_reward, done, truc, sub_agent_info]
    
    
    def get_reward(self,actions):
        '''
        Reward Function: defined as x[:4]=0, x[4] = v_r, x[5:] = 0
        '''
        
        for i in range(self.agent_num):
            
            if i == 0:
                w = 0
            else:
                w = actions[i-1]
            
            # the last term indices the v_r position 
            newstate = NlFuncGap(self.dt, self.agent_state[i], w, actions[i], self.agent_state[i][4])
            
            self.agent_state[i] = torch.tensor(newstate)
            
        #TODO: check the updatea process
        self.step_lenth += 1
        
        # term -norm(x[:4]) 
        reward_control = []
        for i in range(self.agent_num):
            weighted_state = [a*b for a, b in zip(self.agent_state[i][:4],self.weight[:4])]
            reward_control.append(-torch.norm(torch.tensor(weighted_state).clone().detach()))
   
        # term -norm(x[4]-v_r)
        reward_speed = []
        for i in range(self.agent_num):
            reward_speed.append(-torch.norm((self.weight[4] * (self.agent_state[i][4] - self.v_r)).clone().detach()))

            
        # term -norm(x[5:])
        reward_force = []
        for i in range(self.agent_num):
            weighted_state = [a*b for a, b in zip(self.agent_state[i][5:],self.weight[5:])]
            reward_force.append(-torch.norm(self.agent_state[i][5:].clone().detach()))

        
        # bonus term
        reward_bonus = []
        for i in range(self.agent_num):
            bonus = (torch.norm((self.agent_state[i] - self.target).clone().detach()) < self.bonus_withhould) * self.bonus

            reward_bonus.append(bonus)
            
        
        
        
        rewards = [i + j + k + l for i, j, k, l in zip(reward_control,reward_force,reward_speed,reward_bonus)]
        
        rewards = [[reward] for reward in rewards]
        
        
        return rewards
        

        
    def truncated(self, state):
        if torch.norm(torch.tensor(state)) > self.upper_bound:
            return True
        else:
            return False
        
    
    def if_done(self):
        if self.step_lenth > self.boundaray_step_lenth:
            return True
        else: 
            return False
