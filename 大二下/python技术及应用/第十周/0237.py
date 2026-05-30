import re
from collections import Counter

def Read01(filename):
    with open(filename, 'r', encoding='gbk') as file:  # 尝试使用 gbk 编码
        text = file.read().lower()
    # 只保留字母
    letters = re.findall(r'[a-z]', text)
    letter_counts = Counter(letters)
    top_5_letters = letter_counts.most_common(5)

    with open('hamlet_字母频度.txt', 'w', encoding='utf-8') as file:
        for letter, freq in top_5_letters:
            file.write(f"{letter}: {freq}\n")
            print(f"{letter}: {freq}")

def Read02(filename):
    with open(filename, 'r', encoding='gbk') as file:  # 尝试使用 gbk 编码
        text = file.read().lower()
    # 只保留单词，移除空字符
    words = re.findall(r'\b[a-z]+\b', text)
    word_counts = Counter(words)
    top_10_words = word_counts.most_common(10)

    with open('hamlet_单词频度.txt', 'w', encoding='utf-8') as file:
        for word, freq in top_10_words:
            file.write(f"{word}: {freq}\n")
            print(f"{word}: {freq}")

# 调用函数以处理文本文件
filename = 'hamlet.txt'
Read01(filename)
Read02(filename)

