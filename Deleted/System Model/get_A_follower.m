function bra_a2=get_A_follower(a0,t,s,v,es,ElcMap,p0,p2,bcu,peor)
%���ݶ���
st=0.1;
B1=0.075198;
B2=-2.9464;
B3=1.6319;
C=0.008881;
aqmax=1.23;%ǣ�������ٶ����ֵ
a2max=-1.533;
% FOL=a2max/(-1.38);%�󳵼��ٶ�����ֵ
K=(1-es);%���ٶ�ƫ�������ֵ
T0=0.2;
jerk=0.89;%�г����ٶȳ����
T5=0.445;%����ʱʱ�� ������420ms
T1=1.2;
T2=0.2;
T4=0.1;
k1=1;%���ƶ�����
k2=1-k1;%�����ƶ�����

trainlength=94.64;
curtime=t*st; %ʱ��
% %�󳵳�ʼ�ּ��ٶȻ�ȡ
% a0=a0; %��õļ��ٶȼ�ȥ�������ٶ�

% %���ݵ�ձ���Ϣ��ȡ��ʼ�ּ��ٶ�ֵ
% 
% if bcu==0
%     aq0=(a0-a2max)+jerk*0.2; %ʹ�õ�������ֵ�����ܴ�������
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
 
%ǣ�����ٶȱ仯
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
% %���ƶ����ٶ�
% if a0<0
%     if(t<=T2/st)
%         ad=0;
%     else
%         ad=0;
%     end
% else
%     ad=0;
% end
%�����ƶ����ٶ�

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
%                 T3 = SolverOfThreeOrderFunction(K*B3, K*B2, K*B1, a0*k2,K);%ע�������ϵ�������˱仯��
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
% ac=follower_ResForce(s,2911.5,ElcMap); %ǰ���������ٶ�ֵ
ac=0;%���������ٶ�ֵ
% ac=0.14;
az=aq+ad+ak+ac;%�����ƶ�ȡֵ

bra_a2=az;









end
