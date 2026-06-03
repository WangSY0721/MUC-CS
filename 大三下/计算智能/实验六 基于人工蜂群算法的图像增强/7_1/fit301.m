% ÊÊÓ¦¶Èº¯Êý
function FFT=fit301(GG)
scahh=size(GG,1);scacc=size(GG,2);
TTao=[];TTao=GG;
BBian=edge(GG,'sobel');
for i=2:scahh-1
for j=2:scacc-1
Taox=GG(i+1,j-1)+2*GG(i+1,j)+GG(i+1,j+1)-GG(i-1,j-1)-2*GG(i-1,j)-GG(i-1,j+1);
Taoy=GG(i-1,j+1)+2*GG(i,j+1)+GG(i+1,j+1)-GG(i-1,j-1)-2*GG(i,j-1)-GG(i+1,j-1);
TTao(i,j)=sqrt(Taox^2+Taoy^2);
end
end
Ednu=sum(sum(BBian));
if Ednu ~= 0
EI=sum(sum(TTao.*BBian));
temp=imhist(GG);
xu=find(temp~=0);
zuihou=temp(xu);
HI=-sum(log(zuihou/(scahh*scacc)).*(zuihou/(scahh*scacc)));
FI=log(log(EI))*Ednu*HI/(scahh*scacc);
else
FI=0;
end
FFT=FI;