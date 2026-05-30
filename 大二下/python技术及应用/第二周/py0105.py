n = int(input("请输入整数n:"))

i = 1

while i <= n:
    if i % 3 == 0 or i % 4 == 0:
        print(i, end=' ')
    i += 1
