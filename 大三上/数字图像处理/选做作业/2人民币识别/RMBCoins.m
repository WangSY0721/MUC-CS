function totalRMB = DetectRMBCoinsByRadius()

    imgPath = 'D:\王世屹\大学\计算机\数字图像处理\作业\选做作业\2人民币识别\coins.jpg';
    origImg = imread(imgPath);
    figure('Name','原始图像','NumberTitle','off');
    imshow(origImg);
    title('原始图像展示');
    
    grayImg = rgb2gray(origImg);
    grayImg = medfilt2(grayImg,[3 3]);  

    edgeImg = edge(grayImg,'canny');
    
    [centers, radii] = imfindcircles(grayImg,[15 120],...
        'ObjectPolarity','dark','Sensitivity',0.92);
    
    figure('Name','检测圆','NumberTitle','off');
    imshow(origImg);
    hold on;
    viscircles(centers, radii,'Color','r');
    title('检测到的硬币圆心和半径');
    hold off;

    count1Jiao = 0; 
    count5Jiao = 0;  
    count1Yuan = 0; 
    
    for i = 1:length(radii)
        currentRadius = radii(i);
        
        xMin = max(floor(centers(i,1) - currentRadius),1);
        yMin = max(floor(centers(i,2) - currentRadius),1);
        width = min(floor(2*currentRadius), size(origImg,2)-xMin);
        height = min(floor(2*currentRadius), size(origImg,1)-yMin);
        coinImg = imcrop(origImg, [xMin, yMin, width, height]);
        
        if currentRadius < 25
            count1Jiao = count1Jiao + 1;
        elseif currentRadius < 35
            count5Jiao = count5Jiao + 1;
        else
            count1Yuan = count1Yuan + 1;
        end
    end
    
    total1Jiao = count1Jiao * 0.1;
    total5Jiao = count5Jiao * 0.5;
    total1Yuan = count1Yuan * 1.0;
    
    totalRMB = total1Jiao + total5Jiao + total1Yuan;
    
    disp('识别结果：');
    disp(['1角硬币数量：', num2str(count1Jiao), ' 枚']);
    disp(['5角硬币数量：', num2str(count5Jiao), ' 枚']);
    disp(['1元硬币数量：', num2str(count1Yuan), ' 枚']);
    disp(' ');
    disp(['1角硬币对应金额：', num2str(total1Jiao), ' 元']);
    disp(['5角硬币对应金额：', num2str(total5Jiao), ' 元']);
    disp(['1元硬币对应金额：', num2str(total1Yuan), ' 元']);
    disp(' ');
    disp(['识别到的人民币总金额（元）: ', num2str(totalRMB)]);
    
end
