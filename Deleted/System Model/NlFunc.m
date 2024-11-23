function dx = NlFunc(dt, x, u, ElcMap)
%%[ds,dv,da,df,v,a,f]

v1=x(2)+x(5);
v2=x(5);
f1=x(4)+x(7);
f2=x(7);
a1=x(3)+x(6);
a2=x(6);

dx(7)=x(7)+dt*u(2);
dx(6)=x(6)+dt*(x(7)-x(6))/0.7;
dx(5)=x(5)+dt*(x(6));
dx(4)=x(4)+dt*(u(1)-u(2));

dx(3)=x(3)+dt*(x(4)-x(3))/0.7;

dx(2)=x(2)+dt*(x(3));

dv1=dx(2)+dx(5);
dv2=dx(5);
df1=dx(4)+dx(7);
df2=dx(7);
da1=dx(3)+dx(6);
da2=dx(6);

d=dEBI(1000,v1,v2+5/3.6,a1,a2,0.23,0,ElcMap,0);
dd=dEBI(1000,dv1,dv2+5/3.6,da1,da2,0.23,0,ElcMap,0);
% d=dEBI(1000,v1,v2,0,0,0,0.12,ElcMap,0);
% dd=dEBI(1000,dv1,dv2,0,0,0,0.12,ElcMap,0);
dx(1)=x(1)+d-dd+dt*x(2);

% dx(1)=x(1)+dt*(x(2))+0.01*(-v1^2+v2^2)-0.01*(-dv1^2+dv2^2);

% dx(1)=x(1)+dt*x(2);

dx=dx';


% % T=0.7;
% % spt=dt;
% % 
% % A=[1,spt,0,0,0;
% %     0,1,spt,0,0;
% %     0,0,1-spt/T,0,0;
% %     0,0,0,1,spt;
% %     0,0,0,0,1-spt/T];
% % B=[0,0;
% %     0,0;
% %     spt/T,-spt/T;
% %     0,0;
% %     0,spt/T];
% % 
% % dx=A*x+B*u;

end