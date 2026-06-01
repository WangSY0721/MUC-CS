% 读取两幅原始彩色图像（确保图像路径正确）
ImageFile1 = imread("D:/王世屹/大学/计算机/数字图像处理/作业/4/图片10.png");
ImageFile2 = imread("D:/王世屹/大学/计算机/数字图像处理/作业/4/图片9.png");

% 显示混合后的图像
imshow(hybrid_images(ImageFile1, ImageFile2, 9));

% 定义混合图像的函数
function re = hybrid_images(ImageFile1, ImageFile2, radius_input)
    % 将图像转换为双精度型，以便进行数学运算
    I1 = double(ImageFile1);
    I2 = double(ImageFile2);
    
    % 定义输出图像的路径
    ImgFileout = 'D:/王世屹/大学/计算机/数字图像处理/作业/4/图像混合结果3.png';
    
    % 获取半径值
    radius = radius_input;
    
    % 对两幅图像进行傅里叶变换，并进行中心化
    I1_ = fftshift(fft2(I1));
    I2_ = fftshift(fft2(I2));
    
    % 获取图像的尺寸
    [m, n, z] = size(I1);
    
    % 创建高斯滤波器，并进行归一化
    h = fspecial('gaussian', [m, n], radius);
    h = h./max(max(h));
    
    % 初始化融合后的图像
    J_ = zeros(size(I1_));
    
    % 对每个颜色通道进行处理
    for colorI = 1:3
        J_(:,:,colorI) = I1_(:,:,colorI).*(1-h) + I2_(:,:,colorI).*h;
    end
    
    % 进行逆傅里叶变换，并取实部
    J = uint8(real(ifft2(ifftshift(J_))));
    imshow(J);

    % 保存输出图像
    imwrite(J, ImgFileout);
    
    % 返回结果图像
    re = J;
end