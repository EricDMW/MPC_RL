#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File   : network_para.py
@Author : Dongming Wang
@Email  : dongming.wang@email.ucr.edu
@Project: MPC
@Date   : 11/27/2024
@Time   : 11:49:37
@Info   : Description of the script
"""


def get_config(device):
   config_1 = {
        'dim_obs': 33,
        'dim_action': 3,
        'dims_hidden_neurons': (128,256,512,512,256,128), # lower capacity, higher convergence speed
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

