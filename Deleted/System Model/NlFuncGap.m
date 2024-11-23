function dx = NlFuncGap(dt, x, w, u)
%%[ds,dv,da,df,v,a,f]

% input: dt=.2 time step, x: state 7-dimension, w: former control input, u:
% control input

% x[7] = randselect{10,...,20} random seed

% target: x[:4] = 0, x[4] = 15, x[5:] = 0 x[7] = target_speed

% centralized: agents num 3: clip 3 states = 21-dimension state former ontrol input,

% action: u, input: global state, output: control signal u.

% reward: #1-epsicon_1*norm(sum x_i[:4]) #2-epsilon_2*norm(x[4]-x[7]) #3-epsilon_3*norm(x[5:])
% gemeralization 

% initialization: x, w, u: x_1[], x_2[], x_3[]

% u = - (x_i - x_target)

ElcMap=[[0;0;0;2222],[298303;0;0;2222]];

xl=x;ul=[w;u];
for k=1:dt/0.05
    xp=NlFunc(0.05, xl, ul, ElcMap);
    xl=xp;
end

dx=xl;
end