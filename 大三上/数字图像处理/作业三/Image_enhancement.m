% 读取原始图像
original_img = imread('D:\王世屹\大学\计算机\数字图像处理\作业\3\图片1.png');  % 读取指定路径的图像
if size(original_img, 3) == 3
    % size 函数用于获取数组的维度大小。这里 size(original_img, 3) 获取的是 original_img 的第三个维度的大小，通常用于表示图像的颜色通道数
    % 如果返回值为3，说明图像是RGB彩色图像，即包含红色、绿色和蓝色三个颜色通道
    original_img = rgb2gray(original_img);  % 如果图像是RGB图像，转换为灰度图
end
% 灰度图像只有一个颜色通道，表示图像的亮度信息

% 点运算：增加亮度
img_point_operation = original_img * 1.2;  % 将图像亮度增加20%
% 由于乘法操作后，像素值可能会超过255（8位图像的最大像素值），所以需要进行后续的类型转换和裁剪操作以确保像素值在有效范围内
img_point_operation = uint8(img_point_operation);  % uint8将像素值转换为8位无符号整数，以确保图像数据在0-255范围内
% 亮度增加操作可能导致像素值超过255，通过uint8函数进行类型转换，同时MATLAB会自动将超过255的值裁剪到255，低于0的值裁剪到0，这样可以确保图像数据在有效的像素值范围内
imwrite(img_point_operation, '增加亮度1.jpg');

% 直方图均衡化
img_equalized = histeq(original_img);  % 对原始图像进行直方图均衡化
% histeq函数是MATLAB中用于执行直方图均衡化的函数，接受一个灰度图像作为输入，并返回经过直方图均衡化处理后的图像
% 直方图均衡化的目的是使图像的像素值分布更加均匀，这样可以使得图像的暗区域和亮区域的细节更加清晰
imwrite(img_equalized, '直方图均衡化1.jpg');

% 空域滤波：高斯滤波
kernel = fspecial('gaussian', [3, 3], 1);  % 创建一个3x3的高斯滤波核，标准差为1
% fspecial函数用于创建特定的滤波核
img_filtered = imfilter(original_img, kernel);  % 使用高斯滤波对图像进行滤波
imwrite(img_filtered, '高斯滤波1.jpg');

% 计算PSNR和SSIM
psnr_point = calculate_psnr(original_img, img_point_operation);  % 计算增加亮度后图像的PSNR值
ssim_point = calculate_ssim(original_img, img_point_operation);  % 计算增加亮度后图像的SSIM值
fprintf('增加亮度 PSNR: %.2f\n', psnr_point);  % 输出PSNR值
fprintf('增加亮度 SSIM: %.4f\n', ssim_point);  % 输出SSIM值

psnr_equalized = calculate_psnr(original_img, img_equalized);  % 计算直方图均衡化后图像的PSNR值
ssim_equalized = calculate_ssim(original_img, img_equalized);  % 计算直方图均衡化后图像的SSIM值
fprintf('直方图均衡化 PSNR: %.2f\n', psnr_equalized);  % 输出PSNR值
fprintf('直方图均衡化 SSIM: %.4f\n', ssim_equalized);  % 输出SSIM值

psnr_filtered = calculate_psnr(original_img, img_filtered);  % 计算高斯滤波后图像的PSNR值
ssim_filtered = calculate_ssim(original_img, img_filtered);  % 计算高斯滤波后图像的SSIM值
fprintf('高斯滤波 PSNR: %.2f\n', psnr_filtered);  % 输出PSNR值
fprintf('高斯滤波 SSIM: %.4f\n', ssim_filtered);  % 输出SSIM值


% 以下是局部函数部分
% PSNR 计算函数
function psnr_value = calculate_psnr(original, processed)
    % 确保图像是double类型
    original = double(original);  % 将原始图像转换为double类型
    processed = double(processed);  % 将处理后的图像转换为double类型
    % 后续的计算需要使用浮点数以避免整数溢出和确保计算精度

    % 计算均方误差（MSE）
    mse = mean((original - processed).^2, 'all');  % 计算所有像素点的均方误差
    % 使用mean函数计算所有像素点误差平方的平均值，即均方误差（MSE），'all' 参数表示对所有元素进行操作。
    psnr_value = 10 * log10(255^2 / mse);  % 根据MSE计算PSNR值
end

% SSIM 计算函数
function ssim_value = calculate_ssim(original, processed)
    % 设置SSIM公式中的常数
    K1 = 0.01;  % 常数1
    K2 = 0.03;  % 常数2
    L = 255;    % 图像的动态范围（8位图像的最大像素值为255）
    C1 = (K1 * L)^2;  % 计算C1常数
    C2 = (K2 * L)^2;  % 计算C2常数

    % 使用高斯核计算均值和方差
    kernel = fspecial('gaussian', [11, 11], 1.5);  % 创建一个较大的高斯滤波核，用于平滑计算
    mu_x = imfilter(double(original), kernel);  % 对原图进行高斯滤波，计算均值
    mu_y = imfilter(double(processed), kernel);  % 对处理后的图像进行高斯滤波，计算均值
    sigma_x = imfilter(double(original).^2, kernel) - mu_x.^2;  % 计算原图的方差
    sigma_y = imfilter(double(processed).^2, kernel) - mu_y.^2;  % 计算处理后图像的方差
    sigma_xy = imfilter(double(original) .* double(processed), kernel) - mu_x .* mu_y;  % 计算协方差

    % 计算SSIM指数
    numerator = (2 * mu_x .* mu_y + C1) .* (2 * sigma_xy + C2);  % SSIM公式的分子部分
    denominator = (mu_x.^2 + mu_y.^2 + C1) .* (sigma_x + sigma_y + C2);  % SSIM公式的分母部分
    ssim_map = numerator ./ denominator;  % 计算每个像素的SSIM值
    ssim_value = mean(ssim_map(:));  % 计算所有像素点的平均SSIM值
end



