%%%%%%%%%%%%%%%%%初始化%%%%%%%%%%%%%%%%%%% 
clear all; %清除所有变量
close all; %清图
clc; %清屏

% 参数设置
N = 100; % 群体粒子个数
D = 10; % 粒子维数
T = 200; % 最大迭代次数
c1 = 1.5; % 学习因子 1
c2 = 1.5; % 学习因子 2
Wmax = 0.8; % 惯性权重最大值
Wmin = 0.4; % 惯性权重最小值
Vmax = 1; % 速度最大值
Vmin = -20; % 速度最小值
V = 300; % 背包容量
C = [95, 75, 23, 73, 50, 22, 6, 57, 89, 98]; % 物品体积
W = [89, 59, 19, 43, 100, 72, 44, 16, 7, 64]; % 物品价值
afa = 2; % 惩罚函数系数

%%%%%%%%% 初始化种群个体（限定位置和速度） %%%%%%%%%%
x = rand(N, D); % 随机获得二进制编码的初始种群
v = rand(N, D) * (Vmax - Vmin) + Vmin;

%%%%%%%%%%% 初始化个体最优位置和最优值 %%%%%%%%%%%% 
p = x;
pbest = ones(N, 1);

for i = 1:N
    pbest(i) = func4(x(i,:), C, W, V, afa); 
end

%%%%%%%%%%%% 初始化全局最优位置和最优值 %%%%%%%%%%% 
g = ones(1, D);
gbest = -inf; % 修改初始值为负无穷，确保能够正确更新
for i = 1:N
    if pbest(i) > gbest
        g = p(i,:);
        gbest = pbest(i);
    end
end

gb = ones(1, T);

%%%%%%% 按照公式依次迭代直到满足精度或者迭代次数 %%%%%%%
for i = 1:T
    for j = 1:N
        %%%%%% 更新个体最优位置和最优值 %%%%%%%%%%%%%
        currentFitness = func4(x(j,:), C, W, V, afa);
        if currentFitness > pbest(j)
            p(j,:) = x(j,:);
            pbest(j) = currentFitness;
        end

        %%%%%%%%% 更新全局最优位置和最优值 %%%%%%%%%
        if pbest(j) > gbest
            g = p(j,:);
            gbest = pbest(j); 
        end

        %%%%%%%%% 计算动态惯性权重值 %%%%%%%%%%%%% 
        w = Wmax - (Wmax - Wmin) * i / T;

        %%%%%%%%% 更新位置和速度值 %%%%%%%%%%%%%%
        v(j,:) = w * v(j,:) + c1 * rand * (p(j,:) - x(j,:)) + c2 * rand * (g - x(j,:));

        %%%%%%%%%%%% 边界条件处理 %%%%%%%%%%%%%%
        for ii = 1:D
            if v(j,ii) > Vmax || v(j,ii) < Vmin
                v(j,ii) = rand * (Vmax - Vmin) + Vmin;
            end
        end

        vx(j,:) = 1 ./ (1 + exp(-v(j,:))); 
        for jj = 1:D
            if vx(j,jj) > rand
                x(j,jj) = 1;
            else
                x(j,jj) = 0;
            end
        end
    end
    %%%%%%%%%%%%% 记录历代全局最优值 %%%%%%%%%%%%
    gb(i) = gbest;
end

g % 输出最优个体
figure
plot(gb)
xlabel('迭代次数');
ylabel('适应度值');
title('适应度进化曲线')

%%%%%%%%%%%%%%% 适应度函数 %%%%%%%%%%%%%%%%%
function result = func4(f, C, W, V, afa)
    fit = sum(f .* W);
    TotalSize = sum(f .* C); 
    if TotalSize <= V
        fit = fit;
    else
        fit = fit - afa * (TotalSize - V);
    end
    result = fit;
end
