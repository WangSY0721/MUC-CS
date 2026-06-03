clear all;
clc;
II=imread('tank.tiff');
figure; imshow(II(:,:,1)); title('原始图像');
I=im2double(II(:,:,1));
%求解原始图像全局均值 D
D=mean(mean(I));
disp(D);
scah=size(I,1);scac=size(I,2);M=[];
%求原始图像局部均值
for i=1:scah
for j=1:scac
if i==1||i==scah||j==1||j==scac
if i==1&&j==1
M(i,j)=mean(mean(I(i:i+2,j:j+2)));
elseif i==1&&j==scac
M(i,j)=mean(mean(I(i:i+2,j-2:j)));
elseif i==scah&&j==1
M(i,j)=mean(mean(I(i-2:i,j:j+2)));
elseif i==scah&&j==scac
M(i,j)=mean(mean(I(i-2:i,j-2:j)));
elseif i==1&&j>=2&&j<=scac
M(i,j)=mean(mean(I(i:i+2,j-1:j+1)));
elseif i==scah&&j>=2&&j<=scac
M(i,j)=mean(mean(I(i-2:i,j-1:j+1)));
elseif j==1&&i>=2&&i<=scah
M(i,j)=mean(mean(I(i-1:i+1,j:j+2)));
elseif j==scac&&i>=2&&i<=scah
M(i,j)=mean(mean(I(i-1:i+1,j-2:j)));
end
else
M(i,j)=mean(mean(I(i-1:i+1,j-1:j+1)));
end
end
end
%求解原始图像局部标准差
Lumda=[];
Lumda=stdfilt(I);
FG=zeros(1,10);
SN=30;
YL=15;
GS=15;
LB=[0,0,0,0];
HB=[1.5,0.5,1,0.5];
DWEI=4;
ZQ.f=[];
Fa=[];
xmin=[0,0,0,0];xmax=[1.5,0.5,1,0.5];
%产生初始种群
for i=1:SN
P(i,:)=unifrnd(xmin,xmax,1,4);
ZQ(i).f=zqtu(I,P(i,:),D,M,Lumda); %计算适应度值
Fa(i)=fit301(ZQ(i).f);
end
zqiamge.f=[];
gs_zqiamge.f=[];
g=1;
G=100;
FB=zeros(G,DWEI+1);
t1=clock;
FC=zeros(G,YL);
limit=30;
allbee.f=[];
while g<=G
disp(g);
[shu,xuhao]=max(Fa);Xbest=P(xuhao,:);Xme=mean(P);
[F1,pos]=sort(Fa);
F1=fliplr(F1);
pos=fliplr(pos);
FB(g,1)=F1(1); % 存放每次迭代的 F1 最大的结果
FB(g,2:DWEI+1)=P(pos(1),:);
for i=1:YL
my(i,1:DWEI)=P(pos(i),:); %蜜源前 D 位为解，后一位为适应度值,引领蜂
my(i,DWEI+1)=F1(i);
gs(i,1:DWEI)=P(pos(YL+i),:); %跟随蜂群前 D 位为解，后一位为适应度值
gs(i,DWEI+1)=F1(YL+i);
end
% 引领蜂搜索
for i=1:YL
while 2>1
k=ceil(YL*rand());
if (k~=i)
break;
end
end
for j=1:DWEI
yl(i,j)=my(i,j)+(-1+2*rand)*(my(i,j)-my(k,j)); %引领蜂随机搜索位置，取代蜜源
if yl(i,j)>HB(j)
yl(i,j)=HB(j);
end
if yl(i,j)<LB(j)
yl(i,j)=LB(j);
end
end
% 计算新个体的适应度值
zqiamge(i).f=zqtu(I,yl(i,:),D,M,Lumda);
f=fit301(zqiamge(i).f);
if f>my(i,DWEI+1)
my(i,1:DWEI)=yl(i,:);
my(i,DWEI+1)=f;
end
end
% 跟随蜂搜索
ff=sum(my(:,DWEI+1));
ff1=my(:,DWEI+1)/ff;
ff2(1)=ff1(1);
for m=2:YL
ff2(m)=ff2(m-1)+ff1(m); %轮盘赌找出跟随蜂的蜜源,ff2 累计求和
end
for i=1:YL
a=rand;
pos1=find(ff2>=a);
k=pos1(1);
while 2>1
k1=ceil(YL*rand());
if (k1~=k)
break;
end
end
for j=1:DWEI
gs(i,j)=my(k,j)+(-1+2*rand)*(my(k,j)-my(k1,j));
if gs(i,j)>HB(j)
gs(i,j)=HB(j);
end
if gs(i,j)<LB(j)
gs(i,j)=LB(j);
end
end
pos1=[];
end
% 判断是否出现侦查蜂
FC(g,:)=my(:,1+DWEI)';
zck=ones(1,YL);
if g>=2
for j=1:YL
for i=1:g-1
pos2=find(FC(g,j)==FC(i,:), 1);
if isempty(pos2)~=1
zck(j)=1+zck(j);
end
pos2=[];
end
end
pos2=find(zck==limit);
if isempty(pos2)~=1
for i=1:length(pos2)
my(pos2(i),1:4)=unifrnd(xmin,xmax,1,4);
ZQ(pos2(i)).f=zqtu(I,my(pos2(i),1:4),D,M,Lumda); %增强图像
Fa(pos2(i))=fit301(ZQ(pos2(i)).f);
my(pos2(i),5)=Fa(pos2(i));
end
end
end
P(1:YL,:)=my(:,1:DWEI);
P(YL+1:SN, :) = gs(:, 1:DWEI);

for i=1:SN
ZQ(i).f=zqtu(I,P(i,:),D,M,Lumda);
Fa(i)=fit301(ZQ(i).f);
end
fitnum(g)=max(Fa);
g=g+1;
end
[ZYshu,xu]=max(Fa);
ZZYY=ZQ(xu).f;
ZYshu
P(xu)
figure;imshow(ZZYY);title('增强图像')
figure;plot(fitnum);