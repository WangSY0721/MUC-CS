def read_scores(filename):
    scores = []
    with open(filename, 'r') as file:
        for line in file:
            scores.append(int(line.strip()))
    return scores

def calculate_statistics(scores):
    max_score = max(scores)
    min_score = min(scores)
    average_score = sum(scores) / len(scores)
    return max_score, min_score, average_score

filename = "分数.txt"

scores = read_scores(filename)

max_score, min_score, average_score = calculate_statistics(scores)

print(f"最大成绩: {max_score}")
print(f"最小成绩: {min_score}")
print(f"平均成绩: {average_score:.2f}")
