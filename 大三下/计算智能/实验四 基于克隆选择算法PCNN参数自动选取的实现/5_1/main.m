clear; 
clc;
%%第一步参数初始化
gen=800;%最大迭代次数 
N=50;%初始种群个数
L=22;%编码长度
pm=0.2;%变异概率
pc=0.8;%交叉概率
p=0.5;%疫苗接种概率
Ab=round(rand(N,L));%生成二进制初始抗体种群，该步骤实质上是编码
xmin=0;xmax=1;%变量取值范围 
T0= 100;%退火选择的初始温度

f = '10+sin(1./x)./((x-0.16).^2+0.1)'; % 修正格式
%%第二步将初始种群位置标在待求函数的曲线上
x=decode(Ab,xmin,xmax,L); %对初始抗体群进行由二进制到十进制的转化，该步骤实质上是解码，用以计算亲和度值
fit=eval(f); % eval 函数就是将字符串中的表达式放到命令行中执行 
figure(1);
fplot(f,[xmin, xmax]);grid on; hold on;
plot(x, fit, 'k*');title('(a)抗体的初始位置分布图 '); xlabel('x'); ylabel('y');
%%第三步通过迭代实现种群的进化 
it=0;
while it<gen

it=it+1;
[mbest(it),pos]=max(fit);
bestp(it,:)=Ab(pos,:);%找到目前最优解 
T1=Ab;
T2=crossover(T1,pc);%交叉 
T3=mutation(T2,pm);%变异
T4=yimiao(T3,bestp(it,:),p,5);%接种疫苗 
%%退火选择
x=decode(T1,xmin,xmax,L); fit1=eval(f);
x=decode(T4,xmin,xmax,L); fit2=eval(f);
T=log(T0/it+1);%参数调整 
for i= 1:N
if ((fit1(i)<fit2(i))||(fit1(i)==fit2(i))) %若经过交叉、变异、接种疫苗后种群中的第 i 个个体亲和度值大于或等于初始亲和度值，则保留子代个体
    Ab(i,:)=T4(i,:);
elseif (fit2(i)*exp(fit2(i)/T)/sum(fit2.*exp(fit2./T))>rand) Ab(i,:)=T4(i,:);
else
Ab(i,:)=T1(i,:);
end
end
x=decode(Ab,xmin,xmax,L);
fit=eval(f);% eval 函数就是将字符串中的表达式放到命令行中执行 
end
%%第四步输出最后的结果

figure(2);fplot(f,[xmin,xmax]);grid on;hold on;

plot(x,fit,'k*');title('(b)抗体的最终位置分布图 ');xlabel('x');ylabel('y'); figure(3)
plot(1:gen,mbest); title('(c)亲和度函数变化曲线');%亲和度函数曲线 
[gb,opt]=max(fit);
disp (sprintf('全局最优值为:'))
disp (sprintf('y=%f ', gb));
disp (sprintf('其中:'));
disp (sprintf('x=%f ', x(opt)));