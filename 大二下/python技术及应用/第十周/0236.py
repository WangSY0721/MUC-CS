import random
import string

def generate_passwords(num_passwords, length):
    characters = string.ascii_letters + string.digits
    passwords = [''.join(random.choices(characters, k=length)) for _ in range(num_passwords)]
    return passwords

num_passwords = 10
length = 8
passwords = generate_passwords(num_passwords, length)
for i, password in enumerate(passwords, 1):
    print(f"Password {i}: {password}")
