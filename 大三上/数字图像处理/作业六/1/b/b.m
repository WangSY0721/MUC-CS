clear all;
close all;
clc;

original_img = imread('lena.jpg');
if size(original_img,3)==3
    original_img = rgb2gray(original_img);
end
original_img = imresize(original_img,[256 256]);
original_img = im2double(original_img);

len = 25;
theta = 25;
PSF = fspecial('motion',len,theta);
img_blurred = imfilter(original_img,PSF,'conv','circular');

[M, N] = size(img_blurred);
mean_val = 0;
var_val = 0.001;
noise = sqrt(var_val) * randn(M, N) + mean_val;

img_noisy = img_blurred + noise;

img_noisy = max(0, min(1, img_noisy));

figure(1);
subplot(1,3,1);
imshow(original_img);
title('原始图像');

subplot(1,3,2);
imshow(img_blurred);
title('模糊图像');

subplot(1,3,3);
imshow(img_noisy);
title('添加噪声后的图像');

figure(2);
histogram(noise(:), 100, 'Normalization', 'probability');
title('噪声分布直方图');
xlabel('噪声值');
ylabel('概率');
grid on;

noise_mean = mean(noise(:));
noise_var = var(noise(:));
fprintf('噪声的统计特征：\n');
fprintf('理论均值 = 0，实际均值 = %.6f\n', noise_mean);
fprintf('理论方差 = %.3f，实际方差 = %.6f\n', var_val, noise_var);

figure(3);
rect = [100 100 50 50];
subplot(1,3,1);
imshow(original_img);
title('原始图像局部');
rectangle('Position',rect,'EdgeColor','r');

subplot(1,3,2);
imshow(img_blurred);
title('模糊图像局部');
rectangle('Position',rect,'EdgeColor','r');

subplot(1,3,3);
imshow(img_noisy);
title('添加噪声后的局部');
rectangle('Position',rect,'EdgeColor','r');

imwrite(img_noisy, '添加噪声的模糊图像.jpg');

figure(4);
subplot(1,3,1);
imshow(imcrop(original_img, rect));
title('原始图像局部放大');

subplot(1,3,2);
imshow(imcrop(img_blurred, rect));
title('模糊图像局部放大');

subplot(1,3,3);
imshow(imcrop(img_noisy, rect));
title('添加噪声后的局部放大');

original_power = mean(original_img(:).^2);
noise_power = mean(noise(:).^2);
SNR = 10 * log10(original_power/noise_power);
fprintf('图像信噪比(SNR) = %.2f dB\n', SNR);