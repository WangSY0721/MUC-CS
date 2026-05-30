a = int(input("请输入第一个数:"))
b = int(input("请输入第二个数:"))

gcd = 1  # 最大公约数

for i in range(1, min(a, b) + 1):  # 求最大公约数
    if a % i == 0 and b % i == 0:
        gcd = i

lcm = a * b // gcd  # 最小公倍数

print(f"{a}和{b}的最大公约数是:{gcd}")
print(f"{a}和{b}的最小公倍数是:{lcm}")
