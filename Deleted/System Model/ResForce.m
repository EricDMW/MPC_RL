function aF = ResForce(s,v,ElcMap)
% load('Beijing_Metro_Line11_Data.mat')

m=160*1000;

% s=200;
% v=20;

a=3.558;b=0.02143;c=0.00065;

[~,SInd]=min(ElcMap(1,:)<=s*100);
SInd=SInd-1;
EssA=(a+b*v*3.6+c*(v*3.6)^2)*1000/m;

SlpA=9.81*ElcMap(2,SInd)/1000;

CrvA=6.38/(max(ElcMap(3,SInd)*100,300)-55);

aF=-(EssA+SlpA+CrvA);

end