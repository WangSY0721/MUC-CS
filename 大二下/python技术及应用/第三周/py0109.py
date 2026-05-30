def find_factors(num):
    factors = [1]
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            factors.append(i)
            complement = num // i
            if complement != i:
                factors.append(complement)
    return factors

def is_perfect_number(num):
    factors = find_factors(num)
    return sum(factors) == num

perfect_numbers = [num for num in range(2, 1001) if is_perfect_number(num)]

print("1000以内的所有完数：", perfect_numbers)
