from tqdm import tqdm
from datetime import datetime

from participle.test.metric import calculate_metrics
from hmm_分词 import hmm
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """
        在字典树中插入一个词。

        参数：
        word -- 要插入的词语。
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_longest_prefix(self, sentence):
        """
        从字典树中搜索最长的前缀匹配。

        参数：
        sentence -- 待匹配的句子或词语。

        返回：
        longest_word -- 在字典树中匹配到的最长词语。
        """
        node = self.root
        longest_word = ""
        current_word = ""
        for char in sentence:
            if char in node.children:
                current_word += char
                node = node.children[char]
                if node.is_end_of_word:
                    longest_word = current_word
            else:
                break
        return longest_word


def forward_max_match(trie, sentence,use_hmm=False):
    """
    前向最大匹配算法的分词函数。

    参数：
    trie -- Trie树对象，用于匹配句子中的词语。
    sentence -- 需要进行分词的文本字符串。

    返回：
    segment_list -- 分词后的词语列表。
    """
    segment_list = []  # 存放分词后的词语列表
    sentence_raw=sentence
    while len(sentence) > 0:
        longest_word = trie.search_longest_prefix(sentence)
        if longest_word:
            segment_list.append(longest_word)
            sentence = sentence[len(longest_word):]
        elif use_hmm:
            print("hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
            segment_list = hmm(sentence_raw)
            return segment_list

        else:
            segment_list.append(sentence[0])
            sentence = sentence[1:]



    return segment_list


def backward_max_match(trie, sentence,use_hmm=False):
    """
    后向最大匹配算法的分词函数。

    参数：
    trie -- Trie树对象，用于匹配句子中的词语。
    sentence -- 需要进行分词的文本字符串。

    返回：
    segment_list -- 分词后的词语列表。
    """
    segment_list = []
    segment_raw=sentence
    while len(sentence) > 0:
        longest_word = trie.search_longest_prefix(sentence[::-1])  # 使用反转句子在反向Trie树中查找
        if longest_word:
            reversed_longest_word = longest_word[::-1]  # 匹配到的词语再反转回来
            segment_list.append(reversed_longest_word)
            sentence = sentence[:-len(reversed_longest_word)]  # 从句子末尾去除匹配到的词
        elif use_hmm:
            print("hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
            segment_list=hmm(segment_raw)
            return segment_list[::-1]  # 最终结果反转回正序
        else:
            segment_list.append(sentence[-1])
            sentence = sentence[:-1]

    return segment_list[::-1]  # 最终结果反转回正序
def load_dictionary(dict_file):
    """
    读取词典文件，将词典加载为正向和反向的Trie树。

    参数：
    dict_file -- 词典文件路径。

    返回：
    forward_trie -- 正向Trie树。
    backward_trie -- 反向Trie树。
    """
    forward_trie = Trie()
    backward_trie = Trie()

    if dict_file.endswith('.txt'):
        with open(dict_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) > 0:
                    word = parts[0]
                    forward_trie.insert(word)  # 正向插入
                    backward_trie.insert(word[::-1])  # 反向插入
    elif dict_file.endswith('.Dic'):
        with open(dict_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) > 1:
                    word = parts[1]
                    forward_trie.insert(word)  # 正向插入
                    backward_trie.insert(word[::-1])  # 反向插入
    else:
        raise ValueError(f"Unsupported dictionary format for file: {dict_file}")

    return forward_trie, backward_trie


def tokenize_with_trie(input_file, output_file, forward_trie, backward_trie, method="forward"):
    """
    将文本文件进行分词处理，并保存结果。

    参数：
    input_file -- 待分词的输入文本文件路径。
    output_file -- 分词结果输出文件路径。
    forward_trie -- 正向Trie树对象。
    backward_trie -- 反向Trie树对象。
    method -- 分词方法，"forward" 或 "backward"。

    返回：
    tokenized_content -- 分词后的二维列表。
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tokenized_content = []

    for line in tqdm(lines, desc="Processing lines"):
        sentence = line.strip()  # 去除前后的空白符和换行符
        if not sentence:  # 如果是空行则跳过
            continue

        # 根据指定的分词方法，调用相应的分词函数
        if method == "forward":
            result = forward_max_match(forward_trie, sentence)  # 使用正向Trie树进行前向最大匹配
        elif method == "backward":
            result = backward_max_match(backward_trie, sentence)  # 使用反向Trie树进行后向最大匹配
        else:
            raise ValueError("method 参数必须是 'forward' 或 'backward'")

        tokenized_content.append(result)

    with open(output_file, 'w', encoding='utf-8') as f:
        for tokenized_line in tokenized_content:
            f.write(' '.join(tokenized_line) + '\n')

    return tokenized_content


if __name__ == "__main__":
    dict_path = '../dicts/'
    dict_name = 'dict.txt'  # 词典文件路径

    dict_file = dict_path + dict_name

    # 选择分词方法：'forward' 表示前向最大匹配，'backward' 表示后向最大匹配
    method = "forward"

    # 加载正向和反向的Trie树
    forward_trie, backward_trie = load_dictionary(dict_file)

    # 指定输入的txt文件路径和输出的txt文件路径
    input_file = '../data/cleaned_weibo_contents_metric.txt'  # 已清洗的微博内容

    output_file = '../results/' + dict_name.split('.')[0] + "_" + method + '_output.txt'

    # 记录处理时间
    start_time = datetime.now()

    # 进行分词处理并获取结果列表
    tokenized_result = tokenize_with_trie(input_file, output_file, forward_trie, backward_trie, method)

    # 输出处理时间
    time_taken = datetime.now() - start_time
    print(f"处理时间：{time_taken}")

    print(f"分词结果已保存到 {output_file}")

    # 指定标准分词文件和模型分词结果文件
    standard_file = '../test/metric/jieba_metric.txt'  # 标准分词结果文件路径

    # 计算精确度、召回率和F1
    precision, recall, f1_score = calculate_metrics(standard_file, output_file)

    # 输出结果
    print(f"精确度（Precision）：{precision:.4f}")
    print(f"召回率（Recall）：{recall:.4f}")
    print(f"F1 分数（F1-Score）：{f1_score:.4f}")
