import re
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


def process_segment(ch_dict, segment, method):
    """
    对给定的段落（分词单元）进行分词处理。

    参数：
    ch_dict -- 词典列表，用于匹配句子中的词语。
    segment -- 需要进行分词的文本字符串。
    method -- 分词方法 ('forward' 或 'backward')。

    返回：
    分词后的词语列表。
    """
    # 如果含有汉字，则进行最大匹配分词
    if contains_chinese(segment):
        if method == "forward":
            return forward_max_match(ch_dict, segment,use_hmm=True)
        elif method == "backward":
            return backward_max_match(ch_dict, segment,use_hmm=True)
    # 如果不含汉字，则直接返回该段作为一个单元
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


def tokenize_with_custom_match(input_file, output_file, dictionary, method="forward"):
    """
    将文本文件进行分词处理，并保存为二维列表。

    参数：
    input_file -- 输入文件路径。
    output_file -- 输出文件路径。
    dictionary -- 词典。
    method -- 分词方法，'forward' 表示前向最大匹配，'backward' 表示后向最大匹配。
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
            processed_segment = process_segment(dictionary, segment, method)
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
    # 从NLP/dicts/dict.txt读取词典
    dict_file = '../dicts/dict.txt'  # 词典文件路径
    forward_trie, backward_trie = load_dictionary(dict_file)  # 加载正向和反向的词典

    # 选择分词方法：'forward' 表示前向最大匹配，'backward' 表示后向最大匹配
    method = "forward"

    # 根据选择的分词方法，传递正确的 Trie
    if method == "forward":
        ch_dict = forward_trie
    elif method == "backward":
        ch_dict = backward_trie
    else:
        raise ValueError("method 参数必须是 'forward' 或 'backward'")

    # 指定输入的txt文件路径和输出的txt文件路径
    input_file = '../data/cleaned_weibo_contents_separate_symbol.txt'  # 已清洗的微博内容

    output_file = '../results/' + method + '_pre_cleaned_output.txt'

    # 进行分词处理并获取结果列表
    tokenized_result = tokenize_with_custom_match(input_file, output_file, ch_dict, method)

    print(f"分词结果已保存到 {output_file}")

    # 指定标准分词文件和模型分词结果文件
    standard_file = '../test/metric/jieba_metric.txt'  # 标准分词结果文件路径
    # 计算精确度、召回率和F1
    precision, recall, f1_score = calculate_metrics(standard_file, output_file)
    # 输出结果
    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")

