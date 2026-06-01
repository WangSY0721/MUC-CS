import cv2
import numpy as np
import matplotlib.pyplot as plt

# 载入图像
image_path = 'binary.png'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 应用阈值化去除噪声和背景
ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 形态学操作去除小噪点
kernel = np.ones((5,5),np.uint8)
morphed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
plt.figure(figsize=(6, 10))
plt.imshow(morphed, cmap='gray')
plt.show()

# 寻找和绘制轮廓
contours, hierarchy = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 假设最大的轮廓是甲骨的外轮廓
cnt = max(contours, key = cv2.contourArea)

# 绘制轮廓
contour_img = image.copy()
cv2.drawContours(contour_img, [cnt], 0, (255,255,255), 10)

# 创建图像掩膜，并将其填充为黑色
mask = np.zeros_like(image)
cv2.drawContours(mask, [cnt], 0, (255,255,255), cv2.FILLED)

# 将非多边形区域置为黑色
result = cv2.bitwise_and(image, mask)

plt.figure(figsize=(6, 10))
plt.imshow(contour_img, cmap='gray')
plt.show()

plt.figure(figsize=(6, 10))
plt.imshow(result, cmap='gray')
plt.show()
cv2.imwrite("polygon.png",result)
