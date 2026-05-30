def print_compact_aligned_multiplication_table():
    max_num_width = max(len(str(num)) for num in range(1, 10))
    max_product_width = len("81")

    expression_width = max_num_width + 1 + max_num_width + 1 + max_product_width

    total_width = expression_width * 9 + 8

    for i in range(1, 10):
        expressions = []
        for j in range(1, i + 1):
            left_part = f"{j}x{i}="
            right_part = f"{j * i}".rjust(max_product_width)
            expression = f"{left_part:<{max_num_width + 1 + max_num_width + 1}}{right_part}"
            expressions.append(expression)

        aligned_row = ' '.join(expressions).rjust(total_width)
        print(aligned_row)

print_compact_aligned_multiplication_table()


