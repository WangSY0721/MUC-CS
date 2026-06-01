clear all;
close all;
clc;

img = imread('原图.jpg');
if size(img,3)==3
    img = rgb2gray(img);
end
img = im2double(img);

psf_size = 9;
[x, y] = meshgrid(-floor(psf_size/2):floor(psf_size/2));

motion_len = 4;
motion_angle = 45;
sigma_m = 0.5;

defocus_radius = 2;
sigma_d = 1.0;

theta = motion_angle * pi / 180;
x_motion = x * cos(theta) + y * sin(theta);
motion_PSF = exp(-x_motion.^2 / (2 * motion_len^2));
motion_PSF = motion_PSF .* exp(-(x.^2 + y.^2)/(2 * sigma_m^2));
motion_PSF = motion_PSF / sum(motion_PSF(:));

r = sqrt(x.^2 + y.^2);
defocus_PSF = exp(-r.^2/(2 * sigma_d^2)) .* (r <= defocus_radius);
defocus_PSF = defocus_PSF / sum(defocus_PSF(:));

PSF = conv2(motion_PSF, defocus_PSF, 'same');
PSF = PSF / sum(PSF(:));

[M, N] = size(img);
H = psf2otf(PSF, [M N]);
H_conj = conj(H);
H_abs_sq = abs(H).^2;

window = ones(5) / 25;
local_mean = imfilter(img, window, 'replicate');
local_var = imfilter(img.^2, window, 'replicate') - local_mean.^2;
noise_var = median(local_var(:));
signal_var = max(mean(local_var(:)) - noise_var, 0);
NSR = noise_var / (signal_var + eps);

reg_param = 0.005;
F_wiener = (H_conj ./ (H_abs_sq + NSR + reg_param)) .* fft2(img);
img_wiener = real(ifft2(F_wiener));

img_wiener = max(0, min(1, img_wiener));
img_wiener = adapthisteq(img_wiener, 'ClipLimit', 0.005, 'Distribution', 'rayleigh');
img_wiener = imguidedfilter(img_wiener, img, 'NeighborhoodSize', [3 3], 'DegreeOfSmoothing', 0.1^2);

iterations = 25;
img_lr = img;
PSF_flip = rot90(PSF, 2);
damping = 0.8;

for i = 1:iterations
    temp = imfilter(img_lr, PSF, 'conv', 'circular');
    ratio = img ./ (temp + eps);
    correction = imfilter(ratio, PSF_flip, 'conv', 'circular');
    img_lr = img_lr .* (correction.^damping);
    
    if mod(i, 5) == 0
        img_lr = imguidedfilter(img_lr, img, 'NeighborhoodSize', [3 3], 'DegreeOfSmoothing', 0.1^2);
    end
end

figure('Name', '图像复原结果对比', 'Position', [100 100 1200 400]);
subplot(2,2,1);
imshow(img); title('原始图像');

subplot(2,2,2);
imagesc(PSF); 
axis image; 
colormap(gca, parula);
colorbar;
title('混合点扩散函数(PSF)');

subplot(2,2,3);
imshow(img_wiener); title('维纳滤波结果');

subplot(2,2,4);
imshow(img_lr); title('L-R迭代结果');

figure('Name', '局部细节对比');
rect = [size(img,1)/2-40 size(img,2)/2-40 80 80];

subplot(1,3,1);
imshow(imcrop(img, rect));
title('原图局部');

subplot(1,3,2);
imshow(imcrop(img_wiener, rect));
title('维纳滤波局部');

subplot(1,3,3);
imshow(imcrop(img_lr, rect));
title('L-R迭代局部');