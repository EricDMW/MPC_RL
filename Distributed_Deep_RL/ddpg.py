import torch
import torch.nn as nn

from ActorNet import ActorNet
from CriticNet import QCriticNet



from torch.storage import T
class DDPG(nn.Module):
    def __init__(self, config):
        super(DDPG,self).__init__()
        torch.manual_seed(config['seed'])

        self.lr_actor = config['lr_actor']  # learning rate
        self.lr_critic = config['lr_critic']
        self.smooth = config['smooth']  # smoothing coefficient for target net
        self.discount = config['discount']  # discount factor
        self.batch_size = config['batch_size']  # mini batch size
        self.sig = config['sig']  # exploration noise

        self.dims_hidden_neurons = config['dims_hidden_neurons']
        self.dim_obs = config['dim_obs']
        self.dim_action = config['dim_action']

        self.device = config['device']

        self.actor = ActorNet(dim_obs=self.dim_obs,
                              dim_action=self.dim_action,
                              dims_hidden_neurons=self.dims_hidden_neurons).to(self.device)
        self.Q = QCriticNet(dim_obs=self.dim_obs,
                            dim_action=self.dim_action,
                            dims_hidden_neurons=self.dims_hidden_neurons).to(self.device)
        self.actor_tar = ActorNet(dim_obs=self.dim_obs,
                                  dim_action=self.dim_action,
                                  dims_hidden_neurons=self.dims_hidden_neurons).to(self.device)
        self.Q_tar = QCriticNet(dim_obs=self.dim_obs,
                                dim_action=self.dim_action,
                                dims_hidden_neurons=self.dims_hidden_neurons).to(self.device)

        self.optimizer_actor = torch.optim.Adam(self.actor.parameters(), lr=self.lr_actor)
        self.optimizer_Q = torch.optim.Adam(self.Q.parameters(), lr=self.lr_critic)

        # new settings for better performatnce
        self.training_step = 0
        self.reward_scale = config['reward_scale']# scale of reward
        self.loss_func = nn.MSELoss()
        self.tau = config['tau']# target smooth coefiicient

    def update(self, buffer):
        # sample from replay memory
        t = buffer.sample(self.batch_size)


        # Extract the sampled transitions
        obs = t.obs
        action = t.action
        reward = t.reward
        next_obs = t.next_obs
        done = t.done

        self.training_step += 1

        self.update_Q(obs, action, next_obs, reward, done)
        self.update_Actor(obs)

    def update_Q(self, obs, action, next_obs, reward, done):
        next_action = self.actor_tar(next_obs)
        # y = self.reward_scale * reward + ~done * self.discount * self.Q_tar(next_obs, next_action)
        y = self.reward_scale * reward + torch.logical_not(done).float() * self.discount * self.Q_tar(next_obs, next_action)

        Q_value = self.Q(obs, action)
        loss = self.loss_func(y,Q_value)
        self.optimizer_Q.zero_grad()
        loss.backward(retain_graph=True)
        
        # Clip the gradients to the interval [-1, 1]
        for param in self.Q.parameters():
            if param.grad is not None:
                param.grad.data.clamp_(-1, 1)
                
        self.optimizer_Q.step()

        state_dict = self.Q.state_dict().copy()
        state_dict_ = self.Q_tar.state_dict().copy()

        for n, p in state_dict.items():
            state_dict_[n] = self.tau * p + (1-self.tau) * state_dict_[n]
        self.Q_tar.load_state_dict(state_dict_)

    def update_Actor(self,obs):
        action = self.actor(obs).clone()
        loss = torch.mean(-self.Q(obs,action))
        self.optimizer_actor.zero_grad()
        loss.backward(retain_graph=True)
        
        # Clip the gradients to the interval [-1, 1]
        for param in self.actor.parameters():
            
            if param.grad is not None:
                # if torch.max(param.grad.data) > 10:
                #     print('gradient blows up')
                param.grad.data.clamp_(-1, 1)
        
        self.optimizer_actor.step()
        state_dict = self.actor.state_dict().copy()
        state_dict_ = self.actor_tar.state_dict().copy()
        for n, p in state_dict.items():
            state_dict_[n] = self.tau * p + (1-self.tau) * state_dict_[n]
        self.actor_tar.load_state_dict(state_dict_)





    def act_probabilistic(self, obs: torch.Tensor):
        self.actor.eval()
        exploration_noise = torch.normal(torch.zeros(size=(self.dim_action,)), self.sig).to(self.device)
        a = self.actor(obs) + exploration_noise
        self.actor.train()
        return a

    def act_deterministic(self, obs: torch.Tensor):
        self.actor.eval()
        a = self.actor(obs)
        self.actor.train()
        return a

    def save_model(self):
        # Save the model
        policy_actor = self.actor
        torch.save(policy_actor.state_dict(), "Distributed_Deep_RL/model" + "/actor.pt")
        
        policy_critic = self.Q
        torch.save(policy_critic.state_dict(), "Distributed_Deep_RL/model" + "/critic.pt")
        
