is_prime = lambda x: x > 1 and all(x % y != 0 for y in range(2, int(x ** 0.5) + 1))

n = int(input("请输入一个正整数n："))

prime_numbers = [x for x in range(2, n+1) if is_prime(x)]
print(f"{n}以内的所有素数是：{prime_numbers}")
