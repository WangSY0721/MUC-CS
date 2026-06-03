% 参数敏感性分析脚本（不修改原有代码）
clear all; close all; clc;

% 原始地图数据（20城市）
Map1 = [82,7;91,38;83,46;71,44;64,60;68,58;83,69;87,76;74,78;71,71;
        53,50;52,21;60,39;37,84;22,91;25,75;38,52;58,11;69,33;90,23];
MaxIter = 500; % 最大迭代次数
runs = 10;     % 每个参数组合运行次数

% 定义参数范围（与你之前需求一致）
pop_sizes = [150, 500];       % 种群规模
cross_rates = [0.2, 0.8];     % 交叉概率
mutate_rates = [0.01, 0.1];   % 变异概率

% 初始化结果存储矩阵
results = zeros(length(pop_sizes), length(cross_rates), length(mutate_rates), 4);

% 遍历所有参数组合
for i = 1:length(pop_sizes)
    Pop_Size = pop_sizes(i);
    for j = 1:length(cross_rates)
        pc = cross_rates(j);
        for k = 1:length(mutate_rates)
            pm = mutate_rates(k);
            fval_list = zeros(runs, 1); % 存储每次运行的最短里程
            
            % 重复运行多次，利用MATLAB默认随机种子（每次启动后自动变化）
            for run = 1:runs
                [~, fval, ~, ~] = tspga(Map1, MaxIter, Pop_Size, pm, pc);
                fval_list(run) = fval;
            end
            
            % 计算统计量
            results(i,j,k,1) = mean(fval_list); % 平均里程
            results(i,j,k,2) = std(fval_list);  % 标准差（反映稳定性）
            results(i,j,k,3) = min(fval_list);  % 最优里程
            results(i,j,k,4) = max(fval_list);  % 最差里程
            
            % 输出结果
            fprintf('参数组合：Pop=%d, pc=%.1f, pm=%.2f\n', Pop_Size, pc, pm);
            fprintf('  运行%d次 | 最优: %.2f | 平均: %.2f | 标准差: %.2f\n', ...
                runs, results(i,j,k,3), results(i,j,k,1), results(i,j,k,2));
        end
    end
end

% 可视化参数影响（以种群大小为例）
figure;
subplot(1,3,1);
bar([pop_sizes(1), pop_sizes(2)], [results(1,1,1,3), results(2,1,1,3)]);
title('种群大小对最优里程的影响');
xlabel('种群规模'); ylabel('最短里程');
set(gca, 'XTickLabel', {'150', '500'});

% 交叉概率影响（固定种群=150，变异率=0.01）
subplot(1,3,2);
bar([cross_rates(1), cross_rates(2)], [results(1,1,1,3), results(1,2,1,3)]);
title('交叉概率对最优里程的影响');
xlabel('交叉概率'); ylabel('最短里程');
set(gca, 'XTickLabel', {'0.2', '0.8'});

% 变异概率影响（固定种群=150，交叉率=0.2）
subplot(1,3,3);
bar([mutate_rates(1), mutate_rates(2)], [results(1,1,1,3), results(1,1,2,3)]);
title('变异概率对最优里程的影响');
xlabel('变异概率'); ylabel('最短里程');
set(gca, 'XTickLabel', {'0.01', '0.1'});