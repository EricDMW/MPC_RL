'''
Author: Dongming Wang wdong25@ucr.edu
Date: August 3rd, 2024
'''
import argparse

def get_config():
    '''
    Prameters for distributed optimization on Lie Group.
    
    Agents paramters:
        agents_num <int>: Number of agents;
        neighbors <list>: Neighbors of communication of agents;
        
    Learning parameters:
         
    
    '''
    
    parser = argparse.ArgumentParser(
        description='RL_MPC', formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Agents parameters
    parser.add_argument(
        '--agents_num',
        type=int,
        default=3,
        help='Number of agents.'
    )
    parser.add_argument(
        '--neighbors',
        type=int,
        default=[[],[1],[2]],
        help='neighbors of agents'
    )
    
    
    
    return parser