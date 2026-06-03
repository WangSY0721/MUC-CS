function IterBestJ( BestITAE,CycleTimes,style)
for i=1:1:CycleTimes
iter(i)=i;
end
figure(2)
if style==1
plot(iter,BestITAE,'-');
end
xlabel('迭代次数'),ylabel('目标函数值');
hold on
end