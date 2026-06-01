import cv2
import numpy as np
from matplotlib import pyplot as plt

# 读取图像
image_path = 'playground.jpg'  # 替换为你的图片路径
image = cv2.imread(image_path)  # 使用OpenCV读取图像文件

# 将图像转换为灰度图像
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 从BGR（默认）转换为灰度

# 二值化处理
# cv2.threshold函数将图像分为黑白两部分
# 参数说明：输入图像，阈值（127），最大值（255），阈值类型（二值化）
_, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)


# 生成半色调图像的函数
def halftone(image, dot_size=5):
    # 创建与输入图像相同尺寸的空白图像，用于存储半色调图像
    halftone_image = np.zeros(image.shape, dtype=np.uint8)

    # 遍历输入图像，以dot_size为步长处理区域
    for y in range(0, image.shape[0], dot_size):
        for x in range(0, image.shape[1], dot_size):
            # 获取当前区域的子图像
            region = image[y:y + dot_size, x:x + dot_size]
            # 计算当前区域的平均亮度
            avg_brightness = np.mean(region)
            # 根据平均亮度决定半色调点的半径
            radius = int(dot_size * (avg_brightness / 255))  # 将亮度映射到点的大小
            # 在halftone_image上绘制一个实心圆，表示半色调点
            cv2.circle(halftone_image, (x + radius // 2, y + radius // 2), radius, 255, -1)
    return halftone_image  # 返回生成的半色调图像


# 应用半色调函数生成半色调图像
halftone_image = halftone(gray_image)

# 显示结果
plt.figure(figsize=(10, 10))  # 设置图像显示窗口大小

# 显示原始图像
plt.subplot(1, 3, 1)
plt.title('Original Image')  # 设置子图标题
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # 将BGR转换为RGB以正确显示
plt.axis('off')  # 不显示坐标轴

# 显示二值图像
plt.subplot(1, 3, 2)
plt.title('Binary Image')  # 设置子图标题
plt.imshow(binary_image, cmap='gray')  # 使用灰度色图显示二值图像
plt.axis('off')  # 不显示坐标轴

# 显示半色调图像
plt.subplot(1, 3, 3)
plt.title('Halftone Image')  # 设置子图标题
plt.imshow(halftone_image, cmap='gray')  # 使用灰度色图显示半色调图像
plt.axis('off')  # 不显示坐标轴

plt.tight_layout()  # 自动调整子图之间的间距
plt.show()  # 显示图像

# 保存结果
cv2.imwrite('binary_image.jpg', binary_image)  # 保存二值图像
cv2.imwrite('halftone_image.jpg', halftone_image)  # 保存半色调图像

