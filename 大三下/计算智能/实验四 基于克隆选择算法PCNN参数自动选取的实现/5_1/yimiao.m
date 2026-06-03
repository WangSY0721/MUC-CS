function newpop=yimiao(pop, bestp, p, n) 
%输入参数：
%pop： 待接种疫苗的种群 %bestp： 目前最好的个体   %p：   疫苗接种的概率
%n：   需要接种疫苗基因的个数 
%输出参数：
%newpop：疫苗接种后产生的种群 
[px,py]=size(pop);
newpop=pop; 
for i= 1:px
if(rand<p)    %若产生的0～1之间随机数小于疫苗接种概率则进行疫苗接种

for j=1:n
ypoint(j)=round(rand*py); %随机选择个体中基因位
if ypoint(j)==0 ypoint(j)=1;      
end
newpop(i,ypoint(j))=bestp(ypoint(j)); %将随机选择的基因位上的基因用 目前最优个体相对应 的基因位上的基因进行替代
end
end
end
