clear all;
close all;
clc;

images = cell(7,1);
for i = 1:7
    images{i} = imread([num2str(i), '.jpg']);
    if size(images{i},3) > 1
        images{i} = rgb2gray(images{i});
    end
    images{i} = imresize(images{i}, [115 115]);
    images{i} = im2double(images{i});
end

theta = 0:3:179;
interpolation_methods = {'linear', 'spline', 'nearest'};

for img_idx = 1:7
    figure('Name', ['图像 ', num2str(img_idx), ' 的重建结果']);
    
    subplot(2,3,1);
    imshow(images{img_idx}, []);
    title(['原始图像 ', num2str(img_idx)]);
    
    [R, xp] = radon(images{img_idx}, theta);
    
    subplot(2,3,2);
    imagesc(theta, xp, R);
    colormap(gca, hot);
    colorbar;
    title('Sinogram');
    xlabel('角度 (度)');
    ylabel('位移');
    
    for method_idx = 1:3
        method = interpolation_methods{method_idx};
        I_recon = iradon(R, theta, method, 115);
        
        subplot(2,3,method_idx+3);
        imshow(I_recon, []);
        error = norm(I_recon - images{img_idx}, 'fro')/norm(images{img_idx}, 'fro');
        title([method, ' 插值重建']);
        xlabel(['误差: ', num2str(error, '%.4f')]);
        
        F_orig = fftshift(fft2(images{img_idx}));
        F_recon = fftshift(fft2(I_recon));
        
        mag_error = norm(abs(F_recon) - abs(F_orig), 'fro')/norm(abs(F_orig), 'fro');
        phase_error = norm(angle(F_recon) - angle(F_orig), 'fro')/norm(angle(F_orig), 'fro');
        
        fprintf('\n图像 %d - %s插值:\n', img_idx, method);
        fprintf('空间域误差: %.4f\n', error);
        fprintf('幅度谱误差: %.4f\n', mag_error);
        fprintf('相位谱误差: %.4f\n', phase_error);
    end
    
    if img_idx == 4
        figure('Name', ['图像 ', num2str(img_idx), ' 的局部细节']);
        roi = [40 40 35 35];
        
        subplot(2,2,1);
        imshow(imcrop(images{img_idx}, roi), []);
        title('原图局部');
        
        for method_idx = 1:3
            method = interpolation_methods{method_idx};
            I_recon = iradon(R, theta, method, 115);
            subplot(2,2,method_idx+1);
            imshow(imcrop(I_recon, roi), []);
            title([method, ' 插值局部']);
        end
    end
end