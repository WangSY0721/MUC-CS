def perfect_numbers(n):
    find_divisors = lambda x: [i for i in range(1, x) if x % i == 0]

    perfects_and_divisors = []

    for number in range(1, n + 1):
        divisors = find_divisors(number)
        if sum(divisors) == number:
            perfects_and_divisors.append((number, divisors))
    return perfects_and_divisors

def main():
    try:
        n = int(input("请输入一个整数，以找出所有小于或等于该数的完数及其因子："))
        if n < 1:
            print("请输入一个大于0的整数。")
            return
        perfects = perfect_numbers(n)
        if not perfects:
            print(f"没有找到小于或等于 {n} 的完数。")
        else:
            for perfect, divisors in perfects:
                print(f"完数: {perfect}, 因子: {divisors}")
    except ValueError:
        print("输入无效，请输入一个整数。")

if __name__ == "__main__":
    main()
