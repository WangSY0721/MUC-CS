import cv2
import numpy as np

# 读取图像
image = cv2.imread('playground.jpg')

# 创建一个模糊的图像
blurred = cv2.GaussianBlur(image, (25, 25), 0)

# 创建掩模，模仿移轴效果，中间区域清晰，其他区域逐渐模糊
mask = np.zeros_like(image, dtype=np.float32)
rows, cols, _ = image.shape
mask[int(rows*0.3):int(rows*0.7), :] = 1

# 使用掩模将原始图像和模糊图像结合
tilt_shift_image = (image * mask + blurred * (1 - mask)).astype(np.uint8)

# 保存结果
cv2.imwrite('tilt_shift_image.jpg', tilt_shift_image)
