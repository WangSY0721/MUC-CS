% 检查是否安装了图像处理工具箱
if ~license('test', 'image_toolbox')
    error('需要安装图像处理工具箱！');
end

% 读取原始图像
original_img = imread('D:\王世屹\大学\计算机\数字图像处理\作业\3\图片6.jpg');

% 检查是否是彩色图像
if size(original_img, 3) ~= 3
    error('请输入一张彩色图像！');
end

% 自定义滤镜
% 1. 圆形滤镜
circle_filter = [
    0 0 1 1 1 0 0;
    0 1 1 1 1 1 0;
    1 1 1 1 1 1 1;
    1 1 1 1 1 1 1;
    1 1 1 1 1 1 1;
    0 1 1 1 1 1 0;
    0 0 1 1 1 0 0
];
circle_filter = circle_filter / sum(circle_filter(:)); 

% 2. 三角形滤镜
triangle_filter = [
    0 0 0 1 0 0 0;
    0 0 1 1 1 0 0;
    0 1 1 1 1 1 0;
    1 1 1 1 1 1 1
];
triangle_filter = 3*triangle_filter / sum(triangle_filter(:)); % 归一化

% 3. 心形滤镜
heart_filter = [
    0 0 1 1 0 1 1 0 0;
    0 1 1 1 1 1 1 1 0;
    1 1 1 1 1 1 1 1 1;
    1 1 1 1 1 1 1 1 1;
    0 1 1 1 1 1 1 1 0;
    0 0 1 1 1 1 1 0 0;
    0 0 0 1 1 1 0 0 0
];
heart_filter = 4*heart_filter / sum(heart_filter(:)); % 归一化、

% 对每个通道分别应用滤波器
img_circle = zeros(size(original_img), 'like', original_img);
img_triangle = zeros(size(original_img), 'like', original_img);
img_heart = zeros(size(original_img), 'like', original_img);
% zeros函数用于创建一个所有元素都是0的矩阵
% size(original_img)获取原始图像的尺寸，包括其行数和列数
% 'like', original_img指定新创建的矩阵应该与original_img具有相同的数据类型。这意味着如果original_img是一个uint8类型的图像，那么新创建的矩阵也将是uint8类型

for channel = 1:3
    img_circle(:, :, channel) = imfilter(original_img(:, :, channel), circle_filter, 'conv');
    img_triangle(:, :, channel) = imfilter(original_img(:, :, channel), triangle_filter, 'conv');
    img_heart(:, :, channel) = imfilter(original_img(:, :, channel), heart_filter, 'conv');
end
% imfilter函数用于将指定的滤波器应用于图像。
% original_img(:, :, channel)提取原始图像的第channel个通道。
% 'conv'参数指定使用卷积操作，这意味着滤波器将与图像的每个局部区域进行卷积，以计算输出图像中对应像素的值。

% 保存处理后的图像
imwrite(uint8(img_circle), '圆形处理.jpg');
imwrite(uint8(img_triangle), '三角形处理.jpg');
imwrite(uint8(img_heart), '心形处理.jpg');

% 反卷积（逐通道恢复图像）
estimated_nsr = 0.01; % 估计噪声功率比
% 估计噪声功率比（NSR）是一个标量值，用于表示图像中噪声功率与信号功率的比率。这个值用于维纳滤波去噪过程中，以平衡去噪效果和图像细节的保留
img_restored_circle = zeros(size(original_img), 'like', original_img);
img_restored_triangle = zeros(size(original_img), 'like', original_img);
img_restored_heart = zeros(size(original_img), 'like', original_img);

for channel = 1:3
    img_restored_circle(:, :, channel) = deconvwnr(double(img_circle(:, :, channel)), circle_filter, estimated_nsr);
    img_restored_triangle(:, :, channel) = deconvwnr(double(img_triangle(:, :, channel)), triangle_filter, estimated_nsr);
    img_restored_heart(:, :, channel) = deconvwnr(double(img_heart(:, :, channel)), heart_filter, estimated_nsr);
end
% deconvwnr函数是MATLAB中用于执行维纳滤波去噪和恢复的函数。
% double(img_circle(:, :, channel)) 将滤波后的图像通道转换为double类型，这是deconvwnr函数的要求
% 维纳滤波是一种用于信号处理和图像处理的线性滤波技术，旨在从噪声干扰的观测信号中恢复出原始信号，是基于统计理论的最优滤波器之一

% 保存恢复后的图像
imwrite(uint8(img_restored_circle), '圆形恢复.jpg');
imwrite(uint8(img_restored_triangle), '三角形恢复.jpg');
imwrite(uint8(img_restored_heart), '心形恢复.jpg');

% 显示结果
figure;
subplot(2, 4, 1), imshow(original_img), title('原始图像');
subplot(2, 4, 2), imshow(uint8(img_circle)), title('圆形处理');
subplot(2, 4, 3), imshow(uint8(img_triangle)), title('三角形处理');
subplot(2, 4, 4), imshow(uint8(img_heart)), title('心形处理');
subplot(2, 4, 5), imshow(uint8(img_restored_circle)), title('圆形恢复');
subplot(2, 4, 6), imshow(uint8(img_restored_triangle)), title('三角形恢复');
subplot(2, 4, 7), imshow(uint8(img_restored_heart)), title('心形恢复');


