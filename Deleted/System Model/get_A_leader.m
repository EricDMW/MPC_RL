function bra_a1=get_A_leader(a0,t,s,v,es,ElcMap,p0,v0,bcu,peor)

%���ݶ���
st=0.1;
B1=-2.0221;
B2=0.83929;
B3=0;
C=0.05;%������
amax=1.2;%ǣ�������ٶ����ֵ
% a1max=-1.2;
% PRE=a1max/(-1.38);%ǰ�����ٶ�����ֵ
K=(1+es);
T0=0.2;%ǣ���ж�ʱ��
T1=1.2;%�����ƶ����ֵ���ʱ��
T2=0.2;
T4=0;
k1=0;%���ƶ�����
k2=1-k1;%�����ƶ�����

trainlength=94.64;

%ǰ����ʼ�ּ��ٶȻ�ȡ
% a0=a0; %��õļ��ٶȼ�ȥ�������ٶ�,80�ǳ���

% %���ݵ�ձ���Ϣ��ȡ��ʼ�ּ��ٶ�ֵ
% if bcu==0
%     aq=0; %ǣ����Ϊ0
%     ad=0; %���ƶ�Ϊ0
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

%���ж�����һ�����ڡ�

% T3 = SolverOfThreeOrderFunction(B3, B2, B1, C-ak0,1);%ע�������ϵ�������˱仯��
% 
% if T3<0.2
%     T3=0.2;
% end
% 
% %��������
% T3=T3+0.2;
% %���ⳬ�����ֵ
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





%ǣ�����ٶȱ仯
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
% %���ƶ����ٶ�
if a0<0
if(t<=T2/st)
    ad=a0*k1;
else
    ad=0;
end
else
    ad=0;
end
%�����ƶ����ٶ�

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
% ac=leader_ResForce(s,2911.5,ElcMap); %ǰ���������ٶ�ֵ
ac=0; %ǰ���������ٶ�ֵ
% ac=-0.0182;%ȡǰ�����
az=aq+ad+ak+ac;%ǰ�����ƶ�ȡֵ

bra_a1=az;










end
