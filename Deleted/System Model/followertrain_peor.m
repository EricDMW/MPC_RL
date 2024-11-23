function aF = followertrain_peor(shead,ydq)
minpeor=1.17;%×îÐ¡²â¾àÎó²î
for i=2:length(ydq(1,:))
    if shead<=ydq(1,i)
        peor=minpeor+(shead-ydq(1,i-1))*0.02;
        break
    end
    if shead>=ydq(1,length(ydq(1,:)))
        peor=minpeor+(shead-ydq(1,length(ydq(1,:))-1))*0.02;
        break
    end
end
aF=peor;
end
    