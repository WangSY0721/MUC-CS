import random

def generate_sets():
    total_length = 10
    length_a = random.randint(3, 7)
    length_b = total_length - length_a

    A = set(random.sample(range(11), length_a))
    B = set(random.sample(range(11), length_b))

    return A, B

def display_set_info(set_a, set_b):
    print(f"集合 A: {set_a}")
    print(f"长度: {len(set_a)}")
    print(f"最大值: {max(set_a)}")
    print(f"最小值: {min(set_a)}")

    print(f"集合 B: {set_b}")
    print(f"长度: {len(set_b)}")
    print(f"最大值: {max(set_b)}")
    print(f"最小值: {min(set_b)}")

    print(f"并集: {set_a | set_b}")
    print(f"交集: {set_a & set_b}")
    print(f"A 差 B: {set_a - set_b}")
    print(f"B 差 A: {set_b - set_a}")

A, B = generate_sets()
display_set_info(A, B)
