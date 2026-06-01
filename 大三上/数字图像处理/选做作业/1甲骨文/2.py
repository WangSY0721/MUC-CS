import cv2
import numpy as np
from matplotlib import pyplot as plt

# 处理图像的函数
def process_image(image_path):
    # 以灰度图像加载图像
    image = cv2.imread(image_path, 0)

    # 使用中值滤波器去除噪声，同时保留边缘
    median_filtered_image = cv2.medianBlur(image, 3)

    # 使用阈值处理获取二值图像
    _, binary_image = cv2.threshold(median_filtered_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 使用RETR_CCOMP模式在二值图像上查找轮廓，保留两级层次
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个空白图像用于绘制轮廓
    contour_image = np.zeros_like(binary_image)

    # 只绘制没有子轮廓的外部轮廓
    for idx, (contour, hier) in enumerate(zip(contours, hierarchy[0])):
        if hier[2] < 0:  # 没有子轮廓
            cv2.drawContours(contour_image, contours, idx, (255, 255, 255), 1)

    # 将轮廓图像与二值图像相结合，得到最终图像
    final_image_with_text = cv2.bitwise_or(contour_image, binary_image)

    return final_image_with_text

# 清理图像的函数
def clean_image(binary_image):
    # 应用全局阈值处理，将图像转换为二值图像
    _, binary_image = cv2.threshold(binary_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 定义形态学运算的核大小
    kernel_size = (3, 3)
    kernel = np.ones(kernel_size, np.uint8)

    # 先腐蚀后膨胀，增强文字的连通性
    eroded = cv2.erode(binary_image, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)

    # 在膨胀后的图像上查找轮廓
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 定义轮廓的最小面积，用于噪声滤除
    min_area = 50

    # 根据最小面积过滤出大的轮廓
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    # 创建一个与输入图像具有相同尺寸的全黑图像
    cleaned_img = np.zeros_like(dilated)

    # 在黑色图像上绘制大的轮廓，保留文字部分
    cv2.drawContours(cleaned_img, large_contours, -1, (255, 0, 0), thickness=cv2.FILLED)

    # 将图像反转回原始形式
    cleaned_img = cv2.bitwise_not(cleaned_img)

    return cleaned_img

# 处理校正后的图像，获取保留文本的最终二值图像
final_image_with_text = process_image('corrected.png')

# 清理图像，获取保留文字部分的清理后的图像
final_cleaned_image = clean_image(final_image_with_text)

# 将清理后的图像保存到输出文件
output_path = 'binary.png'
cv2.imwrite(output_path, final_cleaned_image)
