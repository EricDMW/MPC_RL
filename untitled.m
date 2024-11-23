% Load the .mat file
data = load('/home/dongmingwang/project/Data_Driven_MPC/eposodic_return.mat');

% Access the tensor directly (if data itself is the tensor)
data = data.tensor; % Load the tensor (you need to refer to the correct variable)


% Assume n x 300 data matrix
n = 3; % Example number of rows
% Calculate the mean and standard deviation
mean_values = mean(data, 1);
std_values = std(data, 0, 1);

% Define the x-axis
x = 1:100;

% Plot the mean values
figure;
plot(x, mean_values, 'b-', 'LineWidth', 1.5);
hold on;

% Add shaded area for standard deviation
fill([x fliplr(x)], [mean_values+std_values fliplr(mean_values-std_values)], 'b', ...
    'FaceAlpha', 0.2, 'EdgeColor', 'none');

% Add labels and title (optional)
xlabel('Data Index');
ylabel('Value');
title('Mean and Standard Deviation');
hold off;
