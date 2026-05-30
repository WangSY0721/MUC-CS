# 求n以内所有素数
is_prime = lambda x: all(x % i != 0 for i in range(2, int(x ** 0.5) + 1)) and x > 1

# 求最大公约数
gcd = lambda a, b: a if b == 0 else gcd(b, a % b)

# 求最小公倍数
lcm = lambda a, b: a * b // gcd(a, b)

# 判断是否为水仙花数
is_narcissistic = lambda x: x == sum(int(i) ** 3 for i in str(x))

m = int(input("请输入m: "))
n = int(input("请输入n: "))

print(f"{n}以内所有素数:")
print([x for x in range(2, n + 1) if is_prime(x)])

print(f"最大公约数({m}, {n}): {gcd(m, n)}")
print(f"最小公倍数({m}, {n}): {lcm(m, n)}")

print("所有的水仙花数:")
print([x for x in range(100, 1000) if is_narcissistic(x)])
