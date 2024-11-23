function headway=dEBI(p1,v1,v2,a1,a2,es,peor,ElcMap,bcu)
%  load('Beijing_Metro_Line11_Data.mat')



veor=2.6;%测速误差千分比
inveor=0.26;%测速误差固定值 单位m/s
aeor=0.31;%加速度测量误差 单位m/s/s

p1=p1-peor;

v1=v1*(1-veor/1000)-inveor;
v2=v2*((1000+veor)/1000)+inveor;

%加速度测量误差
a1=a1-0.332;
a2=a2+0.240;

%前车加速度控制偏差
es_leader=0.123;
%车长
trainlength=94.64;

% %后车加速度偏差项
% if v2>75/3.6
%     es=0.04;
% elseif v2>45/3.6
%     es=0.07;
% else
%     es=0.12;
% end

    


 [P1,V1,A1]=Distance_leader(p1,v1,a1,es_leader,ElcMap,bcu,peor);
% [P2,V2,A2]=Distance_follower(p2,v2,a2,es,ElcMap,);
dis=100;f=1;dis_l=0;dis_h=100;

%停车位置分别在66359、202943、287938、356839
%因此第一站 link10 51747-67628
%因此第二站 link15 188174-204621
%因此第三站 link18 273517-290018
%因此第四站 link28 342632-359038

% first_station_start=465.42;
% first_station_end=676.28;
% 
% second_station_start=1881.74;
% second_station_end=2116.60;
% 
% third_station_start=2735.17;
% third_station_end=2969.93;
% 
% fourth_station_start=3442.70;
% fourth_station_end=3673.09;
% 
% 
% %四个前车停车点的位置  上行
% first_stop=663.29;
% second_stop=2057.74;
% third_stop=2911.64;
% fourth_stop=3640.57;
% 
% %停车点误差
% stop_error=0.5;%50cm
% 
% %前车车头起点
% s_head_start=p1+trainlength+2*peor;
% %前车车尾起点
% s_tail_start=p1;
% 
% 
% %前车车头终点
% s_head_end=P1(length(P1))+trainlength++2*peor;
% %前车车尾终点
% s_tail_end=P1(length(P1));
% 
% 
% %判断前车初始位置的车头或车尾是否在站内
% 
% if ((s_head_start>=first_station_start&&s_head_start<=first_station_end) || (s_tail_start>=first_station_start&&s_tail_start<=first_station_end))&&((s_head_start-peor<first_stop+stop_error)&&(a1<=0))
%     flag_start=1; %判断前车车头或车尾的起始位置是否在第一个车站内
% elseif ((s_head_start>=second_station_start&&s_head_start<=second_station_end) || (s_tail_start>=second_station_start&&s_tail_start<=second_station_end))&&((s_head_start-peor<second_stop+stop_error)&&(a1<=0))
%     flag_start=1; %判断前车车头或车尾的起始位置是否在第二个车站内
% elseif ((s_head_start>=third_station_start&&s_head_start<=third_station_end) || (s_tail_start>=third_station_start&&s_tail_start<=third_station_end))&&((s_head_start-peor<third_stop+stop_error)&&(a1<=0))
%     flag_start=1; %判断前车车头或车尾的起始位置是否在第三个车站内
% elseif ((s_head_start>=fourth_station_start&&s_head_start<=fourth_station_end) || (s_tail_start>=fourth_station_start&&s_tail_start<=fourth_station_end))&&((s_head_start-peor<fourth_stop+stop_error)&&(a1<=0))
%     flag_start=1; %判断前车车头或车尾的起始位置是否在第四个车站内
% else
%     flag_start=0;
% end
% 
% 
% 
% %判断前车停车位置的车头或车尾是否在站内
% 
% if (s_head_end>=first_station_start&&s_head_end<=first_station_end) || (s_tail_end>=first_station_start&&s_tail_end<=first_station_end)
%     flag_end=1; %判断前车车头或车尾的起始位置是否在第一个车站内
% elseif (s_head_end>=second_station_start&&s_head_end<=second_station_end) || (s_tail_end>=second_station_start&&s_tail_end<=second_station_end)
%     flag_end=1; %判断前车车头或车尾的起始位置是否在第二个车站内
% elseif (s_head_end>=third_station_start&&s_head_end<=third_station_end) || (s_tail_end>=third_station_start&&s_tail_end<=third_station_end)
%     flag_end=1; %判断前车车头或车尾的起始位置是否在第三个车站内
% elseif (s_head_end>=fourth_station_start&&s_head_end<=fourth_station_end) || (s_tail_end>=fourth_station_start&&s_tail_end<=fourth_station_end)
%     flag_end=1; %判断前车车头或车尾的起始位置是否在第四个车站内
% else
%     flag_end=0;
% end
% 
% 
% %如果在车站，安全保护距离为0，在区间，保护距离为5
% if  (flag_start&& flag_end)
%     Sm=0;
% else
%     Sm=5;
% end

Sm=0;
StpFlag=0;

% while f
%     [P2,V2,A2]=Distance_follower(p1-dis,v2,a2,es,ElcMap,s_tail_end,v1,bcu,peor);
      [P2,V2,A2]=Distance_follower(p1-dis,v2,a2,es,ElcMap,P1(length(P1)),v1,bcu,peor,StpFlag);
    d=P1-P2;
%     %经过判断前后车停车的阶段，进入不同的循环
%     if(V1(15)==0)
%         if(V2(15)==0)
%             min_d=min(P1-P2);
%         else
%             min_d1=min(P1-P2);
%             min_d2=P1(15)-(P2(15)-V2(15)^2/(2*A2(15)));
%              min_d=min(min_d1,min_d2);
%         end
%     else
%          if(V2(15)==0)
%             min_d=min(P1-P2);
%         else
%             min_d1=min(P1-P2);
%             min_d2=d_brakingphase(P1(15),V1(15),A1(15),P2(15),V2(15),A2(15));
%             min_d=min(min_d1,min_d2);
%         end
%     end
%**********************
   min_d=min(P1-P2);
%    min_d2=d_brakingphase(P1(15),V1(15),A1(15),P2(15),V2(15),A2(15));
%    min_d=min(min_d1,min_d2);
    if (min_d-Sm < 0.01 && min_d >= Sm) || dis_h-dis_l <= 0.01
        f=0;
    % elseif min_d <Sm
        % dis_l=dis;
        % dis=(dis_l+dis_h)/2;
    else
        dis=dis+(Sm-min_d);
        % dis_h=dis;
        % dis=(dis_h+dis_l)/2;
    end
% end
% ve(i,j)=v2;

%画出A1和A2的图像

% plot((1:length(P1))*0.1,P1)
% grid on
% hold on
% plot((1:length(P2))*0.1,P2)
headway = dis + 2*peor;

%headway=p1;

% end
% end
% end
% subplot(211)
% kk=max(length(V1),length(V2));
% plot((1:length(V1))/50,V1,'linewidth',2)
% hold on
% plot((1:length(V2))/50,V2,'linewidth',2)
%
% set(gca,'fontsize',40)
% xlabel('time (s)')
% ylabel('speed (m/s)')
% legend('1','2','EBI-1','EBI-2')
% grid on
%
% subplot(212)
% plot((1:kk)/50,P1(1:kk)-P2(1:kk)-trainlength-2,'linewidth',2)
%
% set(gca,'fontsize',40)
% xlabel('time (s)')
% ylabel('distance - s_m (m)')
% % legend('1','2','EBI-1','EBI-2')
% grid on
end

% x=1:200;y=1:13;
% [X, Y] = meshgrid(y/10,x/10);
% surf(X,Y,ve);
% load('train1.mat')
% load('train2.mat')