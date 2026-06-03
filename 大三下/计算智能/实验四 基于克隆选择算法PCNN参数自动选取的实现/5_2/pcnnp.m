function [htmax,wtbest]=pcnnp(X,Beta,Decay)
%X:输入的灰度图象，Beta:突触之间的链接强度常数，Decay:阈值衰减系数 
Weight=[0.5 1 0.5;1 0 1;0.5 1 0.5];%L 的链接矩阵
Yuzhi=240;%初始阈值 
[a,b]=size(X);
Threshold=zeros(a,b); 
S=zeros(a+2,b+2);
B=zeros(a,b);%标记样板，表明该像素是否被激活过 
Y=zeros(a,b);
Edge=zeros(a,b);Numberofaera=zeros(a,b);Numberofaera_1=zeros(a,b);wt=zeros(a,b);
Num_1=0;Num=0; htmax=0;
n=1;
%初始运算时：令 Y=0；L=0；U=0；Threshold= 1;
while(sum(sum(B)))~=a*b%若采用 128*128 的图像，须注意 
    for i0=2:a+1
for i1=2:b+1
V=[S(i0-1,i1-1) S(i0-1,i1) S(i0-1,i1+1);
S(i0,i1-1) S(i0,i1) S(i0,i1+1);
S(i0+1,i1-1) S(i0+1,i1) S(i0+1,i1+1)];
L=sum(sum(V.*Weight));
F=X(i0-1,i1-1);
U=double(F)*(1+Beta*double(L));
if U>=Threshold(i0-1,i1-1)|Threshold(i0-1,i1-1)<60 
    T(i0-1,i1-1)=1;%T 等价于 Y
Threshold(i0-1,i1-1)=Yuzhi;
Y(i0-1,i1-1)=1;      %系统输出 
if n==1    % n 表示迭代次数
B(i0-1,i1-1)=0;%避免第一次全部激发造成的影响
else
B(i0-1,i1-1)=1;%已发射过的标记
Threshold(i0-1,i1-1)=1000000;%相当于不会第二次激活
end
else
T(i0-1,i1-1)=0; 
Y(i0-1,i1-1)=0;
end
end
end
Threshold(find(B~= 1))=exp(-Decay)*Threshold(find(B~= 1));%find 函数为查找 B 矩阵中值不为 1 的元素下标。
%被激活过的像素不再参与迭代过程
if n~= 1
[Numberofaera_1,Num_1]=bwlabel(Y,4);%bwlabel 二值图像联通物体的标识，4 表示4 联通区域，8 表示 8 联通区域；
%Num_ 1 为联通区个数；Numberofaera_ 1 为联通区域从 1~Num_ 1 的各个联通区域 
for i= 1:a
for j=1:b
if Numberofaera_1(i,j)~=0
Numberofaera_1(i,j)=1;%Numberofaera_ 1(i,j)+Num;
end
end
end
Numberofaera=Numberofaera+Numberofaera_1; 
Num=Num_1;
end
if n==1
S=zeros(a+2,b+2); 
else
S=Bianhuan(T);%加边 
end
wt=wt|Numberofaera_1;
ht=shang(wt);
if ht>htmax
htmax=ht; 
wtbest=wt; 
nbest=n;
end

n=n+1;
Numberofaera_1=zeros(a,b); 
end