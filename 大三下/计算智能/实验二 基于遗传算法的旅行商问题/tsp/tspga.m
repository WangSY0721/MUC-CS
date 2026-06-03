function [opt, fval, MinestRoad_opt, a] = tspga(Map, MaxIter, SizeScale, pm, pc)
    n = max(size(Map));
    DistMatrix = zeros(n, n); % 初始化距离矩阵
 
    for i = 1:n
        for j = 1:n
            DistMatrix(i,j) = distance(Map(i,:), Map(j,:)); % 计算两城市之间距离
        end
    end
 
    % 生成初始种群
    Road = ones(SizeScale, n); % 初始化路径矩阵
    for i = 1:SizeScale
        Road(i,:) = randperm(n); % 随机生成初始种群（路径矩阵）
    end
 
    iter = 1;
    MinestRoad_fval = ones(MaxIter, 1); % 初始化最短里程矩阵历史记录值
    MinestRoad_opt = ones(MaxIter, n); % 初始化最短里程路径矩阵历史记录值
 
    while iter <= MaxIter
        Dist = zeros(SizeScale, 1); % 初始化里程矩阵
 
        % 计算每条路径的历程
        for i = 1:SizeScale
            for j = 1:(n-1)
                Dist(i) = Dist(i) + DistMatrix(Road(i,j), Road(i,j+1)); 
            end
            Dist(i) = Dist(i) + DistMatrix(Road(i, 1), Road(i, n)); % 计算每条路径的里程
        end
 
        % 计算每条路径的适应度值
        fitmatrix = ones(SizeScale, 1);
        [MinRoad, A] = min(Dist(:, 1)); % 计算出最小里程值
        MaxRoad = max(Dist(:, 1)); % 计算出最大里程值
        for i = 1:SizeScale
            fitmatrix(i) = fitness(MinRoad, MaxRoad, Dist(i)); % 计算每条路径的适应度值
        end
 
        % 选择操作
        [c, p] = sort(fitmatrix(:, 1)); % 对适应度值进行升序排列
        change = 20; % 选出适应度值最小路径数目
 
        for i = 1:change
            Road(p(i),:) = Road(p(SizeScale),:); % 用适应度值最大的路径替换最小的
        end
 
        Roadnew = Road;
 
        % 交叉操作
        for i = 1:SizeScale
            u = randi([1 SizeScale], 2, 1);
            s = u(1);
            t = u(2);
            if rand(1) < pc % 判断是否进行交叉操作
                oldp1 = Road(s,:); % 随机选取两个父代染色体
                oldp2 = Road(t,:);
                u = randi([1 n], 2, 1);
                crossj1 = u(1); % 随机选取两个切点
                crossj2 = u(2);
                minjcross = min(crossj1, crossj2);
                maxjcross = max(crossj1, crossj2);
                segment1 = oldp1(minjcross:maxjcross); % 选中的路径片段
                segment2 = oldp2(minjcross:maxjcross); % 选中的路径片段
                oldp12 = eliminate(oldp1, segment2); % 在oldp1中删除与segment2相同的元素
                oldp21 = eliminate(oldp2, segment1); % 在oldp2中删除与segment1相同的元素
 
                newp1 = [segment2, oldp12]; % 生成新路径
                newp2 = [segment1, oldp21]; % 生成新路径
                Roadnew(s,:) = newp1; % 更新种群
                Roadnew(t,:) = newp2;
            end
        end
 
        Road1 = Roadnew;
 
        % 计算交叉操作之后种群的最优解
        Dist = zeros(SizeScale, 1);
        for i = 1:SizeScale
            for j = 1:(n-1)
                Dist(i) = Dist(i) + DistMatrix(Road1(i,j), Road1(i,j+1)); 
            end
            Dist(i) = Dist(i) + DistMatrix(Road1(i, 1), Road1(i, n)); % 更新里程矩阵
        end
 
        [MinRoad2, B] = min(Dist);
        MaxRoad = max(Dist(:, 1)); 
        for i = 1:SizeScale
            fitmatrix(i) = fitness(MinRoad2, MaxRoad, Dist(i)); % 计算适应度函数
        end
 
        % 变异操作（单点交叉）
        k = 1;
        [dp] = sort(fitmatrix(:, 1));
 
        while k <= SizeScale
            c = randi([1 n], 2, 1);
            pos1(1,:) = c(1,:); % 随机产生交叉点
            pos2(1,:) = c(2,:); % 随机产生交叉点
            rk = rand();
            if rk <= pm && k ~= p(SizeScale) % 判断是否进行变异
                temp = Road1(p(k), pos1); % 进行变异操作，更新种群
                Road1(p(k), pos1) = Road1(p(k), pos2);
                Road1(p(k), pos2) = temp;
            end
            k = k + 1;
        end
 
        % 计算变异操作后种群的最优解
        Dist = zeros(SizeScale, 1);
        for i = 1:SizeScale
            for j = 1:(n-1)
                Dist(i) = Dist(i) + DistMatrix(Road1(i,j), Road1(i,j+1)); 
            end
            Dist(i) = Dist(i) + DistMatrix(Road1(i, 1), Road1(i, n));
        end
 
        [MinRoad3, C] = min(Dist);
 
        % 搜索每一代中的最优路径
        if (MinRoad2 > MinRoad) && (MinRoad3 > MinRoad)
            MinestRoad = MinRoad;
            D = A;
            Road(D,:) = Road(A,:);
        elseif (MinRoad > MinRoad2) && (MinRoad3 > MinRoad2)
            MinestRoad = MinRoad2;
            D = B;
            Road(D,:) = Roadnew(B,:);
        else
            MinestRoad = MinRoad3;
            D = C;
            Road(D,:) = Road1(C,:);
        end
 
        MinestRoad_fval(iter, 1) = MinestRoad; % 本代最小里程值
        MinestRoad_opt(iter,:) = Road(D,:); % 本代最优路径
        iter = iter + 1;
        Road = Road1;
    end
 
    [MinestRoad, a] = min(MinestRoad_fval); % 取路径里程最小值
    opt = MinestRoad_opt(a,:); % 输出最优路径
    fval = MinestRoad; % 输出最短里程
end
 
function d = distance(p1, p2)
    % 计算两点之间的欧几里得距离
    d = sqrt(sum((p1 - p2) .^ 2));
end
 
function fit = fitness(MinRoad, MaxRoad, Dist)
    % 计算适应度值
    fit = (MaxRoad - Dist) / (MaxRoad - MinRoad);
end
 
function result = eliminate(arr, segment)
    % 从arr中删除与segment相同的元素
    result = arr(~ismember(arr, segment));
end