% 生成一个随机的RGB图像并保存为tigers.bmp
function createRGBImage
    % 设置图像的大小
    nrow = 256;
    ncol = 256;

    % 生成随机的RGB图像
    img = rand(nrow, ncol, 3);

    % 保存为tigers.bmp
    imwrite(img, 'tigers.bmp');
end


