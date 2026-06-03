function feature = feature_lattice(img)
% 粗网格特征提取
% 先统一大小
for i=1:length(img)
bw2 = im2bw(img{i},graythresh(img{i}));
bw_7050 = imresize(bw2,[70,50]);
% 再等分成5×5的网格，一次统计每个网格中黑色像素点的个数
for cnt = 1:7
    for cnt2 = 1:5
        Atemp = sum(bw_7050(((cnt*10-9):(cnt*10)),((cnt2*10-9):(cnt2*10))));  % 10*10box
        lett((cnt-1)*5+cnt2) = sum(Atemp);
    end
end
% 计算比例，返回特征矩阵
lett = ((100-lett)/100);
lett = lett';
feature(:,i) = lett;
end