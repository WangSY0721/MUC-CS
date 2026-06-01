clear all;
close all;
clc;

img = imread('lena.jpg');
if size(img,3)==3
    img = rgb2gray(img);
end
img = imresize(img,[256 256]);

figure(1);
subplot(1,2,1);
imshow(img);
title('原始图像');

len = 25;
theta = 25;
PSF = fspecial('motion',len,theta);

img_blurred = imfilter(img,PSF,'conv','circular');

subplot(1,2,2);
imshow(img_blurred);
title('运动模糊后的图像');

figure(2);
surf(PSF);
title('运动模糊点扩散函数的3D可视化');

imwrite(img_blurred,'blurred_lena.jpg');

figure(3);
imshow(PSF,[]);
title('运动模糊点扩散函数');

fprintf('原始图像大小: %d x %d\n', size(img));
fprintf('模糊核大小: %d x %d\n', size(PSF));
fprintf('模糊角度: %d度\n', theta);
fprintf('模糊长度: %d像素\n', len);