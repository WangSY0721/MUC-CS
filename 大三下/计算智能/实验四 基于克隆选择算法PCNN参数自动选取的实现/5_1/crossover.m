function newpop=crossover(pop, pc) %输入参数：

%pop：待交叉的种群
%pc：交叉概率 %输出参数：
%newpop：交叉后的种群 
[px, py]=size(pop);
newpop=zeros(size(pop)); 
for i= 1:px
if(rand<pc)    %若产生的 0 到 1 之间随机数小于交叉概率则进行交叉操作
cpoint = randi([1, 2], [1, py]); %确定发生交叉基因点的位置 
newpop(i,:)=pop(i,:);
newpop(i,cpoint(1))=pop(i, cpoint(2)); %第 i 个个体 cpoint(1)位用第 i 个个体 cpoint(2)位代替
newpop(i,cpoint(2))=pop(i, cpoint(1)); %第 i 个个体 cpoint(2)位用第 i 个个体 cpoint(1)位代替
else
newpop(i,:)=pop(i,:);
end
end