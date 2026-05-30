numbers = []
while True:
    num = input("请输入一个正数（输入'q'结束）：")
    if num.lower() == 'q':
        break
    try:
        num = float(num)
        if num > 0:
            numbers.append(num)
        else:
            print("请输入正数！")
    except ValueError:
        print("请输入有效的数字！")

numbers.sort()

if numbers:
    average = sum(numbers) / len(numbers)
    print("排序后的列表：", numbers)
    print("平均值：", average)
else:
    print("列表为空，无法计算平均值。")
