function main()
    createRGBImage();
    ACO_ImageSegmentation();
end

function createRGBImage()
    % 设置图像的大小
    nrow = 64;
    ncol = 64;

    % 生成随机的RGB图像
    img = rand(nrow, ncol, 3);

    % 保存为tigers.bmp
    imwrite(img, 'tigers.bmp');
end

function ACO_ImageSegmentation()
    filename = 'tigers';
    img = double(imread([filename '.bmp']))./255;

    % 如果图像是RGB图像，将其转换为灰度图像
    if size(img, 3) == 3
        img = rgb2gray(img);
    end

    [nrow, ncol] = size(img);
    v = zeros(size(img));
    v_norm = 0;

    %%计算每个像素点的局部方差，作为蚁群算法的启发信息
    for rr = 1:nrow
        for cc = 1:ncol
            temp1 = [rr-2 cc-1; rr-2 cc+1; rr-1 cc-2; rr-1 cc-1; rr-1 cc; rr-1 cc+1; rr-1 cc+2; rr cc-1];
            temp2 = [rr+2 cc+1; rr+2 cc-1; rr+1 cc+2; rr+1 cc+1; rr+1 cc; rr+1 cc-1; rr+1 cc-2; rr cc+1];
            temp0 = find(temp1(:, 1) >= 1 & temp1(:, 1) <= nrow & temp1(:,2) >= 1 & temp1(:,2) <= ncol & temp2(:, 1) >= 1 & temp2(:, 1) <= nrow & temp2(:,2) >= 1 & temp2(:,2) <= ncol);
            temp11 = temp1(temp0, :);
            temp22 = temp2(temp0, :);
            temp00 = zeros(size(temp11, 1), 1);
            for kk = 1:size(temp11, 1)
                temp00(kk) = abs(img(temp11(kk, 1), temp11(kk, 2)) - img(temp22(kk, 1), temp22(kk, 2))); 
            end
            if isempty(temp11)
                v(rr, cc) = 0;
                v_norm = v_norm + v(rr, cc);
            else
                lambda = 100;
                temp00 = lambda .* temp00 .^ 4;
                v(rr, cc) = sum(temp00); 
                v_norm = v_norm + v(rr, cc);
            end
        end
    end
    v = v ./ v_norm;
    
   %% 初始化蚁群参数
p = 0.0001 .* ones(size(img)); % 初始化信息素浓度矩阵
alpha = 1; % 启发因子
beta = 0.1; % 期望因子
rho = 0.1; % 信息素挥发系数
ant_total_num = round(sqrt(nrow * ncol)); % 计算蚂蚁数量
ant_pos_idx = zeros(ant_total_num, 2); % 初始化蚂蚁位置矩阵
temp = rand(ant_total_num, 2); % 初始化蚂蚁位置
ant_pos_idx(:, 1) = round(1 + (nrow - 1) * temp(:, 1)); % 初始化蚂蚁位置的行坐标
ant_pos_idx(:, 2) = round(1 + (ncol - 1) * temp(:, 2)); % 初始化蚂蚁位置的列坐标
A = 40; % 常量，计算蚂蚁记忆长度
memory_length = round(rand(1) * (0.3 * A) + 0.85 * A); % 随机生成蚂蚁记忆长度
ant_memory = zeros(ant_total_num, memory_length); % 初始化蚂蚁记忆矩阵
total_step_num = 900; % 总迭代次数

   %% 在每次迭代中，对每只蚂蚁进行移动
for step_idx = 1:total_step_num
    delta_p_current = zeros(nrow, ncol); % 初始化当前信息素变化矩阵
    for ant_idx = 1:ant_total_num
        ant_current_row_idx = ant_pos_idx(ant_idx, 1); % 获取当前蚂蚁的行坐标
        ant_current_col_idx = ant_pos_idx(ant_idx, 2); % 获取当前蚂蚁的列坐标
        rr = ant_current_row_idx; % 临时变量，用于存储当前蚂蚁的行坐标
        cc = ant_current_col_idx; % 临时变量，用于存储当前蚂蚁的列坐标

        ant_search_range_temp = [rr-1 cc-1; rr-1 cc; rr-1 cc+1; rr cc-1; rr cc+1; rr+1 cc-1; rr+1 cc; rr+1 cc+1]; % 计算当前蚂蚁的邻居像素位置
        temp = ant_search_range_temp(:, 1) >= 1 & ant_search_range_temp(:, 1) <= nrow & ant_search_range_temp(:, 2) >= 1 & ant_search_range_temp(:, 2) <= ncol; % 过滤掉超出图像边界的像素
        ant_search_range = ant_search_range_temp(temp, :); % 获取有效的邻居像素位置
        ant_transit_prob_v = zeros(size(ant_search_range, 1), 1); % 初始化局部方差的移动概率
        ant_transit_prob_p = zeros(size(ant_search_range, 1), 1); % 初始化信息素浓度的移动概率
        for kk = 1:size(ant_search_range, 1)
            temp = (ant_search_range(kk, 1) - 1) * ncol + ant_search_range(kk, 2); % 计算当前邻居像素在记忆中的索引
            if isempty(find(ant_memory(ant_idx, :) == temp, 1))
                ant_transit_prob_v(kk) = v(ant_search_range(kk, 1), ant_search_range(kk, 2)); % 计算局部方差
                ant_transit_prob_p(kk) = p(ant_search_range(kk, 1), ant_search_range(kk, 2)); % 计算信息素浓度
            else
                ant_transit_prob_v(kk) = 0; % 如果邻居像素在蚂蚁记忆中，设置其移动概率为 0
                ant_transit_prob_p(kk) = 0;
            end
        end
        if (sum(ant_transit_prob_v) == 0) || (sum(ant_transit_prob_p) == 0)
            for kk = 1:size(ant_search_range, 1)
                ant_transit_prob_v(kk) = v(ant_search_range(kk, 1), ant_search_range(kk, 2)); % 如果所有邻居像素的移动概率都为 0，重新计算所有邻居像素的移动概率
                ant_transit_prob_p(kk) = p(ant_search_range(kk, 1), ant_search_range(kk, 2));
            end
        end
        ant_transit_prob = (ant_transit_prob_v .^ alpha) .* (ant_transit_prob_p .^ beta) ./ (sum((ant_transit_prob_v .^ alpha) .* (ant_transit_prob_p .^ beta))); % 计算最终的移动概率

        temp = find(cumsum(ant_transit_prob) >= rand(1), 1); % 根据移动概率选择下一个位置
        ant_next_row_idx = ant_search_range(temp, 1); % 获取下一个位置的行坐标
        ant_next_col_idx = ant_search_range(temp, 2); % 获取下一个位置的列坐标
        if isempty(ant_next_row_idx)
            ant_next_row_idx = ant_current_row_idx; % 如果没有选择到有效的位置，保持当前位置不变
            ant_next_col_idx = ant_current_col_idx;
        end
        ant_pos_idx(ant_idx, 1) = ant_next_row_idx; % 更新蚂蚁的位置
        ant_pos_idx(ant_idx, 2) = ant_next_col_idx;
        delta_p_current(ant_pos_idx(ant_idx, 1), ant_pos_idx(ant_idx, 2)) = 1; % 更新当前信息素变化矩阵
        if step_idx <= memory_length
            ant_memory(ant_idx, step_idx) = (ant_pos_idx(ant_idx, 1) - 1) * ncol + ant_pos_idx(ant_idx, 2); % 更新蚂蚁记忆
        elseif step_idx > memory_length
            ant_memory(ant_idx, :) = circshift(ant_memory(ant_idx, :), [0 -1]); % 移动记忆，保持记忆长度不变
            ant_memory(ant_idx, end) = (ant_pos_idx(ant_idx, 1) - 1) * ncol + ant_pos_idx(ant_idx, 2);
        end

        p = ((1 - rho) .* p + rho .* delta_p_current .* v) .* delta_p_current + p .* (abs(1 - delta_p_current)); % 更新信息素浓度矩阵
    end
end

T = judge(p); % 调用 judge 函数，计算最终的阈值 T
imwrite(uint8(abs((p >= 0.8 * T) * 255 - 255)), gray(256), [filename '_edge_aco_' '.bmp'], 'bmp'); % 根据阈值 T 生成二值化图像并保存
end

function tt = judge(I) 
    I = I(:);
    [counts, N] = hist(I, 256); 
    i = 1;
    mu = cumsum(counts);
    T(i) = (sum(N .* counts)) / mu(end);
    mu2 = cumsum(counts(N <= T(i)));
    MBT = sum(N(N <= T(i)) .* counts(N <= T(i))) / mu2(end);
    mu3 = cumsum(counts(N > T(i)));
    MAT = sum(N(N > T(i)) .* counts(N > T(i))) / mu3(end);
    i = i + 1;
    T(i) = (MAT + MBT) / 2;
    Threshold = T(i);
    while abs(T(i) - T(i-1)) >= 1
        mu2 = cumsum(counts(N <= T(i)));
        MBT = sum(N(N <= T(i)) .* counts(N <= T(i))) / mu2(end);
        mu3 = cumsum(counts(N > T(i)));
        MAT = sum(N(N > T(i)) .* counts(N > T(i))) / mu3(end); 
        i = i + 1;
        T(i) = (MAT + MBT) / 2;
        Threshold = T(i);
    end
    tt = Threshold;
end
