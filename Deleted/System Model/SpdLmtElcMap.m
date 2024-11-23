function SpdLmt=SpdLmtElcMap(s1,v1,a1,s2,ElcMap)
SpdMarg=3;

umin=-0.8;
L=94.64;
EndPos=s1+v1^2/2/1;
StartPos=s2-L;
HeadPos=s1;
StartFlag=1;EndFlag=1;HeadFlag=1;
i=2;

while StartFlag || EndFlag
    if StartFlag && StartPos <= ElcMap(1,i)/100
        StartFlag=0;
        StartInd=i-1;
    end
    if HeadFlag && HeadPos <= ElcMap(1,i)/100
        HeadFlag=0;
        HeadInd=i-1;
    end
    if EndFlag && EndPos <= ElcMap(1,i)/100
        EndFlag=0;
        EndInd=i-1;
    end
    i=i+1;
end

IniSpdLmt=min(ElcMap(4,StartInd:HeadInd))/100-SpdMarg;
SpdLmt=IniSpdLmt;

for i = (HeadInd + 1) : EndInd
    if ElcMap(4,i)/100-SpdMarg < IniSpdLmt
        SpdLmtAux=sqrt((ElcMap(4,i)/100-SpdMarg)^2+((ElcMap(1,i)/100-s1)*2*-umin));
        SpdLmt=min(SpdLmtAux,SpdLmt);
    end
end

end