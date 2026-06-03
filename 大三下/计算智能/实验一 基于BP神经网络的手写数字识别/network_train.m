function [net, tr] = network_train(train_data, train_label) 
    %% BP 神经网络的创建、训练
    layer = 25; % 隐含层神经元
    net = newff(train_data, train_label, layer);

    net.trainParam.epochs = 10; 
    net.trainParam.lr = 0.1;
    net.trainParam.goal = 0.001;
    net.trainFcn = 'trainrp';

    % 网络训练
    [net, tr] = train(net, train_data, train_label);
    
    % 可视化损失曲线
    figure;
    plot(tr.perf, 'b', 'LineWidth', 2);
    hold on;
    plot(tr.vperf, 'r', 'LineWidth', 2);
    hold off;
    title('Training and Validation Loss');
    xlabel('Epoch');
    ylabel('Loss');
    legend('Training Loss', 'Validation Loss');
    grid on;
end
