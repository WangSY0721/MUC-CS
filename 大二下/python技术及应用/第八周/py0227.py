import math

def find_special_numbers(m, n):
    return [i for i in range(m, n+1) if '7' in str(i) or i % 7 == 0]

def factorial(x):
    return 1 if x == 0 else x * factorial(x-1)

def gcd(m, n):
    while n != 0:
        m, n = n, m % n
    return m

def lcm(m, n):
    return abs(m*n) // gcd(m, n)

def find_palindromes(m, n):
    return [x for x in range(m, n+1) if str(x) == str(x)[::-1]]

m = int(input("请输入整数m:"))
n = int(input("请输入整数n:"))
print(find_special_numbers(m, n))
print(factorial(m))
print(factorial(n))
print(gcd(m, n))
print(lcm(m, n))
print(find_palindromes(m, n))
