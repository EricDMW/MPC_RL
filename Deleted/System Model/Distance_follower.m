function [P,V,A]= Distance_follower(p,v,a,es,ElcMap,p1,v1,bcu,peor,StpFlag)

t =25;%车辆运行时间定为2s
st=0.05;
%赋予初值,数组第一位其实是原位置，也就是0s
V=v;
P=p;

%可碰撞处理，如果前车速度为0，则采用另一套计算距离的方式

    for i=2:(t/st)

        if (i > 0 && V(i-1) <= 0)
            A(i-1) = 0;
        else
            A(i-1) = get_A_follower(a, i-1,P(i-1),V(i-1),es,ElcMap,p1,p,bcu,peor);
        end

        if (V(i-1) < 0)
            V(i-1) = 0;
        end

        V(i) = V(i-1) + A(i-1) * st;
        P(i) = P(i-1) + V(i-1) * st;

    end
    A(i)=A(i-1);
% else %可碰撞
%     for i=2:(t/st)
% 
%         if (i > 0 && V(i-1) <= 0)
%             A(i-1) = 0;
%         else
%             A(i-1) = get_A_follower(a, i-1,P(i-1),V(i-1),es,ElcMap,p1,p,bcu,peor);
%         end
% 
%         if (V(i-1) < 0)
%             V(i-1) = 0;
%         end
% 
%         if V(i-1)<= 5/3.6  %为匹配数值暂时先改为5
%             V(i)=V(i-1);
%             P(i) = P(i-1);
%         else
%             V(i) = V(i-1) + A(i-1) * st;
%             P(i) = P(i-1) + V(i-1) * st;
%         end
% 
%     end
%     A(i)=A(i-1);
% end
end

