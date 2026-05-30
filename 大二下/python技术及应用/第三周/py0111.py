data = input("请输入一组数据，用空格分隔：")

data_list = data.split()  # 将数据拆分为列表

reversed_tuple = tuple(reversed(data_list))

print("逆序后的数据：")
for item in reversed_tuple:
    print(item, end=" ")
