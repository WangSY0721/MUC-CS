import pickle
from tqdm import tqdm
import numpy as np
import os
import re


def make_label(text_str):
    text_len = len(text_str)
    if text_len == 1:
        return "S"
    return "B" + "M" * (text_len - 2) + "E"


def text_to_state(file="../data/1998人民日报（分词）.txt"):
    all_data = open(file, "r", encoding="gbk").read().split("\n")

    with open("../data/all_train_state.txt", "w", encoding="utf-8") as f:
        for d_index, data in tqdm(enumerate(all_data)):
            if data:
                state_ = ""
                for w in data.split(" "):
                    if w:
                        state_ = state_ + make_label(w) + " "
                if d_index != len(all_data) - 1:
                    state_ = state_.strip() + "\n"
                    # d_index是当前处理的行号，len(all_data) - 1是总数据的最后一行索引。
                    # 如果不是最后一条记录，就需要在状态序列末尾加上换行符。
                f.write(state_)


class HMM:
    def __init__(self, file_text="../data/1998人民日报（分词）.txt", file_state="../data/all_train_state.txt"):
        self.all_states = open(file_state, "r", encoding="utf-8").read().split("\n")
        # try:
        #     # 尝试使用 GBK 编码读取 ANSI 编码的文件
        #     self.all_texts = open(file_text, "r", encoding="gbk").read().split("\n")
        # except UnicodeDecodeError:
        #     # 如果 GBK 失败，使用 ISO-8859-1 编码
        #     self.all_texts = open(file_text, "r", encoding="iso-8859-1").read().split("\n")
        self.all_texts = open(file_text, "r", encoding="gbk").read().split("\n")
        self.states_to_index = {"B": 0, "M": 1, "S": 2, "E": 3}
        self.index_to_states = ["B", "M", "S", "E"]
        self.len_states = len(self.states_to_index)

        self.init_matrix = np.zeros((self.len_states))
        self.transfer_matrix = np.zeros((self.len_states, self.len_states))
        self.emit_matrix = {}

    def cal_init_matrix(self, state):
        # print("state[0]:", state[0])
        # print("states_to_index:", self.states_to_index)
        # print("states_to_index[state[0]]:", self.states_to_index[state[0]])
        print("state:", state)
        self.init_matrix[self.states_to_index[state[0]]] += 1

    def cal_transfer_matrix(self, states):
        sta_join = "".join(states)
        sta1 = sta_join[:-1]
        sta2 = sta_join[1:]
        for s1, s2 in zip(sta1, sta2):
            self.transfer_matrix[self.states_to_index[s1], self.states_to_index[s2]] += 1

    def cal_emit_matrix(self, words, states):
        for word, state in zip("".join(words), "".join(states)):
            if word not in self.emit_matrix:
                self.emit_matrix[word] = {"total": 0}
            self.emit_matrix[word][state] = self.emit_matrix[word].get(state, 0) + 1
            self.emit_matrix[word]["total"] += 1

    def normalize(self):
        self.init_matrix = self.init_matrix / np.sum(self.init_matrix)
        self.transfer_matrix = self.transfer_matrix / np.sum(self.transfer_matrix, axis=1, keepdims=True)
        self.emit_matrix = {word: {state: time / states["total"] for state, time in states.items() if state != "total"}
                            for word, states in self.emit_matrix.items()}

    # 训练计算三大概率矩阵
    def train(self):
        if os.path.exists("../data/three_matrix.pkl"):
            self.init_matrix, self.transfer_matrix, self.emit_matrix = pickle.load(open(
                "../data/three_matrix.pkl", "rb"))
            return
        for words, states in tqdm(zip(self.all_texts, self.all_states)):
            if not words.strip() or not states.strip():  # 检查是否为空行
                continue
            words = words.split(" ")
            print("words:", words)
            states = states.split(" ")
            print("states:", states)
            self.cal_init_matrix(states[0])
            # states[0]是一个句子的第一个词
            self.cal_transfer_matrix(states)
            self.cal_emit_matrix(words, states)
        self.normalize()
        pickle.dump([self.init_matrix, self.transfer_matrix, self.emit_matrix], open("../data/three_matrix.pkl", "wb"))


# 测试阶段维特比算法求出概率最大路径
def viterbi(text, hmm):
    """
    使用维特比算法实现基于隐马尔可夫模型的分词。

    参数：
    - text: 待分词的文本字符串。
    - hmm: 包含 HMM 参数的对象，包括初始矩阵、发射矩阵和转移矩阵。

    返回：
    - segment_list: 分词结果的列表。
    """
    # 初始化所有可能的路径
    paths = [s for s in hmm.index_to_states]
    # 初始化路径对应的分数（概率）
    scores = [p for p in hmm.init_matrix]

    # 遍历每个字符及其索引
    for w_index, w in enumerate(text):
        # print("w:", w)  # 打印当前字符
        # print("w_index:", w_index)  # 打印当前字符的索引

        # 遍历所有路径
        for p_index, path in enumerate(paths):
            # 如果当前字符不在发射矩阵中，进行平滑处理（初始化其发射概率为 1）
            if w not in hmm.emit_matrix:
                hmm.emit_matrix[w] = {"B": 1, "M": 1, "S": 1, "E": 1}
            for state in hmm.index_to_states:
                if state not in hmm.emit_matrix[w]:
                    hmm.emit_matrix[w][state] = 1e-8  # 如果某个状态缺失，初始化为  1e-8
            # 更新路径的分数，将当前路径的分数乘以发射概率
            scores[p_index] *= hmm.emit_matrix[w][path[-1]]

        # 如果已经是最后一个字符，跳出循环
        if w_index == len(text) - 1:
            break

        # 检查下一个字符是否在发射矩阵中，若没有则进行平滑处理
        if text[w_index + 1] not in hmm.emit_matrix:
            hmm.emit_matrix[text[w_index + 1]] = {"B": 1, "M": 1, "S": 1, "E": 1}
        for state in hmm.index_to_states:
            if state not in hmm.emit_matrix[text[w_index + 1]]:
                hmm.emit_matrix[text[w_index + 1]][state] = 1e-8  # 如果某个状态缺失，初始化为  1e-8
        # 创建一个副本存储当前路径
        new_s = [lp for lp in paths]

        # 遍历所有可能的状态
        for state in hmm.index_to_states:
            # 存储转移和发射概率的中间结果
            tp_s = []

            # 计算从路径末状态转移到当前状态的概率，以及发射概率
            for lp in new_s:
                tp_s.append(
                    hmm.transfer_matrix[
                        hmm.states_to_index[lp[-1]], hmm.states_to_index[state]
                    ] * hmm.emit_matrix[text[w_index + 1]][state]
                )

            # 找出概率最大的路径状态索引，并映射回状态名称
            max_s = hmm.index_to_states[np.argmax(tp_s)]
            # 获取该路径的最大概率值
            max_p = np.max(tp_s)

            # 更新路径，在当前最佳路径末尾加入新状态
            paths[hmm.states_to_index[max_s]] += state
            # 更新路径分数，乘以转移和发射的最大概率值
            scores[hmm.states_to_index[max_s]] *= max_p

    # 找出分数最高的路径作为最终结果
    result_p = paths[np.argmax(scores)]

    # 构建分词结果字符串
    cut_result = ""
    for t, p in zip(text, result_p):
        cut_result += t
        # 遇到状态为 S（单字）或 E（结束字）时，添加空格
        if p == "S" or p == "E":
            cut_result += " "

    # 按空格将结果分割为列表
    segment_list = cut_result.split(' ')
    print(segment_list)  # 打印分词结果
    return segment_list  # 返回分词结果


def hmm(text):
    # 每次换新训练语料，就需要重新调用这个函数，生成all_train_state.txt
    # text_to_state()
    hmm = HMM()
    hmm.train()
    segment_list = viterbi(text, hmm)
    return segment_list


def clean_spaces(tokens):
    """
    清理多余的空格，确保词与词之间只有一个空格。

    参数：
    tokens -- 分词后的词语列表。

    返回：
    一个干净的字符串，其中词与词之间只有一个空格。
    """
    return ' '.join([token for token in tokens if token.strip()])  # 去掉多余空白


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


def tokenize_with_custom_match(input_file, output_file):
    """
    将文本文件进行分词处理，并保存为二维列表。
    参数：
    input_file -- 输入文件路径。
    output_file -- 输出文件路径。
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
            processed_segment = hmm(segment)
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


if __name__ == "__main__":
    # 从NLP/dicts/dict.txt读取词典

    # 指定输入的txt文件路径和输出的txt文件路径
    input_file = '../data/data.txt'  # 已清洗的微博内容

    output_file = '../results/hmm_output.txt'

    # 进行分词处理并获取结果列表
    tokenized_result = tokenize_with_custom_match(input_file, output_file)

    print(f"分词结果已保存到 {output_file}")

    # 指定标准分词文件和模型分词结果文件
    standard_file = '../test/metric/jieba_metric.txt'  # 标准分词结果文件路径
    # 计算精确度、召回率和F1
    precision, recall, f1_score = calculate_metrics(standard_file, output_file)
    # 输出结果
    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")
