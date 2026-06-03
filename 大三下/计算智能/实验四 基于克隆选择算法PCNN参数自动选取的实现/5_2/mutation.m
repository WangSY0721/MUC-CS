%变异函数。Coffspring 为变异前的种群；Moffspring 为变异后的子代；
function Moffspring=mutation(Coffspring,pm)
Moffspring=Coffspring;  [r1,c1]=size(Coffspring);
for n=1:r1;
for m= 1:c1;
rm=rand(1); if rm<pm;
Moffspring(n,m)=~Coffspring(n,m); end
end
end
