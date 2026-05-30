numbers = []
for i in range(8):
    num = int(input("请输入第{}个数：".format(i+1)))
    numbers.append(num)

sorted_numbers = sorted(numbers, reverse=True)

print("从大到小排序后的列表：", sorted_numbers)
