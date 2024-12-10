import numpy as np
import random
import torch
import sys
from pathlib import Path


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
        
        # bonus withold
        self.bonus_withhould = 0.05
        # bonus value
        self.bonus = 100

        # Control parameters
        self.K = [0.01,0.1,0.15,0.6,0,0,0]
        
        
        
        # if execution
        self.execution = False
        
        self.flag = False
        
        ##############lxl-speed-varying    
        # initialization for time instant
        self.timeinst = 1
        # initialization for the virtual state of the leader
        self.x0 = torch.zeros([self.state_dim])
        self.x0[-3] = self.v_r 
        ##############lxl-speed-varying    
        
        # parameters of env
        self.dt = 0.2
        # record the process of training
        self.done = False
        # give the truncated condition
        self.Truncated = False
        # self.w = -1
       
        
        self.vr_range = [i for i in range(10,21)]
        
        
        
        self.initial_control_input = torch.zeros(self.agent_num,)
        

    def reset(self):
        
        self.flag = [False, False, False]
        
        # Question: why do we need to set the vr=15 here
        sub_agent_obs = []
        # self.v_r = random.choice(self.vr_range)
        self.v_r = 15
        self.timeinst =1
        
        self.target = torch.zeros(self.state_dim)
        self.target[4] += self.v_r
        
        self.agent_state = torch.zeros([self.agent_num,self.state_dim]) # 3*7
        
        for i in range(self.agent_num):
            ###################lxl
            self.agent_state[i][0] = 10#if cruising
            # self.agent_state[i][0] = 0#if speed-varying
            self.agent_state[i][-3] = self.v_r
            ###################lxl
        
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
        
        return sub_agent_obs

    def step(self, actions):
        """
        Update Dimension of agents: 3*11, include the obs of itself and agents
        """
        ############lxl   
        #f speed-varying operation
        # if self.timeinst >= 31 and self.timeinst <= 50:
        #     newx0=NlFuncGap(self.dt, self.x0, 0, 0.125/2, self.v_r)
        # elif self.timeinst >= 51 and self.timeinst <= 70:
        #     newx0=NlFuncGap(self.dt, self.x0, 0, -0.125/2, self.v_r)
        # elif self.timeinst >= 231 and self.timeinst <= 250:
        #     newx0=NlFuncGap(self.dt, self.x0, 0, -0.125/2, self.v_r)
        # elif self.timeinst >= 251 and self.timeinst <= 270:
        #     newx0=NlFuncGap(self.dt, self.x0, 0, 0.125/2, self.v_r)
        # else:
        #     newx0=NlFuncGap(self.dt, self.x0, 0, 0, self.v_r)
        # self.x0 = torch.tensor(newx0)
        # self.v_r = self.x0[4]#speed-varying #cruising
        ############lxl   
        
         
        
        # for i in range(self.agent_num):#TODO
        #     u_pre = self.K[0] * self.agent_state[i][0] + self.K[1] * self.agent_state[i][1] + self.K[2] *\
        #         self.agent_state[i][2] + self.K[3] * self.agent_state[i][3] + self.K[4] * (self.v_r -\
        #             self.agent_state[i][4]) + self.K[5] * self.agent_state[i][5] + self.K[6] * self.agent_state[i][6]
                
        #     # actions[i] = actions[i] + np.array(u_pre)
        #     if self.execution:
        #         if abs(self.agent_state[i][0]) < 0.1:
        #             self.flag[i] = True
                    
        #         if self.flag[i]:
        #             actions[i] = np.array(u_pre)
        #         else:
        #             actions[i] = actions[i]
        #     else:
        #         actions[i] = actions[i]
        #         # actions[i] = np.array(u_pre)
        #         # actions[i] = 0
        
        ############lxl   
        #timer
        # self.timeinst = self.timeinst + 1
        ############lxl   
        
        
        


            
        sub_agent_done = []
        sub_agent_info = []
        for i in range(self.agent_num):
            sub_agent_done.append(False)
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
        
        

        return [sub_agent_obs, sub_agent_reward, sub_agent_done, sub_agent_info]
    
    
    def get_reward(self,actions):
        '''
        Reward Function: defined as x[:4]=0, x[4] = v_r, x[5:] = 0
        '''
        
        for i in range(self.agent_num):
            ############3lxl
            if i == 0:
                # if self.timeinst >= 31 and self.timeinst <= 50:
                #     w=0.125/2
                # elif self.timeinst >= 51 and self.timeinst <= 70:
                #     w=-0.125/2
                # elif self.timeinst >= 231 and self.timeinst <= 250:
                #     w=-0.125/2
                # elif self.timeinst >= 251 and self.timeinst <= 270:
                #     w=0.125/2
                # else:
                #     w=0
                w=0#cruising case
            ############3lxl
            else:
                w = actions[i-1]
                
            newstate = NlFuncGap(self.dt, self.agent_state[i], w, actions[i], self.v_r)
            
            if newstate[6] > 1:
                newstate[6] = 1
            elif newstate[6] < -1:
                newstate[6] = -1
                
            
            self.agent_state[i] = torch.tensor(newstate)
        
        
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

            
        reward_bonus = []
        for i in range(self.agent_num):
            bonus = (torch.norm((self.agent_state[i] - self.target).clone().detach()) < self.bonus_withhould) * self.bonus

            reward_bonus.append(bonus)
            
        
        
        
        rewards = [i + j + k + l for i, j, k, l in zip(reward_control,reward_force,reward_speed,reward_bonus)]
        
    
        
        rewards = [[reward] for reward in rewards]
        
        
        return rewards
        

        
    def truncated(self):
        pass
        
