n = int(input("请输入一个整数n："))

# 用列表推导式创建二维数组
Yanghui_triangle = [[1] * (i + 1) for i in range(n)]

# 用循环产生数组中的数据
for i in range(2, n):
    for j in range(1, i):
        Yanghui_triangle[i][j] = Yanghui_triangle[i - 1][j - 1] + Yanghui_triangle[i - 1][j]

for row in Yanghui_triangle:
    print(" ".join(map(str, row)))
