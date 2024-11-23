%%system state: x=[ds,dv,da,df,v,a,f]^T
%%original system input: u=[psi_{i-1},psi_i]^T
%%divided into two inputs: 
%%(1) w=[psi_{i-1}]-control input of the preceding unit;
%%(2) u=[psi_i]-control input of the preceding unit;


%%example
x=[1000;0;0;0;15;0;0.5];
%x = ones(7,1);
w=-1;
u=1;
dt=0.2;
x_next=NlFuncGap(dt, x, w, u);%%'NlFuncGap' is the system dynamics function
disp(x_next)





