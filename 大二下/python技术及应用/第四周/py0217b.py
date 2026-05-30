original_list = [1, 7, 8, 8, 8, 8, 2, 2, 2, 55, 6, 6]

unique_list = []

for item in original_list:
    if item not in unique_list:
        unique_list.append(item)

print("去重后的列表（保持原顺序）：", unique_list)
