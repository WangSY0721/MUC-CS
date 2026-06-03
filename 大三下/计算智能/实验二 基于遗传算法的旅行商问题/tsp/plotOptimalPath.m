function plotOptimalPath(Map, MinestRoad_opt, a)
    n = max(size(Map)); % 城市数量
    figure;
    plot(Map(:,1), Map(:,2), '*'); % 绘制城市位置
    hold on;
    for c = 1:n
        text(Map(c, 1), Map(c, 2), [' ' num2str(c)], 'Color', 'k', 'FontWeight', 'b');
    end
    XX = Map(MinestRoad_opt(a,:), 1);
    XX = [XX; Map(MinestRoad_opt(a, 1), 1)];
    YY = Map(MinestRoad_opt(a,:), 2);
    YY = [YY; Map(MinestRoad_opt(a, 1), 2)];
    plot(XX, YY); % 绘制最优路径
    legend('城市', '最优路径');
end