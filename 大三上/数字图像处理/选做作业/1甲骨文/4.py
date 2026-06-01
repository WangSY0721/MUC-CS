import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = 'polygon.png'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 反转图像，使得文字为白色，背景为黑色，方便进行轮廓检测
image_inverted = cv2.bitwise_not(image)

# 查找可能表示单个字符/符号的轮廓
contours, _ = cv2.findContours(image_inverted, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# 将轮廓按照从上到下、从左到右的顺序进行排序
def sort_contours(cnts):
    bounding_boxes = [cv2.boundingRect(c) for c in cnts]
    cnts, bounding_boxes = zip(*sorted(zip(cnts, bounding_boxes), key=lambda b: (b[1][1], b[1][0])))
    return cnts, bounding_boxes

sorted_contours, bounding_boxes = sort_contours(contours)

# 提取每个符号并存储它们
extracted_symbols = []
for contour, bbox in zip(sorted_contours, bounding_boxes):
    x, y, w, h = bbox
    if w > 20 and h > 20:
        symbol = image_inverted[y:y+h, x:x+w]
        extracted_symbols.append(symbol)

# 显示提取的符号以确保正确性
fig, axes = plt.subplots(1, len(extracted_symbols), figsize=(12, 3))
if len(extracted_symbols) == 1:  # 如果只有一个符号, 创建一个只含有一个图轴的图表
    axes = [axes]
for ax, symbol in zip(axes, extracted_symbols):
    ax.imshow(symbol, cmap='gray')
    ax.axis('off')
plt.tight_layout()
plt.show()

# 文件保存路径
save_path = './result/'

# DPI（每英寸的像素数）
dpi = 300

# 逐个缩放并保存提取的字符
for i, symbol in enumerate(extracted_symbols):
    # 将DPI转换为像素/厘米的比例
    pixel_per_cm = dpi / 2.54

    # 计算缩放后的宽度和高度
    new_width = int(pixel_per_cm * 1)
    new_height = int(pixel_per_cm * 1)

    # 缩放字符图像
    resized_symbol = cv2.resize(symbol, (new_width, new_height))

    # 保存缩放后的字符图像
    file_name = f"symbol_{i}.png"
    file_path = save_path + file_name
    cv2.imwrite(file_path, resized_symbol)
    print(f"Symbol {i + 1} saved as {file_path}")