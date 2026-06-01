import cv2

# 读取原图像
image = cv2.imread('playground.jpg')

# 增强局部对比度以模拟HDR效果
hdr_image = cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)

# 保存结果
cv2.imwrite('hdr_image.jpg', hdr_image)
