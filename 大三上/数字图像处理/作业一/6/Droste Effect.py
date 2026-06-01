from PIL import Image

# 读取图像
image = Image.open('playground.jpg')

# 初始化循环嵌套的参数
droste_image = image.copy()
size_factor = 0.6  # 缩小比例
iterations = 5  # 嵌套层数
for i in range(iterations):
    # 缩小图像
    droste_image = droste_image.resize((int(droste_image.width * size_factor), int(droste_image.height * size_factor)))

    # 贴图到原图中心
    offset = ((image.width - droste_image.width) // 2, (image.height - droste_image.height) // 2)
    image.paste(droste_image, offset)

# 保存结果
image.save('droste_image.jpg')

