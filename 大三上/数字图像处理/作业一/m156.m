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

H = psf2otf(PSF, [M N]);
G = fft2(img_noisy_blurred);

noise_power = var(noise(:));
signal_power = var(img_blurred(:));
NSR = noise_power / signal_power;
H_conj = conj(H);
F_wiener = H_conj ./ (abs(H).^2 + NSR) .* G;
img_wiener = real(ifft2(F_wiener));
img_wiener = max(0, min(1, img_wiener));

epsilon = 1e-6;
F_inverse = G ./ (H + epsilon);
img_inverse = real(ifft2(F_inverse));
img_inverse = max(0, min(1, img_inverse));

iterations = 20;
img_lr = img_noisy_blurred;
PSF_flip = rot90(PSF,2);
for i = 1:iterations
    temp = imfilter(img_lr, PSF, 'conv', 'circular');
    ratio = img_noisy_blurred ./ (temp + eps);
    img_lr = img_lr .* imfilter(ratio, PSF_flip, 'conv', 'circular');
end

snr_wiener = 10 * log10(mean(original_img(:).^2) / mean((original_img(:)-img_wiener(:)).^2));
snr_inverse = 10 * log10(mean(original_img(:).^2) / mean((original_img(:)-img_inverse(:)).^2));
snr_lr = 10 * log10(mean(original_img(:).^2) / mean((original_img(:)-img_lr(:)).^2));
snr_noisy = 10 * log10(mean(original_img(:).^2) / mean((original_img(:)-img_noisy_blurred(:)).^2));

figure(1);
subplot(2,3,1); imshow(original_img); title('原始图像');
subplot(2,3,2); imshow(img_noisy_blurred); title('带噪声的模糊图像');
subplot(2,3,3); imshow(img_wiener); title('维纳滤波复原');
subplot(2,3,4); imshow(img_inverse); title('逆滤波复原');
subplot(2,3,5); imshow(img_lr); title('LR迭代复原');

rect = [100 100 50 50];
figure(2);
subplot(2,3,1); imshow(imcrop(original_img,rect)); title('原始图像局部');
subplot(2,3,2); imshow(imcrop(img_noisy_blurred,rect)); title('噪声模糊图像局部');
subplot(2,3,3); imshow(imcrop(img_wiener,rect)); title('维纳滤波局部');
subplot(2,3,4); imshow(imcrop(img_inverse,rect)); title('逆滤波局部');
subplot(2,3,5); imshow(imcrop(img_lr,rect)); title('LR迭代局部');

fprintf('\n不同方法的SNR比较：\n');
fprintf('带噪声模糊图像的SNR = %.2f dB\n', snr_noisy);
fprintf('维纳滤波复原后的SNR = %.2f dB\n', snr_wiener);
fprintf('逆滤波复原后的SNR = %.2f dB\n', snr_inverse);
fprintf('LR迭代复原后的SNR = %.2f dB\n', snr_lr);