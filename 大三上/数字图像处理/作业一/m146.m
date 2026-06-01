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
img_noisy_blurred = img_blurred + noise;

noise_power = var(noise(:));
signal_power = var(img_blurred(:));
NSR = noise_power / signal_power;

H = psf2otf(PSF, [M N]);
G = fft2(img_noisy_blurred);
H_conj = conj(H);
F = H_conj ./ (abs(H).^2 + NSR) .* G;
img_restored = real(ifft2(F));

img_restored = max(0, min(1, img_restored));

figure(1);
subplot(2,2,1);
imshow(original_img);
title('原始图像', 'FontSize', 12);

subplot(2,2,2);
imshow(img_blurred);
title('模糊图像', 'FontSize', 12);

subplot(2,2,3);
imshow(img_noisy_blurred);
title('带噪声的模糊图像', 'FontSize', 12);

subplot(2,2,4);
imshow(img_restored);
title('维纳滤波复原后的图像', 'FontSize', 12);

noisy_SNR = 10 * log10(mean(original_img(:).^2) / mean((original_img(:)-img_noisy_blurred(:)).^2));
restored_SNR = 10 * log10(mean(original_img(:).^2) / mean((original_img(:)-img_restored(:)).^2));

fprintf('\n信噪比比较：\n');
fprintf('带噪声模糊图像的SNR = %.2f dB\n', noisy_SNR);
fprintf('复原后图像的SNR = %.2f dB\n', restored_SNR);
fprintf('计算得到的NSR = %.6f\n', NSR);

figure(2);
rect = [100 100 50 50];
subplot(2,2,1);
imshow(original_img);
title('原始图像', 'FontSize', 12);
rectangle('Position',rect,'EdgeColor','r','LineWidth',1.5);

subplot(2,2,2);
imshow(img_blurred);
title('模糊图像', 'FontSize', 12);
rectangle('Position',rect,'EdgeColor','r','LineWidth',1.5);

subplot(2,2,3);
imshow(img_noisy_blurred);
title('带噪声的模糊图像', 'FontSize', 12);
rectangle('Position',rect,'EdgeColor','r','LineWidth',1.5);

subplot(2,2,4);
imshow(img_restored);
title('维纳滤波复原后的图像', 'FontSize', 12);
rectangle('Position',rect,'EdgeColor','r','LineWidth',1.5);

figure(3);
subplot(2,2,1);
imshow(imcrop(original_img, rect));
title('原始图像局部放大', 'FontSize', 12);

subplot(2,2,2);
imshow(imcrop(img_blurred, rect));
title('模糊图像局部放大', 'FontSize', 12);

subplot(2,2,3);
imshow(imcrop(img_noisy_blurred, rect));
title('带噪声的模糊图像局部放大', 'FontSize', 12);

subplot(2,2,4);
imshow(imcrop(img_restored, rect));
title('维纳滤波复原后的图像局部放大', 'FontSize', 12);