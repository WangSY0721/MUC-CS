from max_match_with_tree import load_dictionary
from participle.test.metric import calculate_metrics


def load_bigram_frequencies(bigram_file):
    """
    加载二元语法频率数据，返回一个字典。
    """
    bigram_freq = {}
    with open(bigram_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                w1, w2, freq = parts
                bigram_freq[(w1, w2)] = int(freq)
    return bigram_freq


def calculate_bigram_score(tokens, bigram_freq):
    """
    计算分词结果的二元语法频率之和，作为评分。
    """
    score = 0
    for i in range(len(tokens) - 1):
        bigram = (tokens[i], tokens[i + 1])
        freq = bigram_freq.get(bigram, 0)
        score += freq
    return score


def tokenize_with_ngram_selection(forward_list, backward_list, hmm_list, bigram_freq):
    """
    选择二元语法评分更高的分词结果。
    """
    total = []
    for index in range(len(forward_list)):

        # 获得forward_result分词的结果
        forward_result = forward_list[index]
        print("前向最大匹配结果", forward_result)

        # 获得backward分词的结果
        backward_result = backward_list[index]
        print("后向最大匹配结果", backward_result)

        # 获得hmm分词的结果
        hmm_result = hmm_list[index]
        print("hmm结果", hmm_result)
        index += 1

        # 计算二元语法评分
        forward_score = calculate_bigram_score(forward_result, bigram_freq)
        backward_score = calculate_bigram_score(backward_result, bigram_freq)
        hmm_score = calculate_bigram_score(hmm_result, bigram_freq)

        # 选择评分更高的分词结果
        if forward_score >= backward_score and forward_score >= hmm_score:
            selected_tokens = forward_result
        if backward_score >= forward_score and backward_score >= hmm_score:
            selected_tokens = backward_result
        if hmm_score >= backward_score and hmm_score >= forward_score:
            selected_tokens = hmm_result

        selected_result = ' '.join(selected_tokens)
        total.append(selected_result)

    return total


if __name__ == "__main__":
    # 加载二元语法频率数据
    bigram_file = '../data/bigram_freq_output.txt'
    bigram_freq = load_bigram_frequencies(bigram_file)

    # 指定hmm分词结果作为候选输入
    hmm_result_file = '../results/hmm_output.txt'
    with open(hmm_result_file, 'r', encoding='utf-8') as f:
        hmm_list = []
        for lines in f:
            hmm_list.append(lines.split(' '))

    # 指定前向分词结果作为候选输入
    forward_result_file = '../results/forward_output.txt'
    with open(hmm_result_file, 'r', encoding='utf-8') as f:
        forward_list = []
        for lines in f:
            forward_list.append(lines.split(' '))

    # 指定后向分词结果作为候选输入
    backward_result_file = '../results/backward_output.txt'
    with open(backward_result_file, 'r', encoding='utf-8') as f:
        backward_list = []
        for lines in f:
            backward_list.append(lines.split(' '))

    # 进行分词处理，针对每一行选择最佳分词结果
    tokenized_result = tokenize_with_ngram_selection(
        forward_list, backward_list, hmm_list, bigram_freq)

    # 保存最终的分词结果到指定文件
    output_file = '../results/comparison_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for tokenized_line in tokenized_result:
            f.write(tokenized_line)

    print(f"\n分词结果已保存到 {output_file}")

    # 计算精确度、召回率和F1
    standard_file = '../test/metric/jieba_metric.txt'
    precision, recall, f1_score = calculate_metrics(standard_file, output_file)

    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")
