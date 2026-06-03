function [NewX] = FindElse_FUN(xi,xk,MaxPID,MinPID)
NewX=zeros(1,4);
NewX(1,1)=xi(1,1)+rand(1)*(xi(1,1)-xk(1,1));
NewX(1,2)=xi(1,2)+rand(1)*(xi(1,2)-xk(1,2));
NewX(1,3)=xi(1,3)+rand(1)*(xi(1,3)-xk(1,3));
for i=1:1:3
if NewX(1,i)>MaxPID(i)
NewX(1,i)=MaxPID(i);
else if NewX(1,i)<MinPID(i)
NewX(1,i)=MinPID(i);
end
end
end
end