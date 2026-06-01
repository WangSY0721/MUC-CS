import jieba
from collections import defaultdict


def segment_file(input_file, output_file):
    """
    使用 Jieba 对输入文件进行分词，并将分词结果写入输出文件。

    参数：
    input_file -- 输入文本文件路径。
    output_file -- 分词结果输出文件路径。
    """
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            stripped_line = line.strip()
            if stripped_line:  # 确保非空行
                print(f"当前行内容: {stripped_line}")  # 调试信息，打印每行内容
                words = jieba.lcut(stripped_line)
                print(f"分词结果: {words}")  # 调试信息，打印分词结果
                outfile.write(' '.join(words) + '\n')

    print(f"分词结果已写入 {output_file}")


# 示例调用
if __name__ == "__main__":
    # 输入文件路径
    input_file = r"D:\PycharmProjects\NLP\participle\data\cleaned_weibo_contents_metric.txt"  # 替换为绝对路径
    segmented_output_file = r"D:\PycharmProjects\NLP\participle\test\metric\jieba_metric.txt"  # 分词结果输出文件

    # 1. 分词并写入分词结果文件
    segment_file(input_file, segmented_output_file)
