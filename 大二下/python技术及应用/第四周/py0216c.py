s = [9, 7, 8, 3, 2, 1, 55, 6]

element_count = 0
max_value = None
min_value = None
sum_of_elements = 0

for value in s:
    element_count += 1
    sum_of_elements += value
    if max_value is None or value > max_value:
        max_value = value
    if min_value is None or value < min_value:
        min_value = value

average_value = sum_of_elements / element_count

print("元素个数：", element_count)
print("最大值：", max_value)
print("最小值：", min_value)
print("和：", sum_of_elements)
print("平均值：", average_value)
