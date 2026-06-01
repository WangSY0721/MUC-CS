% 读取图像和水印
image = imread('figure1.png'); % 图像
image = rgb2gray(image);
watermark = imread('logo.png'); % 水印
watermark = rgb2gray(watermark);
watermark = imbinarize(watermark);
figure;
imshow(watermark);
% 对图像进行傅里叶变换
image_f = fft2(double(image));
image_f_shifted = fftshift(image_f); % 将零频率成分移到频谱的中心
%获取频域最大值,生成水印添加比例

% 获取水印的大小
[rows_w, cols_w] = size(watermark);
% 获取图像的大小
[rows_i, cols_i] = size(image);

max_f = max(max(image_f_shifted(1:rows_w,1:cols_w)))*1;
%max_f = 1;
watermark = double(watermark*max_f);
% 将图像b插入到频域图像A中
% 左上角插入
image_f_shifted(1:rows_w, 1:cols_w) = watermark;
% 对频域图像进行逆傅里叶变换
image_inv_shifted = ifftshift(image_f_shifted); % 还原频率零点到左上角
image_inv = uint8(abs(ifft2(image_inv_shifted))); % 逆傅里叶变换
%imwrite(image_inv, '加水印图像.png');
% 对结果图像进行傅里叶变换
image_inv_f = fft2(double(image_inv));
image_inv_f_shifted = fftshift(image_inv_f);

% 显示结果
figure;
subplot(2, 2, 1);imshow(image, []); 
subplot(2, 2, 2);imshow(log(abs(image_f_shifted)+1), []); 
subplot(2, 2, 3);imshow(image_inv, []);
subplot(2, 2, 4);imshow(log(abs(image_inv_f_shifted)+1), []); 

figure;
% 1. 显示加水印后的图像
subplot(2,4,1);
imshow(image);
title('加水印后的图像');
subplot(2,4,2);
imshow(log(abs(image_f_shifted)+1),[]);
title('加水印后的图像');
% 2. 旋转攻击（旋转角度可以调整）
rotation_angle = 30;  % 设置旋转角度
rotated_img = imrotate(image_inv, rotation_angle, 'bilinear', 'crop');
rotated_img = imresize(rotated_img, size(image_inv));  % 调整为与原图相同的大小
subplot(2,4,3);
imshow(rotated_img);
title(['旋转攻击 (' num2str(rotation_angle) '°)']);
subplot(2,4,4);
imshow(log(abs(fftshift(fft2(double(rotated_img))))+1),[]);
title('旋转攻击后频谱图');
% 3. 缩放攻击（缩放比例可以调整）
scale_factor = 0.8;  % 设置缩放比例
scaled_img = imresize(image_inv, scale_factor);
scaled_img = imresize(scaled_img, size(image_inv));  % 调整为与原图相同的大小
subplot(2,4,5);
imshow(scaled_img);
title(['缩放攻击 (' num2str(scale_factor) '倍)']);
subplot(2,4,6);
imshow(log(abs(fftshift(fft2(double(scaled_img))))+1),[]);
title('缩放攻击后频谱图');
% 4. 平移攻击（水平和垂直平移）
translation_x = 30;  % 设置水平平移量
translation_y = 30;  % 设置垂直平移量
tform = affine2d([1 0 0; 0 1 0; translation_x translation_y 1]);
translated_img = imwarp(image_inv, tform);
translated_img = imresize(translated_img, size(image_inv));  % 调整为与原图相同的大小
subplot(2,4,7);
imshow(translated_img);
title(['平移攻击 (' num2str(translation_x) ', ' num2str(translation_y) ')']);
subplot(2,4,8);
imshow(log(abs(fftshift(fft2(double(translated_img))))+1),[]);
title('平移攻击后频谱图');
