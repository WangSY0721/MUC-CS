import re
from collections import Counter
import os


def process_file(input_filename, bigram_counter):
    with open(input_filename, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除非中文字符和标点符号（作为分隔符）
            segments = re.split(r'[^\u4e00-\u9fff\s]+', line)
            for segment in segments:
                segment = segment.strip()
                if segment:
                    # 将段落分割成词语
                    words = segment.split()
                    # 生成二元组
                    bigrams = zip(words, words[1:])
                    bigram_counter.update(bigrams)


def main():
    input_files = [
        '../data/courpus/as_training.utf8',
        '../data/courpus/msr_training.txt',
        '../data/courpus/nlpcc2016-word-seg-train.dat',
        '../data/courpus/pku_training.txt'
    ]  # 输入文件列表
    output_filename = 'bigram_freq_output.txt'  # 输出文件，记录二元组频率

    # 初始化一个计数器，用于统计所有文件中的二元组
    bigram_counter = Counter()

    # 遍历每个文件并处理，更新二元组计数器
    for input_file in input_files:
        if os.path.exists(input_file):  # 检查文件是否存在
            process_file(input_file, bigram_counter)
        else:
            print(f"文件未找到: {input_file}")

    # 将二元组及其频率写入输出文件
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for (word1, word2), freq in bigram_counter.items():
            outfile.write(f"{word1} {word2} {freq}\n")


if __name__ == "__main__":
    main()
