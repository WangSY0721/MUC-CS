%随机产生初始种群，其中 popsize 为每代群体数量，
% 基因数目且 a=c+d c 为图像配准时旋转角度参数的编码位数;d 为图像配准时尺度变换参数的编码位数
function Population=initialization(popsize,a);
Population = logical(randi([0, 1], popsize, a));