import re
import math
from tqdm import tqdm
from max_match_with_tree import forward_max_match, backward_max_match, load_dictionary
from participle.test.metric import calculate_metrics


def contains_chinese(text):
    """
    检查给定文本是否包含汉字。

    参数：
    text -- 要检查的字符串。

    返回：
    如果字符串中包含汉字，返回 True；否则返回 False。
    """
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def load_unigram_counts(filename):
    """
    加载词典并获取词频信息。

    参数：
    filename -- 词典文件路径。

    返回：
    unigram_counts -- 一元词频字典。
    total_unigram_count -- 一元词频总数。
    """
    unigram_counts = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 3:
                continue
            word = parts[0]
            count = int(parts[1])
            unigram_counts[word] = count
    total_unigram_count = sum(unigram_counts.values())
    return unigram_counts, total_unigram_count


def compute_sentence_probability(segmentation, unigram_counts, total_unigram_count, vocabulary_size):
    """
    计算给定分词结果的句子概率（对数形式）。

    参数：
    segmentation -- 分词后的词语列表。
    unigram_counts -- 一元词频字典。
    total_unigram_count -- 一元词频总数。
    vocabulary_size -- 词汇表大小。

    返回：
    prob -- 句子概率的对数值。
    """
    prob = 0.0

    for word in segmentation:
        # 使用一元词频，添加拉普拉斯平滑
        count = unigram_counts.get(word, 0) + 1  # 加1平滑
        prob += math.log(count / (total_unigram_count + vocabulary_size))

    return prob


def process_segment(forward_trie, backward_trie, segment, unigram_counts, total_unigram_count, vocabulary_size):
    """
    对给定的段落（分词单元）进行分词处理，并使用N-gram模型选择更合理的分词结果。

    参数：
    forward_trie -- 正向Trie树。
    backward_trie -- 反向Trie树。
    segment -- 需要进行分词的文本字符串。
    unigram_counts -- 一元词频字典。
    total_unigram_count -- 一元词频总数。
    vocabulary_size -- 词汇表大小。

    返回：
    最优的分词结果列表。
    """
    if contains_chinese(segment):
        # 获取前向和后向最大匹配的分词结果
        forward_seg = forward_max_match(forward_trie, segment)
        backward_seg = backward_max_match(backward_trie, segment)

        # 计算各自的句子概率
        forward_prob = compute_sentence_probability(forward_seg, unigram_counts, total_unigram_count, vocabulary_size)
        backward_prob = compute_sentence_probability(backward_seg, unigram_counts, total_unigram_count, vocabulary_size)

        # 选择概率更高的分词结果
        if forward_prob > backward_prob:
            return forward_seg
        else:
            return backward_seg
    else:
        return [segment]


def clean_spaces(tokens):
    """
    清理多余的空格，确保词与词之间只有一个空格。

    参数：
    tokens -- 分词后的词语列表。

    返回：
    一个干净的字符串，其中词与词之间只有一个空格。
    """
    return ' '.join([token for token in tokens if token.strip()])  # 去掉多余空白


def tokenize_with_custom_match(input_file, output_file, forward_trie, backward_trie, unigram_counts, total_unigram_count, vocabulary_size):
    """
    将文本文件进行分词处理，并保存为二维列表。

    参数：
    input_file -- 输入文件路径。
    output_file -- 输出文件路径。
    forward_trie -- 正向Trie树。
    backward_trie -- 反向Trie树。
    unigram_counts -- 一元词频字典。
    total_unigram_count -- 一元词频总数。
    vocabulary_size -- 词汇表大小。
    """
    # 读取已清洗的文本文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 存储所有分词结果的二维列表
    tokenized_content = []

    # 使用 tqdm 显示进度条，遍历每一行内容并进行分词
    for line in tqdm(lines, desc="Processing lines"):
        sentence = line.strip()  # 去除前后的空白符和换行符
        if not sentence:  # 如果是空行则跳过
            continue

        # 使用正则表达式找到空格包裹的内容或其他部分
        segments = re.split(r'(\s+)', sentence)  # 保留分隔符，避免丢失空格

        result = []
        for segment in segments:
            # 如果内容是空格，直接跳过，不保留空格
            if segment.isspace():
                continue

            # 对非空格部分进行分词处理
            processed_segment = process_segment(forward_trie, backward_trie, segment, unigram_counts, total_unigram_count, vocabulary_size)
            result.extend(processed_segment)

        # 清理多余空格后，将分词结果添加到二维列表中
        cleaned_line = clean_spaces(result)
        tokenized_content.append(cleaned_line)

    # 将分词结果保存为新的文件，每个词语间以一个空格分隔
    with open(output_file, 'w', encoding='utf-8') as f:
        for tokenized_line in tokenized_content:
            f.write(tokenized_line + '\n')  # 每行词语之间一个空格

    # 返回分词后的二维列表
    return tokenized_content


if __name__ == "__main__":
    # 从 ../dicts/dict.txt 读取词典
    dict_file = '../dicts/dict.txt'  # 词典文件路径
    forward_trie, backward_trie = load_dictionary(dict_file)  # 加载Trie树

    # 加载一元词频
    unigram_counts, total_unigram_count = load_unigram_counts(dict_file)

    # 词汇表大小
    vocabulary_size = len(unigram_counts)

    # 指定输入的 txt 文件路径和输出的 txt 文件路径
    input_file = '../data/cleaned_weibo_contents_separate_symbol.txt'  # 已清洗的微博内容
    output_file = '../results/unigram_based_output.txt'  # 输出文件路径

    # 进行分词处理并获取结果列表
    tokenized_result = tokenize_with_custom_match(
        input_file,
        output_file,
        forward_trie,
        backward_trie,
        unigram_counts,
        total_unigram_count,
        vocabulary_size
    )

    print(f"分词结果已保存到 {output_file}")

    # 指定标准分词文件和模型分词结果文件
    standard_file = '../test/metric/jieba_metric.txt'  # 标准分词结果文件路径

    # 计算精确度、召回率和 F1
    precision, recall, f1_score = calculate_metrics(standard_file, output_file)
    # 输出结果
    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")
