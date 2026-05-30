def calculate_average(filename):
    total = 0
    count = 0
    with open(filename, 'r') as file:
        for line in file:
            try:
                score = float(line.strip())
                total += score
                count += 1
            except ValueError:
                print(f"Invalid score found and skipped: {line.strip()}")
    if count == 0:
        return 0
    return total / count

filename = '分数.txt'
average = calculate_average(filename)
print(f"The average score is: {average}")
