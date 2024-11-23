function bra_a2=get_A_follower(a0,t,s,v,es,ElcMap,p0,p2,bcu,peor)
%数据定义
st=0.1;
B1=0.075198;
B2=-2.9464;
B3=1.6319;
C=0.008881;
aqmax=1.23;%牵引力加速度最大值
a2max=-1.533;
% FOL=a2max/(-1.38);%后车加速度配置值
K=(1-es);%加速度偏差乘配置值
T0=0.2;
jerk=0.89;%列车加速度冲击率
T5=0.445;%后车延时时间 现在是420ms
T1=1.2;
T2=0.2;
T4=0.1;
k1=1;%电制动比例
k2=1-k1;%空气制动比例

trainlength=94.64;
curtime=t*st; %时间
% %后车初始分加速度获取
% a0=a0; %测得的加速度减去阻力加速度

% %根据电空比信息获取初始分加速度值
% 
% if bcu==0
%     aq0=(a0-a2max)+jerk*0.2; %使用的是名义值，可能存在问题
% else
%     aq0=a0+jerk*0.2;
% end

%  aq0=a0;
 if a0>=0
     aq0=a0;
     ad0=0;
 else
     aq0=0;
     ad0=a0*k1;
 end
 
%牵引加速度变化
if bcu==0
    aqmax=aqmax;
else
    aqmax=0;
end

if curtime<T5
    aqANDad=aq0+ad0+jerk*t*st;
    
    if aqANDad<aqmax
        aq= aqANDad;
        ad = 0;
        
    else 
        aq = aqmax;
        ad = 0;
    end
elseif curtime <= T5+T2
    
    if aq0+ad0+jerk*T5 < 0
        aq = 0;
        ad = 0;
        
    else
        aq = aq0+ad0+jerk*T5;
        
        if aq > aqmax
            aq = aqmax;
        end
        ad = 0;
    end
    
    
else
    aq = 0;
    ad = 0;
end
% else
%     if curtime<T5
%         aq=0;
%         ad=0;
%     elseif curtime<T5+T2
%         aq=0;
%         ad=0;
%     else
%         aq = 0;
%         ad = 0;
%     end
% end










% if a0>=0
%     if(t<=T5/st)
%         aq1=a0+jerk*t*st;
%         if(aq1<aqmax)
%             aq=aq1;
%         else
%             aq=aqmax;
%         end
%         elseif(t<=(T5+T0)/st)
%             aq1=a0+jerk*T5;
%         if(aq1<aqmax)
%             aq=aq1;
%         else
%             aq=aqmax;
%         end
%     else
%         aq=0;
%     end
% else
%     aq=0;
% end
% 
% %电制动加速度
% if a0<0
%     if(t<=T2/st)
%         ad=0;
%     else
%         ad=0;
%     end
% else
%     ad=0;
% end
%空气制动加速度

% if (a0 > 0)
    if (t<=T5/st)
        ak=0;
    elseif (t <(T1+T5) / st)
        ak = (K * B1 * ((t * st)-T5) + K * B2 * ((t * st)-T5) * ((t * st)-T5) + K * B3 * ((t * st)-T5) * ((t * st)-T5) * ((t * st)-T5)+C);
    elseif (t >= (T1+T5) / st && v > 0)
            ak = -1.533*K;
        else
            ak = 0;
     end
% elseif(a0 == 0)
%                 
%      if (t<=T5/st)
%         ak=0;
%     elseif (t < (T1+T5) / st)
%         ak = -(K * B1 * ((t * st)-T5) + K * B2 * ((t * st)-T5) * ((t * st)-T5) + K * B3 * ((t * st)-T5) * ((t * st)-T5) * ((t * st)-T5));
%     elseif (t >= (T1+T5) / st && v > 0)
%             ak = -1.38*K;
%         else
%             ak = 0;
%      end
% else
%                 
%                 T3 = SolverOfThreeOrderFunction(K*B3, K*B2, K*B1, a0*k2,K);%注意这里的系数发生了变化。
%                 if (t <= (T4+T5) / st)
%                     ak = a0*k2;
%                 elseif (t < (T1 - T3 + T4+T5) / st)
%                         ak = -(K * B1 * ((t * st) + T3 - T4-T5) + K * B2 * ((t * st) + T3 - T4-T5) * ((t * st) + T3 - T4-T5) + K * B3 * ((t * st) + T3 - T4-T5) * ((t * st) + T3 - T4-T5) * ((t * st) + T3 - T4-T5));
%                 elseif (t >= ((T1 - T3 + T4+T5) / st) && v > 0)
%                             ak = -1.38*K;
%                 else
%                             ak = 0;
%                 end
% end



% ac=0;
% smaxhead=p0;
% if smaxhead>4099
%     smaxhead=4099;
% end
% ac=follower_ResForce(s,2911.5,ElcMap); %前车阻力加速度值
ac=0;%后车阻力加速度值
% ac=0.14;
az=aq+ad+ak+ac;%后车总制动取值

bra_a2=az;









end
