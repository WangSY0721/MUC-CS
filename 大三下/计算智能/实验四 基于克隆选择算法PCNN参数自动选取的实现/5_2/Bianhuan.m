function Y=Bianhuan(X)
%此函数的功能是：将矩阵

%[1 2 3  % 4 5 6  % 7 8 9]
%变换成矩阵：

%[0 0 0 0 0
% 0 1 2 3 0
% 0 4 5 6 0
% 0 7 8 9 0
% 0 0 0 0 0]
[m,n]=size(X);
Y=zeros(m+2,n+2);
for i= 1:m+2
for j=1:n+2
if i==1 | j==1 | i==m+2 | j==n+2 
    Y(i,j)=0;
else
Y(i,j)=X(i-1,j-1);
end
end
end
