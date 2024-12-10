import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.io import savemat

# Specify the path to your JSON file
json_file_path = '/home/dongmingwang/project/Data_Driven_MPC/light_mappo/results/MyEnv/MyEnv/mappo/check/run10/logs/summary.json'

# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)


data_record = []
# Iterate through each key-value pair in the JSON data
for key, values in data.items():
    if key == '/home/dongmingwang/project/Data_Driven_MPC/light_mappo/results/MyEnv/MyEnv/mappo/check/run10/logs/agent0/value_loss/agent0/value_loss':
        # Extract the timestamp, steps, and scalar values from the nested lists
        steps = [item[1] for item in values]
        scalar_values = [item[2] for item in values]

        # Apply Gaussian filter for smoothing
        scalar_values_smooth = gaussian_filter1d(scalar_values, sigma=2.8)
        # scalar_values_smooth = scalar_values
        
        data_record.append(scalar_values_smooth)
        # Plot the smoothed data
        plt.figure()
        plt.plot(steps, scalar_values_smooth, label='Agent 1')
        plt.xlabel('Training Steps')
        plt.ylabel('Value Loss')
        # plt.title(f'Training Process')
        plt.legend()
        plt.grid(True)

    
    if key == '/home/dongmingwang/project/Data_Driven_MPC/light_mappo/results/MyEnv/MyEnv/mappo/check/run10/logs/agent1/value_loss/agent1/value_loss':
        # Extract the timestamp, steps, and scalar values from the nested lists
        steps = [item[1] for item in values]
        scalar_values = [item[2] for item in values]

        # Apply Gaussian filter for smoothing
        scalar_values_smooth = gaussian_filter1d(scalar_values, sigma=2.8)
        # scalar_values_smooth = scalar_values
        
        data_record.append(scalar_values_smooth)
        # Plot the smoothed data

        plt.plot(steps, scalar_values_smooth, label='Agent 2')
        plt.xlabel('Training Steps')
        plt.ylabel('Value Loss')
        # plt.title(f'Training Process')
        plt.legend()
        plt.grid(True)
 
    
    if key == '/home/dongmingwang/project/Data_Driven_MPC/light_mappo/results/MyEnv/MyEnv/mappo/check/run10/logs/agent2/value_loss/agent2/value_loss':
        # Extract the timestamp, steps, and scalar values from the nested lists
        steps = [item[1] for item in values]
        scalar_values = [item[2] for item in values]

        # Apply Gaussian filter for smoothing
        scalar_values_smooth = gaussian_filter1d(scalar_values, sigma=2.8)
        # scalar_values_smooth = scalar_values
        
        data_record.append(scalar_values_smooth)
        # Plot the smoothed data

        plt.plot(steps, scalar_values_smooth, label='Agent 3')
        plt.xlabel('Training Steps')
        plt.ylabel('Value Loss')
        # plt.title(f'Training Process')
        plt.legend()
        plt.grid(True)
plt.show()

plt.savefig('new_training_process.png', format='png')

data_record = np.array(data_record)

savemat('Training_Process_gaussian_smooth_2_8.mat', {'tensor': data_record})