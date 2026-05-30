n = int(input("请输入整数n:"))

factorial_sum = 0

for i in range(1, n + 1):
    factorial = 1
    for j in range(1, i + 1):
        factorial *= j
    factorial_sum += factorial

print(f"1到{n}的阶乘之和为:{factorial_sum}")
