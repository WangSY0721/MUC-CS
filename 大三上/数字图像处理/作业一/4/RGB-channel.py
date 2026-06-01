from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def get_rgb_channels(image_path):
    # 打开图像文件
    img = Image.open(image_path)  # 使用 image_path 变量传递图像路径

    # 确保图像被转换为RGB格式
    img = img.convert('RGB')

    # 将图像转换为NumPy数组
    img_array = np.array(img)

    # 创建三个副本，用于分别存储红色、绿色和蓝色通道的图像
    red_channel = img_array.copy()
    green_channel = img_array.copy()
    blue_channel = img_array.copy()

    # 只保留红色通道，其他通道设置为0
    red_channel[:, :, 1] = 0  # 将绿色通道的值设为0
    red_channel[:, :, 2] = 0  # 将蓝色通道的值设为0

    # 只保留绿色通道，其他通道设置为0
    green_channel[:, :, 0] = 0  # 将红色通道的值设为0
    green_channel[:, :, 2] = 0  # 将蓝色通道的值设为0

    # 只保留蓝色通道，其他通道设置为0
    blue_channel[:, :, 0] = 0  # 将红色通道的值设为0
    blue_channel[:, :, 1] = 0  # 将绿色通道的值设为0

    # 创建一个Matplotlib的子图，1行4列
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))

    # 显示原始图像
    axs[0].imshow(img)  # 显示原始图像
    axs[0].set_title('Original Image')  # 设置标题
    axs[0].axis('off')  # 关闭坐标轴

    # 显示红色通道图像
    axs[1].imshow(red_channel)  # 显示红色通道
    axs[1].set_title('Red Channel')  # 设置标题
    axs[1].axis('off')  # 关闭坐标轴

    # 显示绿色通道图像
    axs[2].imshow(green_channel)  # 显示绿色通道
    axs[2].set_title('Green Channel')  # 设置标题
    axs[2].axis('off')  # 关闭坐标轴

    # 显示蓝色通道图像
    axs[3].imshow(blue_channel)  # 显示蓝色通道
    axs[3].set_title('Blue Channel')  # 设置标题
    axs[3].axis('off')  # 关闭坐标轴

    # 展示所有生成的图像
    plt.show()  # 显示图像


# 使用示例
image_path = 'picture2.jpg'  # 输入图像的路径
get_rgb_channels(image_path)  # 调用函数处理图像
