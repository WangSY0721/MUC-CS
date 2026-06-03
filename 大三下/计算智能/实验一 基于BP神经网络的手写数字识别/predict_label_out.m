for i=1:length(test_data)
    out4(i)=find(predict_label4(:,i)==max(predict_label4(:,i)));
end

%% 计算正确率
[u,v]=find(test_label==1);
label=u';
error=label-out4;
accuracy=size(find(error==0),2)/size(label,2)
