function aF = follower_ResForce(s,smaxhead,ElcMap)
% load('Beijing_Metro_Line11_Data.mat')
% m=160*1000;
% s=200;
% % v=20;
% a=3.558;b=0.02143;c=0.00065;
% % [~,SInd]=min(ElcMap(1,:)<=s*100);
% % SInd=SInd-1;
% EssA=(a+b*v*3.6+c*(v*3.6)^2)*1000/m;
% SlpA=9.81*slope/1000;
% % CrvA=6.38/(max(ElcMap(3,SInd)*100,300)-55);
% aF=-(EssA+SlpA);
shead=smaxhead*100;
stail=s*100;
j=1;
%寻找车尾所在的区段
for i=2:length(ElcMap(1,:))
    if stail<ElcMap(1,i)
        tailbuff=i-1;
        break
    else
        continue;
    end
end

%寻找车头所在的区段
for i=2:length(ElcMap(1,:))
    if shead<ElcMap(1,i)
        headbuff=i-1;
        break
    else
        continue;
    end
end

%将剩下的区段赋值(除车头和车尾所在区段)
for i=tailbuff+1:headbuff-1
     slopebuff(j)=ElcMap(2,i);
     j=j+1;
end

%如果车尾所在的区段为首部
if  tailbuff==1
    tailleft=0;
else

%计算车尾区段的坡度
%计算车尾区段的左弧
tailleft=abs(ElcMap(2,tailbuff-1)-ElcMap(2,tailbuff))*(ElcMap(3,tailbuff)/20000);
end
% a=(ElcMap(3,tailbuff)/20000);
%计算车尾区段的右弧

if tailbuff==164
    tailright=0;
else
tailright=abs(ElcMap(2,tailbuff)-ElcMap(2,tailbuff+1))*(ElcMap(3,tailbuff)/20000);
end

%判断车尾处是否处于弧上

if stail>=ElcMap(2,tailbuff)&&stail<ElcMap(2,tailbuff)+tailleft %在左弧上
    %判断是否是从坡度高的地方到坡度低的地方
    if ElcMap(2,tailbuff-1)>ElcMap(2,tailbuff)
        tailslope=ElcMap(2,tailbuff);
    else
         tailslope=ElcMap(2,tailbuff)+((tailleft+stail-ElcMap(1,tailbuff))/(ElcMap(3,tailbuff-1)));
    end
elseif  stail>=ElcMap(2,tailbuff+1)-tailright&&stail<ElcMap(2,tailbuff+1) %在右弧上
    if ElcMap(2,tailbuff)>ElcMap(2,tailbuff+1)
         tailslope=ElcMap(2,tailbuff)+((tailright)/(ElcMap(3,tailbuff+1)));
    else
        tailslope=ElcMap(2,tailbuff)+((tailright+ElcMap(1,tailbuff+1)-stail)/(ElcMap(3,tailbuff+1)));
    end
else
    tailslope=ElcMap(2,tailbuff);
end


%计算车头区段的坡度
%计算车头区段的左弧
if headbuff==1
    headleft=0;
else
headleft=abs(ElcMap(2,headbuff-1)-ElcMap(2,headbuff))*(ElcMap(3,headbuff)/20000);
end
%计算车头区段的右弧
if headbuff==1
    headright=0;
else
headright=abs(ElcMap(2,headbuff)-ElcMap(2,headbuff+1))*(ElcMap(3,headbuff)/20000);
end

%判断车头处是否处于弧上

if shead>=ElcMap(2,headbuff)&&shead<ElcMap(2,headbuff)+headleft %在左弧上
    %判断是否是从坡度高的地方到坡度低的地方
    if ElcMap(2,headbuff-1)>ElcMap(2,headbuff)
        headslope=ElcMap(2,headbuff)+((headleft+shead-ElcMap(2,headbuff))/(ElcMap(3,headbuff-1)));
    else
         headslope=ElcMap(2,headbuff)+((headleft)/(ElcMap(3,headbuff-1)));
    end
elseif  shead>=ElcMap(2,headbuff+1)-headright&&shead<ElcMap(2,headbuff+1) %在右弧上
    if ElcMap(2,tailbuff)>ElcMap(2,tailbuff+1)
        headslope=ElcMap(2,headbuff)+((headright)/(ElcMap(3,tailbuff+1)));
    else
         headslope=ElcMap(2,headbuff)+((headright+ElcMap(2,headbuff+1)-shead)/(ElcMap(3,headbuff+1)));
    end
else
   headslope=ElcMap(2,headbuff);
end

 slopebuff(j)= tailslope;
 slopebuff(j+1)= headslope;
% for i=2:length(ElcMap(1,:))
%     if stail>ElcMap(1,i) || shead<ElcMap(1,i-1)
%     else
%         slopebuff(j)=ElcMap(2,i-1);
%         j=j+1;
%     end
% end
slope=min(slopebuff)/10;
if slope>0
    slope=0;
end
SlpA=9.81*slope/1000;
aF=-SlpA;
end