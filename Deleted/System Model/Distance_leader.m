function [P,V,A]= Distance_leader(p,v,a,es,ElcMap,bcu,peor) 

	 t =25;%车辆运行时间定为2s
     st=0.05;
     %赋予初值
     V=v;
     P=p;
	 A=get_A_leader(a, 1,P,V,es,ElcMap,p,v,bcu,peor);
     for i=2:(t/st)
         
         if (i > 0 && V(i-1) <= 0) %
             A(i) = 0;
         else
             A(i) = get_A_leader(a, i,P(i-1),V(i-1),es,ElcMap,p,v,bcu,peor);
         end
         
         if (V(i-1) < 0)
             V(i-1) = 0;
         end  
        
             V(i) = V(i-1) + A(i) * st;
             P(i) = P(i-1) + V(i) * st;
         
     end
%      A(i)=A(i-1);
end