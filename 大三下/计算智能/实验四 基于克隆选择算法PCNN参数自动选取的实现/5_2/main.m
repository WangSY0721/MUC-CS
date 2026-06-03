clear;
clc;
close all;
X =double(imread('cameraman.tif')); %  人工免疫算法
popsize=10;      %种群数
m=popsize/5;      %记忆库-亲和度较高；
%初始化编码
a=16; %%编码位数
Population=initialization(popsize,a);    %初始化种群，其中 popsize 为每代群体数量
v=256;
[ax,bx]=codep(Population);                          %编码

tic
%初始化归一化互信息
for i= 1:popsize
htp=pcnnp(X,ax(i),bx(i));%计算每一个 ax,bx 下的 pcnn 分割后的最大熵 
%  计算归一化互信息
    objection(i)=htp;
end;
%%%%%%%%免疫算子 
k= 1; %叠代次数
obj_max=max(objection); 
pc=0.7;    %交叉概率
pm=0.05; %变异概率
for k=2:50; %叠代
[L,h]=size(Population);%L 初始种群，h 编码位数
[offspring,t,MM1,memory,location]=clonep(Population,objection,m,h);      %克隆 M 的种群
Coffspring=twopointcross(offspring,pc);                              %交叉
Moffspring=mutation(Coffspring,pm);%变异
%%%%%增加新染色体,使种群数保持在 100 个 
[Cr,Cc]=size(Moffspring);
if Cr>=popsize
Population=Moffspring; 
elseif Cr<popsize
Cr1=popsize-Cr;
Population1=initialization(Cr1,a);
Population=[Moffspring;Population1];
end
k=k+1;
Population

%对新的种群 Moffspring 计算亲和度
[ax1,bx1]=codep(Population);
[r,c]=size(Population); 
for i= 1:r
htp=pcnnp(X,ax1(i),bx1(i)); 
objection(i)=htp;
end
end
%显示计算结果

objection 
toc

%选择最大值,找到对应的参数进行配准 
[obj_end,pst]=max(objection) ;
best=Population(pst,:);
[axde,bxde]=codep(best);
[htp,wtbest]=pcnnp(X,axde,bxde); 
htp %最大熵
axde
bxde
figure;imshow(wtbest);title('最佳分割图像')