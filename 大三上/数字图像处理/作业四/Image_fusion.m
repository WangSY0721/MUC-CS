% 读取图像
img1 = imread('D:/王世屹/大学/计算机/数字图像处理/作业/4/图片1.png'); % 图像1
img2 = imread('D:/王世屹/大学/计算机/数字图像处理/作业/4/图片2.png'); % 图像2

% 确保图像尺寸一致
if size(img1) ~= size(img2)
    img2 = imresize(img2, [size(img1, 1), size(img1, 2)]);
end

% 显示图像1并手动选择椭圆区域
figure;
imshow(img1);
title('Select an elliptical region to crop from Image 1');

% 手动选择椭圆区域
h = imellipse;
position = wait(h); % 等待用户完成绘制椭圆区域

% 获取椭圆的掩码
mask = createMask(h); % 创建椭圆掩码

% 提取图像1中的对应区域
cropped_img1 = bsxfun(@times, img1, cast(mask, 'like', img1)); % 使用掩码提取区域

% 显示裁剪后的区域
figure;
imshow(cropped_img1);
title('Cropped Elliptical Region from Image 1');

% 获取椭圆区域的边界
stats = regionprops(mask, 'BoundingBox');
x_start = round(stats.BoundingBox(1)); % 起始x坐标
y_start = round(stats.BoundingBox(2)); % 起始y坐标
width = round(stats.BoundingBox(3));   % 裁剪区域宽度
height = round(stats.BoundingBox(4));  % 裁剪区域高度

% 确保图像2的尺寸足够容纳裁剪区域
if size(img2, 1) < y_start + height || size(img2, 2) < x_start + width
    error('The crop region is out of bounds for Image 2.');
end

% 将裁剪区域加到图像2中对应的位置，保留椭圆形状
fused_image = img2; % 初始化融合图像为图2

% 获取目标区域
target_region = fused_image(y_start:y_start+height-1, x_start:x_start+width-1, :);

% 使用掩码将椭圆区域叠加到图像2
for c = 1:3 % 对每个颜色通道进行操作
    target_region(:,:,c) = target_region(:,:,c) .* uint8(~mask(y_start:y_start+height-1, x_start:x_start+width-1)) + ...
                           cropped_img1(y_start:y_start+height-1, x_start:x_start+width-1, c) .* uint8(mask(y_start:y_start+height-1, x_start:x_start+width-1));
end

% 将处理过的区域放回图像2
fused_image(y_start:y_start+height-1, x_start:x_start+width-1, :) = target_region;

% 显示最终融合后的图像
figure;
imshow(fused_image);
title('Fused Image with Elliptical Region');
