def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_twin_primes(limit):
    twin_primes = {}
    for num in range(2, limit):
        if is_prime(num) and is_prime(num + 2):
            twin_primes[num] = num + 2
    return twin_primes

twin_primes_dict = find_twin_primes(1000)

print(twin_primes_dict)
