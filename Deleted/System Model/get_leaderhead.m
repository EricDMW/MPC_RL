function leaderhead=get_leaderhead(s,v,peor,trainlength)

slope=-28.5;%ȫ�ζ���ǰ����˵����¶�
a=0.8-9.81*slope/1000;
head=s+trainlength+v*v/(2*a)+2*peor;
leaderhead=head;
end