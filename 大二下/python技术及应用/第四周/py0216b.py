s = [9, 7, 8, 3, 2, 1, 55, 6]

element_count = len(s)
max_value = s[0]
min_value = s[0]
sum_of_elements = 0

for i in range(-element_count, 0):
    if s[i] > max_value:
        max_value = s[i]
    if s[i] < min_value:
        min_value = s[i]
    sum_of_elements += s[i]

average_value = sum_of_elements / element_count

# 输出结果
print("元素个数：", element_count)
print("最大值：", max_value)
print("最小值：", min_value)
print("和：", sum_of_elements)
print("平均值：", average_value)
