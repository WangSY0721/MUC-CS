function [offspring,t,MM1,memory,location]=clonep(Population,objection,m,h);
[MM,location]=sort(objection,'descend');
%MM:升序的 objection,location:排序的位置关系
%初始克隆 memory ,产生 C2 矩阵
memory=Population(location(1:m),:); %生成 m 个较好的初始记忆库
MM1=MM(1:m);
C1=memory;
ke=sum(MM1)/m; ke1=MM1/ke;
ke2=floor(5*ke1);
ke3=fliplr(ke2); %选择 ke3 个抗体进行克隆 
t=sum(ke3);
C2=zeros(t,h); 
y= 1;
for i= 1:m;
for j=1:ke3(i);
C2(y,:)=C1(i,:);
y=y+1;
end
end
offspring=C2;