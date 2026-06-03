% Map1=[82,7;91,38;83,46;71,44;64,60;68,58; 83,69;87,76;74,78;71,71]; 
Map1 = [82, 7; 91, 38; 83, 46; 71, 44; 64, 60; 68, 58; 83, 69; 87, 76; 74, 78; 71, 71; 53, 50; 52, 21; 60, 39; 37, 84; 22, 91; 25, 75; 38, 52; 58, 11; 69, 33; 90, 23];

MaxIter=500;   %最大迭代次数
Pop_Size=500;  %种群规模 
pc=0.2;        %选择概率
pm=0.01;        %变异概率
[opt,fval, MinestRoad_opt, a]=tspga(Map1,MaxIter,Pop_Size,pm,pc);
disp('最优路径：'); disp(opt);
disp('最短里程：'); disp(fval);

plotOptimalPath(Map1, MinestRoad_opt, a);