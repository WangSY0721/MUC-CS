def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    fib_series = [0, 1]

    for i in range(2, n):
        next_item = fib_series[i - 1] + fib_series[i - 2]
        fib_series.append(next_item)

    return fib_series

n = int(input('请输入一个整数:'))
print(fibonacci(n))
