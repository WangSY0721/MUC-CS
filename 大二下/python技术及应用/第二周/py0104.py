m = int(input("请输入整数m:"))
n = int(input("请输入整数n:"))

if m % 2 != 0:  # 从偶数开始
    m += 1

even_sum = 0
for i in range(m, n+1, 2):  # range函数左闭右开
    even_sum += i

print(f"区间内所有偶数之和为:{even_sum}")

