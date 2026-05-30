def sum_to_n(n):
    return sum(range(1, n + 1))

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_divisors(n):
    return [i for i in range(1, n) if n % i == 0]

def is_perfect(n):
    divisors = find_divisors(n)
    if sum(divisors) == n:
        return True, divisors
    return False, []

n = int(input("请输入一个正整数n："))

print(f"1到{n}的和是：{sum_to_n(n)}")

prime_dict = {i: "是" if is_prime(i) else "否" for i in range(1, n + 1)}
print(f"{n}以内所有素数：{prime_dict}")

perfect_dict = {}
for i in range(1, n + 1):
    is_perf, divisors = is_perfect(i)
    if is_perf:
        perfect_dict[i] = divisors
print(f"{n}以内所有完数及其因子：{perfect_dict}")
