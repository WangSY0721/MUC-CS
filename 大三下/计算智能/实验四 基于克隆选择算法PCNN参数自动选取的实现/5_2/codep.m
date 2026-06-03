function [ax,bx]=codep(X);
Wa=0.01:0.005:2.6;%旋转参数的取值范围 
Wb=0.01:0.005:2.6;%尺度参数的取值范围
[R,C]=size(X); 
for i= 1:R
aa(i,:)=X(i, 1:8);
a1(i,:)=num2str(aa(i,:));%数字转换成字符串
a2(i)=bin2dec(a1(i,:)); %将 2 进制表示为 10 进制，位数最多不能多于 10 位 
bb(i,:)=X(i,9:16);
b1(i,:)=num2str(bb(i,:));
b2(i)=bin2dec(b1(i,:));
end
ax=Wa(a2+1);  
bx=Wb(b2+1);