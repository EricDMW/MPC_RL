import torch.nn as nn
import torch
import datetime
import copy

import numpy.random as nr
import numpy as np
import gymnasium as gym
from torch.utils.tensorboard import SummaryWriter


from typing import Tuple
from collections import namedtuple
from collections import deque

class ReplayBuffer(nn.Module):
    def __init__(self, config):
        super().__init__()
        replay_buffer_size = config['replay_buffer_size']
        seed = config['seed']
        self.device = config['device']
        nr.seed(seed)
        # setting the tensor type
        self.Tensor = torch.DoubleTensor
        torch.set_default_tensor_type(self.Tensor)
        self.Transitions = namedtuple('Transitions', ['obs', 'action', 'reward', 'next_obs', 'done'])

        self.replay_buffer_size = replay_buffer_size
        self.obs = deque([], maxlen=self.replay_buffer_size)
        self.action = deque([], maxlen=self.replay_buffer_size)
        self.reward = deque([], maxlen=self.replay_buffer_size)
        self.next_obs = deque([], maxlen=self.replay_buffer_size)
        self.done = deque([], maxlen=self.replay_buffer_size)

    def append_memory(self,
                      obs,
                      action,
                      reward,
                      next_obs,
                      done: bool):
        self.obs.append(obs)
        self.action.append(action)
        self.reward.append(reward)
        self.next_obs.append(next_obs)
        self.done.append(done)

    def sample(self, batch_size):
        buffer_size = len(self.obs)

        idx = nr.choice(buffer_size,
                        size=min(buffer_size, batch_size),
                        replace=False)
        t = self.Transitions
        t.obs = torch.stack(list(map(self.obs.__getitem__, idx))).to(self.device)
        t.action = torch.stack(list(map(self.action.__getitem__, idx))).to(self.device)
        t.reward = torch.stack(list(map(self.reward.__getitem__, idx))).to(self.device)
        t.next_obs = torch.stack(list(map(self.next_obs.__getitem__, idx))).to(self.device)
        t.done = torch.tensor(list(map(self.done.__getitem__, idx)))[:, None].to(self.device)
        return t

    def clear(self):
        self.obs = deque([], maxlen=self.replay_buffer_size)
        self.action = deque([], maxlen=self.replay_buffer_size)
        self.reward = deque([], maxlen=self.replay_buffer_size)
        self.next_obs = deque([], maxlen=self.replay_buffer_size)
        self.done = deque([], maxlen=self.replay_buffer_size)