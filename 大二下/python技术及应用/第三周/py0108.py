narcissistic_numbers = [num for num in range(100, 1000) if sum(int(digit) ** 3 for digit in str(num)) == num]
print("所有三位数中的水仙花数：", narcissistic_numbers)
