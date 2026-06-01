import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.transform import hough_line, hough_line_peaks

# 加载图像
file_path = 'original.png'
image = cv2.imread(file_path, 0)  # 以灰度图像加载图像


# 应用锐化滤波器
kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])  # 锐化滤波器
sharpened_image = cv2.filter2D(image, -1, kernel)


# 边缘检测
edges = cv2.Canny(image, 50, 150, apertureSize=3)

# 图像均衡化
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
equalized_image = clahe.apply(image)

# 找到图像的质心
M = cv2.moments(edges)
if M["m00"] != 0:
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
else:
    cX, cY = 0, 0  # 如果质心为零，将质心设为原点，以避免除零错误

# 使用Hough/Radon变换找到文本的倾斜角度
# 使用Hough变换检测线条
tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360)
h, theta, d = hough_line(edges, theta=tested_angles)

# 获取线条的角度
accum, angles, dists = hough_line_peaks(h, theta, d)

# 假设文本与最显著的线条对齐，取第一条线条的角度
# （因为hough_line_peaks返回按强度降序排序的线条）
if angles.size > 0:
    main_angle = angles[0]
else:
    main_angle = 0  # 如果未找到线条，则假设文本水平

# 计算旋转角度以使文本水平对齐
rotation_angle = np.rad2deg(main_angle)

# 计算旋转矩阵
rot_mat = cv2.getRotationMatrix2D((cX, cY), rotation_angle, 1.0)

# 围绕质心旋转图像
corrected_image = cv2.warpAffine(image, rot_mat, image.shape[::-1], flags=cv2.INTER_LINEAR)

# 绘制结果图像
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# 原始图像并标记质心
ax1.imshow(image, cmap='gray')
ax1.scatter([cX], [cY], color='red')
ax1.set_title('Original Image with Centroid')

# 边缘检测图像
ax2.imshow(edges, cmap='gray')
ax2.set_title('Edge Detection')

# 校正后的图像
ax3.imshow(corrected_image, cmap='gray')
ax3.set_title('Corrected Image')

# 显示图像
plt.tight_layout()
plt.show()

cv2.imwrite("corrected.png", corrected_image)
