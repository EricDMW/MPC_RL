function bra_a1=get_A_leader(a0,t,s,v,es,ElcMap,p0,v0,bcu,peor)

%数据定义
st=0.1;
B1=-2.0221;
B2=0.83929;
B3=0;
C=0.05;%常数项
amax=1.2;%牵引力加速度最大值
% a1max=-1.2;
% PRE=a1max/(-1.38);%前车加速度配置值
K=(1+es);
T0=0.2;%牵引切断时间
T1=1.2;%紧急制动最大值完成时间
T2=0.2;
T4=0;
k1=0;%电制动比例
k2=1-k1;%空气制动比例

trainlength=94.64;

%前车初始分加速度获取
% a0=a0; %测得的加速度减去阻力加速度,80是车长

% %根据电空比信息获取初始分加速度值
% if bcu==0
%     aq=0; %牵引力为0
%     ad=0; %电制动为0
%     ak0=a0-amax;
% else
%     if a0>=0
%         aq=0;
%         ad=0;
%     else
%         aq=0;
%         ad=a0;
%     end
%     ak0=0;
% end

%所有都加上一个周期。

% T3 = SolverOfThreeOrderFunction(B3, B2, B1, C-ak0,1);%注意这里的系数发生了变化。
% 
% if T3<0.2
%     T3=0.2;
% end
% 
% %考虑周期
% T3=T3+0.2;
% %避免超过最大值
% if T3>1.2
%     T3=1.2;
% end


% if ak0<K*(-1.38)
%     ak0=-1.38*K;
% elseif ak0>-0.03
%         ak0=-(K * B1 * 0.2 + K * B2 * 0.2 * 0.2 + K * B3 * 0.2 * 0.2 * 0.2);
%     else
%         ak0=ak0;
%  end





%牵引加速度变化
if a0>0
if(t<=T0/st)
    aq=0;
else
    aq=0;
end
else
    aq=0;
end
%
% %电制动加速度
if a0<0
if(t<=T2/st)
    ad=a0*k1;
else
    ad=0;
end
else
    ad=0;
end
%空气制动加速度

if (a0 > 0)
    
    if (t < T1 / st)
        ak = K *( B1 * (t * st) +  B2 * (t * st) * (t * st) + B3 * (t * st) * (t * st) * (t * st)+C);
    elseif (t >= ((T1) / st) && v > 10/3.6)
        ak = -1.223*K;
    elseif (t >= ((T1) / st) && v > 0)
        ak = -1.223*1.3;
    else
        ak = 0;
    end
elseif(a0 == 0)
    
    
    if (t < T1 / st)
        ak = K *( B1 * (t * st) +  B2 * (t * st) * (t * st) + B3 * (t * st) * (t * st) * (t * st)+C);
    elseif (t >= ((T1) / st) && v > 10/3.6)
        ak = -1.223*K;
    elseif (t >= ((T1) / st) && v > 0)
        ak = -1.223*1.3;
    else
        ak = 0;
    end
else
% if a0>=0
%     a0=0;
% else
%     a0=a0;
% end

    T3=SolverOfThreeOrderFunction(K*B3, K*B2, K*B1, K*C-a0*k2,K);
%     if T3<0.2
%         T3=0.2;
%     else
%         T3=T3;
%     end
    
    if (t <= T4 / st)
        ak = a0*k2;
    elseif (t < (T1 - T3 + T4) / st)
        ak = (K * B1 * ((t * st) + T3 - T4) + K * B2 * ((t * st) + T3 - T4) * ((t * st) + T3 - T4) + K * B3 * ((t * st) + T3 - T4) * ((t * st) + T3 - T4) * ((t * st) + T3 - T4));
    elseif (t >= ((T1 - T3 + T4) / st) && v > 10/3.6)
        ak = -1.223*K;
    elseif (t >= ((T1 - T3 + T4) / st) && v > 0)
        ak = -1.223*1.3;
    else
        ak = 0;
    end
end


%
% ac=0;
% smaxhead=get_leaderhead(p0,v0,peor,trainlength);
% if smaxhead>4099
%     smaxhead=4099;
% end
% ac=leader_ResForce(s,2911.5,ElcMap); %前车阻力加速度值
ac=0; %前车阻力加速度值
% ac=-0.0182;%取前车最差
az=aq+ad+ak+ac;%前车总制动取值

bra_a1=az;










end
