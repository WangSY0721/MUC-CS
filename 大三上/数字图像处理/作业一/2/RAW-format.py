from PIL import Image
import numpy as np


def image_to_raw(input_image_path, output_raw_path):
    # 打开图像
    img = Image.open(input_image_path)

    # 将图像转换为RGB格式
    img = img.convert('RGB')

    # 获取图像的像素数据
    pixel_data = np.array(img)

    # 将像素数据保存为RAW格式
    with open(output_raw_path, 'wb') as raw_file:
        raw_file.write(pixel_data.tobytes())

# 使用示例
input_image_path = 'picture1.jpg'  # 输入图像的路径
output_raw_path = 'picture1.raw'  # 输出RAW图像的路径
image_to_raw(input_image_path, output_raw_path)
