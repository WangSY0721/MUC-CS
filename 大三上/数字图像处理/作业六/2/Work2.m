clear all;
close all;
clc;

blurred_img = imread('原图.jpg');
if size(blurred_img,3)==3
    blurred_img = rgb2gray(blurred_img);
end
blurred_img = im2double(blurred_img);

psf_size = 31;
center = floor(psf_size/2) + 1;
PSF = zeros(psf_size);

[X,Y] = meshgrid(1:psf_size, 1:psf_size);
sigma_center = 0.5;
sigma_line = 1.5;

horizontal = exp(-(Y-center).^2/(2*sigma_line^2)) .* exp(-(X-center).^2/(2*sigma_center^2));
vertical = exp(-(X-center).^2/(2*sigma_line^2)) .* exp(-(Y-center).^2/(2*sigma_center^2));
PSF = horizontal + vertical;

PSF = PSF / sum(PSF(:));

[M, N] = size(blurred_img);
H = psf2otf(PSF, [M N]);

NSR = 0.015;
G = fft2(blurred_img);
H_conj = conj(H);
F_wiener = H_conj ./ (abs(H).^2 + NSR) .* G;
img_wiener = real(ifft2(F_wiener));
img_wiener = max(0, min(1, img_wiener));

img_wiener = wiener2(img_wiener, [3 3], 0.05);

iterations = 100;
img_lr = blurred_img;
PSF_flip = rot90(PSF, 2);
damping = 0.95;

for i = 1:iterations
    temp = imfilter(img_lr, PSF, 'conv', 'circular');
    ratio = blurred_img ./ (temp + eps);
    correction = imfilter(ratio, PSF_flip, 'conv', 'circular');
    img_lr = img_lr .* (correction.^damping);
    
    if mod(i, 15) == 0
        img_lr = wiener2(img_lr, [3 3], 0.02);
    end
end

figure('Name', '图像复原结果', 'Position', [100 100 800 600]);
subplot(2,2,1);
imshow(blurred_img);
title('原始模糊图像', 'FontSize', 12);

subplot(2,2,2);
imagesc(PSF);
axis image;
colormap(gca, jet);
h = colorbar;
ylabel(h, '\times10^{-3}');
title('点扩散函数(PSF)', 'FontSize', 12);

subplot(2,2,3);
imshow(img_wiener);
title('维纳滤波复原结果', 'FontSize', 12);

subplot(2,2,4);
imshow(img_lr);
title('LR迭代复原结果', 'FontSize', 12);

figure('Name', '局部细节对比', 'Position', [900 100 800 300]);
rect = [200 200 100 100];

subplot(1,3,1);
imshow(imcrop(blurred_img, rect));
title('原始图像局部', 'FontSize', 12);

subplot(1,3,2);
imshow(imcrop(img_wiener, rect));
title('维纳滤波局部', 'FontSize', 12);

subplot(1,3,3);
imshow(imcrop(img_lr, rect));
title('LR迭代局部', 'FontSize', 12);

compute_contrast = @(img) (max(img(:)) - min(img(:))) / (max(img(:)) + min(img(:)) + eps);
compute_sharpness = @(img) std2(imfilter(img, fspecial('laplacian')));

contrast_blurred = compute_contrast(blurred_img);
contrast_wiener = compute_contrast(img_wiener);
contrast_lr = compute_contrast(img_lr);

sharpness_blurred = compute_sharpness(blurred_img);
sharpness_wiener = compute_sharpness(img_wiener);
sharpness_lr = compute_sharpness(img_lr);

fprintf('\n图像质量评价指标:\n');
fprintf('原始模糊图像 - 对比度: %.4f, 清晰度: %.4f\n', contrast_blurred, sharpness_blurred);
fprintf('维纳滤波结果 - 对比度: %.4f, 清晰度: %.4f\n', contrast_wiener, sharpness_wiener);
fprintf('LR迭代结果 - 对比度: %.4f, 清晰度: %.4f\n', contrast_lr, sharpness_lr);