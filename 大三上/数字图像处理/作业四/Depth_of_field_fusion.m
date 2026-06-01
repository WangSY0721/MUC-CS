% 读取两幅原始彩色图像（确保图像路径正确）
img1 = im2double(imread('D:/王世屹/大学/计算机/数字图像处理/作业/4/图片1.png'));  % 图像1
img2 = im2double(imread('D:/王世屹/大学/计算机/数字图像处理/作业/4/图片2.png'));  % 图像2

% 调整图像尺寸，使它们的尺寸一致
[min_rows, min_cols, ~] = size(img1);  % 获取第一幅图像的尺寸（行数和列数）
[min_rows2, min_cols2, ~] = size(img2);  % 获取第二幅图像的尺寸（行数和列数）

min_rows = min(min_rows, min_rows2);  % 获取最小的行数
min_cols = min(min_cols, min_cols2);  % 获取最小的列数

img1 = imresize(img1, [min_rows, min_cols]);  % 调整图像1的大小
img2 = imresize(img2, [min_rows, min_cols]);  % 调整图像2的大小

% 图像融合：低频图像使用低通滤波器，高频图像使用高通滤波器
% 定义高斯滤波器
low_pass_filter = fspecial('gaussian', [30, 30], 10);  % 低通滤波器（提取低频成分）
high_pass_filter = fspecial('gaussian', [30, 30], 5);  % 高频滤波器（提取高频成分）

% 使用滤波器提取低频成分
low_freq_image = imfilter(img1, low_pass_filter, 'replicate');
    
% 使用滤波器提取高频成分
high_freq_image = img2 - imfilter(img2, high_pass_filter, 'replicate');

% 将低频和高频成分合成图像
    hybrid_image = low_freq_image + high_freq_image;

% 显示融合后的图像
figure;
imshow(hybrid_image);
title('图像融合结果');

