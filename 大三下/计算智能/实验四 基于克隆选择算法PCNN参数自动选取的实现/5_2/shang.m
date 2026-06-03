%计算二值图像的熵
%计算公式：H1(P)=-P1*log2(P1)-P0*Log2(P0)
%其中 p1 表示二值图像中值为 1 的概率
function HT=shang(I); 
p1=sum(sum(I));
[m,n]=size(I);

p1=p1/(m*n);
if p1==1 | p1==0
HT=0; 
else
p0= 1-p1;
HT=(-p1*log2(p1)-p0*(log2(p0)))^1.006;
end