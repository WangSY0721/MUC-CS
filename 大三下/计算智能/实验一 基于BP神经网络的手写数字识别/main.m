clc;
clear all;
close all;
% 读取图像
root='./data';
img=read_train(root);

% 粗网格特征提取
img_feature=feature_lattice(img);
ann_data=img_feature;

% 构造标签
class=10;   
numberpclass=500; 
ann_label=zeros(class,numberpclass*class);
for i=1:class
    for j=numberpclass*(i-1)+1:numberpclass*i
        ann_label(i,j)=1;
    end
end

% 选定训练集和测试集
k=rand(1,numberpclass*class); 
[m,n]=sort(k); 
ntraindata=4500;
ntestdata=500;
train_data=ann_data(:,n(1:ntraindata));
test_data=ann_data(:,n(ntraindata+1:numberpclass*class));
train_label=ann_label(:,n(1:ntraindata));
test_label=ann_label(:,n(ntraindata+1:numberpclass*class));

% 创建BP神经网络
net=network_train(train_data,train_label); 
% 测试BP神经网络
predict_label=network_test(test_data,net); 

% 计算正确率
for i=1:length(test_data)
    out(i)=find(predict_label(:,i)==max(predict_label(:,i)));
end

[u,v]=find(test_label==1); 
label=u';
error=label-out;

accuracy=size(find(error==0),2)/size(label,2);
accuracy