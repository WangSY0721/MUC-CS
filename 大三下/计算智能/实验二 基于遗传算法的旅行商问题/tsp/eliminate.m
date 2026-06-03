function  elim=eliminate(x,y)
for n=1:length(y)
x=x(find(x~=y(n))); %È¥³ý x ÖÐµÄ y
end
elim=x; end