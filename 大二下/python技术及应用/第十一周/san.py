import jieba
import logging

# 设置jieba的日志级别
jieba.setLogLevel(logging.WARNING)

from collections import Counter


# 合并不同名称的角色
def merge_names(counter):
    merge_dict = {
        "曹操": ["曹操", "丞相"],
        "诸葛亮": ["孔明", "孔明曰", "诸葛亮"],
        "关羽": ["关羽", "关公"],
        "刘备": ["刘备", "玄德", "玄德曰", "刘皇叔", "刘使君"],
        "张飞": ["张飞"]
    }

    merged_counter = Counter()

    for name, variants in merge_dict.items():
        total_count = sum(counter[variant] for variant in variants)
        merged_counter[name] = total_count

    return merged_counter


# 读取文本文件
with open('三国演义.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# 使用JIEBA分词
words = jieba.lcut(text)

# 排除非人名的词语
exclude_words = {"却说", "将军", "二人", "不可", "荆州", "不能", "如此", "商议", "如何", "主公", "军士"}
filtered_words = [word for word in words if word not in exclude_words]

# 统计词频
word_counts = Counter(filtered_words)

# 合并不同名称的角色
merged_counts = merge_names(word_counts)

# 找出出现频率最高的前5位人物
top_5_characters = merged_counts.most_common(5)

# 打印结果
for character, count in top_5_characters:
    print(f"{character}: {count}")
