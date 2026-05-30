input_str = input("请输入一个字符串：")

letter_count = 0
digit_count = 0
space_count = 0
other_count = 0

for char in input_str:
    if char.isalpha():
        letter_count += 1
    elif char.isdigit():
        digit_count += 1
    elif char.isspace():
        space_count += 1
    else:
        other_count += 1

print("字母的个数：", letter_count)
print("数字的个数：", digit_count)
print("空格的个数：", space_count)
print("其它字符的个数：", other_count)
