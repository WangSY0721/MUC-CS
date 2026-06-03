function newpop=mutation(pop, pm) %输入参数：
%pop：待变异的种群
%pm：变异概率 %输出参数：
%newpop：变异后的种群 
[px, py]=size(pop);
newpop=zeros(size(pop)); 
for i= 1:px
if(rand<pm)    %若产生的0～1之间随机数小于变异概率则进行变异操作

mpoint=round(rand*py); %确定发生变异的位置
if mpoint==0 mpoint= 1;     
end
newpop(i,:)=pop(i,:);
if newpop(i,mpoint)==0 %将种群中个体变异点元素进行变异，0 变 1 ，1 变 0 
    newpop(i,mpoint)=1;
else
newpop(i,mpoint)=0; 
end
else
newpop(i,:)=pop(i,:); %若产生的 0～1 之间随机数大于或等于变异概率则不进行变异操作 
end
end