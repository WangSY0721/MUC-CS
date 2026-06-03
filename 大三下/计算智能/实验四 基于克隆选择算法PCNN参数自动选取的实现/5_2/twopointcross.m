% 双点交叉函数， pc 为交叉概率
function Coffspring = twopointcross(offspring, pc)
    Coffspring = offspring; 
    [r, c] = size(offspring); 
    m = 1;
    Position = [];  % 初始化 Position

    for n = 1:r
        rc = rand(1); 
        if rc < pc
            Position(1, m) = n; 
            m = m + 1;
        end
    end

    [r1, c1] = size(Position);
    l = floor(c1 / 2);
    
    for t = 1:l
        Point = randi([1, c-1], 1, 2);  % 使用 randi 替换 randint
        minPoint = min(Point);
        maxPoint = max(Point);

        % 交换两个个体在交叉点之间的基因片段
        Coffspring(Position(1, 2*t-1), minPoint:maxPoint) = offspring(Position(1, 2*t), minPoint:maxPoint);
        Coffspring(Position(1, 2*t), minPoint:maxPoint) = offspring(Position(1, 2*t-1), minPoint:maxPoint);
    end
end
