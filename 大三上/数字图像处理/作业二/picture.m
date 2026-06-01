% 读取图像文件
img = imread('picture1.jpg');

% 显示图像并手动选择地面区域的四个角点
% ginput(4) 会让用户在图像中手动选择四个点，返回这些点的 x 和 y 坐标
figure; imshow(img);
title('按顺时针方向从左下角开始，顺时针选择地面区域的四个角点');
[x, y] = ginput(4);  % 手动选择图像中的4个点，分别存储x和y坐标

% 设置矫正后图像的宽度和高度
% width 和 height 代表校正后图像的目标尺寸
width = 640;   % 目标图像的宽度
height = 480; % 目标图像的高度

% 将用户选择的四个角点坐标存储在 selected_points 中
selected_points = [x(1), y(1);  % 第一个点（左下角）
                   x(2), y(2);  % 第二个点（左上角）
                   x(3), y(3);  % 第三个点（右上角）
                   x(4), y(4)]; % 第四个点（右下角）

% 定义校正后图像中，四个角点的目标位置
% desired_points 包含目标图像中四个角点的坐标
desired_points = [0, height;     % 左下角
                  0, 0;          % 左上角
                  width, 0;      % 右上角
                  width, height];% 右下角

% 构建线性方程组 A*h = b，用于计算透视变换矩阵
A = [];  % 初始化空矩阵 A，用于存储方程的系数
b = [];  % 初始化空向量 b，用于存储方程的结果

% 遍历四个角点，生成线性方程组
for i = 1:4
    % 原始图像中的角点坐标
    x_orig = selected_points(i, 1);  % 角点的 x 坐标
    y_orig = selected_points(i, 2);  % 角点的 y 坐标
    
    % 校正后图像中相应角点的目标坐标
    x_dest = desired_points(i, 1);  % 目标 x 坐标
    y_dest = desired_points(i, 2);  % 目标 y 坐标

    % 构建两组方程，分别描述 x' 和 y' 的变换关系
    A = [A;
         x_orig, y_orig, 1, 0, 0, 0, -x_orig*x_dest, -y_orig*x_dest;  % x' 的方程
         0, 0, 0, x_orig, y_orig, 1, -x_orig*y_dest, -y_orig*y_dest];% y' 的方程
     
    % 将 x' 和 y' 的值添加到结果向量 b 中
    b = [b; x_dest; y_dest];
end

% 通过解线性方程组 A*h = b，得到透视变换矩阵的元素 h
h = A \ b;

% 使用解得的参数构造 3x3 透视变换矩阵 H
% h 是 8x1 的列向量，我们需要将其扩展为 3x3 矩阵，并在最后一行添加 [0, 0, 1]
H = [h(1), h(2), h(3);
     h(4), h(5), h(6);
     h(7), h(8), 1];

% 创建投影变换对象 tform，用于将透视变换应用到图像上
tform = projective2d(H');

% 使用 imwarp 函数进行透视校正，并将校正后的图像存储到 corrected_image
% 'Outputview' 和 imref2d 用于定义输出图像的大小，即矫正后的图像尺寸
corrected_image = imwarp(img, tform, 'Outputview', imref2d([height, width]));

% 显示校正后的图像
figure; imshow(corrected_image);
title('校正后的地面正视图');
