num1 = float(input("请输入第一个数: "))
num2 = float(input("请输入第二个数: "))
num3 = float(input("请输入第三个数: "))
num4 = float(input("请输入第四个数: "))

numbers = [num1, num2, num3, num4]

sorted_numbers = sorted(numbers, reverse=True)

print("四个数从大到小排序的结果为:", sorted_numbers)
