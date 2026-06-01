from tqdm import tqdm

from participle.test.metric import calculate_metrics


def forward_max_match(ch_dict, sentence):
    """
    正向最大匹配算法的分词函数。

    参数：
    ch_dict -- 词典列表，用于匹配句子中的词语。
    sentence -- 需要进行分词的文本字符串。

    返回：
    segment_list -- 分词后的词语列表。
    """
    segment_list = []  # 存放分词后的词语列表
    # sentence='今天下午去看大学生活动中心'
    while len(sentence) >= 1:
        max_match_len = 5  # 最大匹配单词的长度，可根据词典中最长词语的长度调整

        # 确保最大匹配长度不超过剩余句子长度
        if len(sentence) < max_match_len:
            max_match_len = len(sentence)

        # 从最大匹配长度开始逐渐减少匹配长度
        while max_match_len > 1:
            current_word = sentence[0:max_match_len]
            if current_word in ch_dict:
                segment_list.append(current_word)
                sentence = sentence[max_match_len:]
                break
            max_match_len -= 1

        # 如果没有匹配的词语，截取单个字符
        if max_match_len == 1:
            segment_list.append(sentence[0:1])
            sentence = sentence[1:]
    # print(segment_list)
    return segment_list


def backward_max_match(ch_dict, sentence):
    """
    后向最大匹配算法的分词函数。

    参数：
    ch_dict -- 词典列表，用于匹配句子中的词语。
    sentence -- 需要进行分词的文本字符串。

    返回：
    segment_list -- 分词后的词语列表（顺序从左到右）。
    """
    segment_list = []  # 存放分词后的词语列表
    # sentence='今天下午去看大学生活动中心'
    while len(sentence) >= 1:
        max_match_len = 5  # 最大匹配单词的长度，可根据词典中最长词语的长度调整

        # 确保最大匹配长度不超过剩余句子长度
        if len(sentence) < max_match_len:
            max_match_len = len(sentence)

        # 从最大匹配长度开始逐渐减少匹配长度
        while max_match_len > 1:
            current_word = sentence[-max_match_len:]
            # print("当前取得：")
            # print(current_word)
            if current_word in ch_dict:
                # print("匹配ok的：")
                segment_list.append(current_word)
                sentence = sentence[:-max_match_len]
                break
            max_match_len -= 1

        # 如果没有匹配的词语，截取单个字符
        if max_match_len == 1:
            segment_list.append(sentence[-1:])
            sentence = sentence[:-1]

    # 分词结果是逆序的，需要反转
    segment_list.reverse()
    # print(segment_list)
    return segment_list


# 读取词典文件，将词典加载为列表
def load_dictionary(dict_file):
    dictionary = []

    # 判断文件类型，根据不同类型选择不同的解析逻辑
    if dict_file.endswith('.txt'):
        # 处理 '../dicts/dict.txt' 格式的词典文件
        with open(dict_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()  # 将每一行按照空格分割
                if len(parts) > 0:
                    word = parts[0]  # 获取词语部分
                    dictionary.append(word)  # 将词语添加到词典中
    elif dict_file.endswith('.Dic'):
        # 处理 '../dicts/wordlist.Dic' 格式的词典文件
        with open(dict_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()  # 将每一行按照空格分割
                if len(parts) > 1:
                    word = parts[1]  # 获取词语部分（忽略序号）
                    dictionary.append(word)  # 将词语添加到词典中
    else:
        raise ValueError(f"Unsupported dictionary format for file: {dict_file}")

    return dictionary


# 定义一个函数，将文本文件进行分词处理，并保存为二维列表
def tokenize_with_custom_match(input_file, output_file, dictionary, method="backward"):
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

        # 根据指定的分词方法，调用相应的分词函数
        if method == "forward":
            result = forward_max_match(dictionary, sentence)  # 前向最大匹配分词
        elif method == "backward":
            result = backward_max_match(dictionary, sentence)  # 后向最大匹配分词
        else:
            raise ValueError("method 参数必须是 'forward' 或 'backward'")

        # 将分词结果（列表形式）添加到二维列表中
        tokenized_content.append(result)

    # 将分词结果保存为新的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for tokenized_line in tokenized_content:
            f.write(' '.join(tokenized_line) + '\n')  # 将每行分词结果写入文件，词之间用空格分隔

    # 返回分词后的二维列表
    return tokenized_content


if __name__ == "__main__":
    # 从NLP/dicts/dict.txt读取词典
    dict_path = '../dicts/'
    # dict_name = 'dict.txt'  # 词典文件路径
    dict_name = 'wordlist.Dic'

    dict_file = dict_path + dict_name

    ch_dict = load_dictionary(dict_file)  # 加载词典
    # 指定输入的txt文件路径和输出的txt文件路径
    input_file = '../data/cleaned_weibo_contents_metric.txt'  # 已清洗的微博内容

    # 选择分词方法：'forward' 表示前向最大匹配，'backward' 表示后向最大匹配
    method = "forward"

    output_file = '../results/' + dict_name.split('.')[0] + "_" + method + '_output.txt'

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
