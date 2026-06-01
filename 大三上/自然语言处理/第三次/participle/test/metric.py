# 计算精确度、召回率和F1的函数

def calculate_metrics(standard_file, result_file):
    with open(standard_file, 'r', encoding='utf-8') as f:
        standard_lines = f.readlines()  # 读取标准分词文件的每一行

    with open(result_file, 'r', encoding='utf-8') as f:
        result_lines = f.readlines()  # 读取模型分词文件的每一行

    # 定义变量用于存储匹配结果
    true_positive = 0  # 模型分词与标准分词一致的词数
    false_positive = 0  # 模型分出的词语，但不在标准分词中的词数
    false_negative = 0  # 标准分词中的词语，但没有被模型分出来的词数

    # 遍历每一行的分词结果
    for standard_line, result_line in zip(standard_lines, result_lines):
        # 将标准分词和模型分词结果转换为位置编码列表
        standard_tokens = tokenize_with_positions(standard_line.strip())  # 标准分词结果位置列表
        result_tokens = tokenize_with_positions(result_line.strip())  # 模型分词结果位置列表

        # 打印标准结果和模型结果的位置编码以进行对比
        # print(f"标准分词位置编码：{standard_tokens}")
        # print(f"模型分词位置编码：{result_tokens}")

        # 计算 True Positive (TP)：模型分对的词
        true_positive += len([token for token in standard_tokens if token in result_tokens])

        # 计算 False Positive (FP)：模型分词中多分的词
        false_positive += len([token for token in result_tokens if token not in standard_tokens])

        # 计算 False Negative (FN)：标准分词中有但模型未分出的词
        false_negative += len([token for token in standard_tokens if token not in result_tokens])

    # 计算精确度、召回率和F1分数
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score


def tokenize_with_positions(line):
    """
    将一行文本的每个字符转换为位置编码，并用空格和换行符将位置编码分割成一个二维列表
    例如：
    "我们 都有 光明的 前途" -> [[0, 1], [2, 3], [4, 5, 6], [7, 8]]
    """
    position_list = []  # 用于存储每个词的位置编码
    current_token = []  # 当前词的位置编码

    current_position = 0  # 当前字符位置，从0开始
    for char in line:
        if char != ' ' and char != '\n':
            current_token.append(current_position)  # 为每个非空格和换行符的字符赋予位置编码
            current_position += 1  # 只有非空格字符位置才增加
        else:
            if current_token:
                position_list.append(current_token)  # 将完整的词加入位置列表
                current_token = []  # 重置当前词
    # 最后一个词处理
    if current_token:
        position_list.append(current_token)

    return position_list


# 示例调用
if __name__ == "__main__":
    # 指定标准分词文件和模型分词结果文件
    standard_file = 'metric/jieba_metric.txt'  # 标准分词结果文件路径

    # 模型分词结果文件路径

    # result_file = '../results/forward_output.txt'
    # result_file = '../results/backward_pre_cleaned_output.txt'
    # result_file = '../results/forward_pre_cleaned_output.txt'
    # result_file = '../results/ngram_based_output.txt'
    # result_file = '../results/LLM分词结果.txt'
    result_file = '../results/hmm_output.txt'

    # 计算精确度、召回率和F1
    precision, recall, f1_score = calculate_metrics(standard_file, result_file)

    # 输出结果
    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")
