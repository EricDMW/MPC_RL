function [P,V,A]= Distance_follower(p,v,a,es,ElcMap,p1,v1,bcu,peor,StpFlag)

t =25;%��������ʱ�䶨Ϊ2s
st=0.05;
%�����ֵ,�����һλ��ʵ��ԭλ�ã�Ҳ����0s
V=v;
P=p;

%����ײ�������ǰ���ٶ�Ϊ0���������һ�׼������ķ�ʽ

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
% else %����ײ
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
%         if V(i-1)<= 5/3.6  %Ϊƥ����ֵ��ʱ�ȸ�Ϊ5
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

