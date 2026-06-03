function x= decode(pop, xmin, xmax, L) %输入参数：
%pop：待解码的种群
%xmin：要转化成的十进制数的最小值 %xmax：要转化成的十进制数的最大值
%L：编码的长度 %输出参数：
%x：转化成的要求范围内的十进制数
[px, py]=size(pop); %求待解码种群 pop 的行数和列数 
for i= 1:py
pop1(:,i)=2.^(py-i).*pop(:,i); 
end
%求 pop1 的每一行之和，得到一个 px 维 1 列的十进制数矩阵
x1=sum(pop1,2);
x=xmin+(xmax-xmin)*x1./(2.^L-1);%将十进制数转化到要求范围内