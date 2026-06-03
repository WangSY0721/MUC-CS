% ÔöÇ¿Í¼Ïñº¯Êý
function ZZQ=zqtu(Input,XX,DD,MM,LLumda)
scahh=size(Input,1);scacc=size(Input,2);
G=[];
for i=1:scahh
for j=1:scacc
G(i,j)=XX(4)*DD/(LLumda(i,j)+XX(2))*(Input(i,j)-XX(3)*MM(i,j))+MM(i,j).^XX(1);
end
end
ZZQ=G;