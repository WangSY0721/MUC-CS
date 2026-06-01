import re
from tqdm import tqdm
from max_match_with_tree import forward_max_match, backward_max_match, load_dictionary
from participle.test.metric import calculate_metrics


def contains_chinese(text):
    """
    检查给定文本是否包含汉字。
    """
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def clean_spaces(tokens):
    """
    清理多余的空格，确保词与词之间只有一个空格。
    """
    return ' '.join([token for token in tokens if token.strip()])


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


def tokenize_with_ngram_selection(input_file, forward_dict, backward_dict, bigram_freq):
    """
    对文本进行分词处理，对于每个最小的中文句子，选择二元语法评分更高的分词结果。
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tokenized_content = []

    for line in tqdm(lines, desc="Processing lines with n-gram selection"):
        sentence = line.strip()
        if not sentence:
            continue

        # 使用正则表达式分割句子，保留分隔符
        segments = re.split(r'(\s+)', sentence)

        result = []
        for segment in segments:
            if segment.isspace():
                # 保留原始的空白符
                result.append(segment)
                continue

            if contains_chinese(segment):
                # 对于含有汉字的最小句子，分别进行前向和后向最大匹配分词
                forward_tokens = forward_max_match(forward_dict, segment)
                backward_tokens = backward_max_match(backward_dict, segment)

                # 计算二元语法评分
                forward_score = calculate_bigram_score(forward_tokens, bigram_freq)
                backward_score = calculate_bigram_score(backward_tokens, bigram_freq)

                # 选择评分更高的分词结果
                if forward_score >= backward_score:
                    selected_tokens = forward_tokens
                else:
                    selected_tokens = backward_tokens
            else:
                # 非中文内容，直接作为一个词
                selected_tokens = [segment]

            # 将选择的分词结果添加到结果列表
            result.extend(selected_tokens)

        # 清理多余空格，形成最终的分词结果行
        cleaned_line = clean_spaces(result)
        tokenized_content.append(cleaned_line)

    return tokenized_content


if __name__ == "__main__":
    # 加载词典
    dict_file = '../dicts/dict.txt'
    forward_trie, backward_trie = load_dictionary(dict_file)

    # 加载二元语法频率数据
    bigram_file = '../data/bigram_freq_output.txt'
    bigram_freq = load_bigram_frequencies(bigram_file)

    # 指定输入文件
    input_file = '../data/cleaned_weibo_contents_separate_symbol.txt'

    # 进行分词处理，针对每个小分段选择最佳分词结果
    tokenized_result = tokenize_with_ngram_selection(
        input_file, forward_trie, backward_trie, bigram_freq)

    # 保存最终的分词结果到指定文件
    output_file = '../results/ngram_based_output.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for tokenized_line in tokenized_result:
            f.write(tokenized_line + '\n')

    print(f"\n分词结果已保存到 {output_file}")

    # 计算精确度、召回率和F1
    standard_file = '../test/metric/jieba_metric.txt'
    precision, recall, f1_score = calculate_metrics(standard_file, output_file)

    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")
