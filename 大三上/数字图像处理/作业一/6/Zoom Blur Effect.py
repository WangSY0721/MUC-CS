import cv2
import numpy as np

# 读取图像
image = cv2.imread('playground.jpg')
rows, cols = image.shape[:2]

# 创建滑动变焦效果
center = (cols / 2, rows / 2)
num_layers = 30  # 定义模糊层数
zoomed_image = np.zeros_like(image, dtype=np.float32)

for i in range(1, num_layers + 1):
    scale = 1 + (i / 100)  # 缩放比例
    zoomed_layer = cv2.resize(image, None, fx=scale, fy=scale)
    zoomed_layer = zoomed_layer[(zoomed_layer.shape[0] - rows) // 2:(zoomed_layer.shape[0] - rows) // 2 + rows,
                                (zoomed_layer.shape[1] - cols) // 2:(zoomed_layer.shape[1] - cols) // 2 + cols]
    zoomed_image += zoomed_layer / num_layers

# 保存结果
zoomed_image = zoomed_image.astype(np.uint8)
cv2.imwrite('zoom_blur_image.jpg', zoomed_image)
