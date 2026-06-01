import json
import re


# 定义清洗和处理内容的函数
def clean_content(content):
    # 如果内容是转发的（以"//"开头），则跳过
    if content.startswith("//"):
        return None

    # 删除##包裹的话题内容
    cleaned_content = re.sub(r'#.*?#', '', content)

    # 移除不需要的短语，如“展开c”和“O网页链接”以及"↓↓↓"
    cleaned_content = re.sub(r'展开c|O网页链接|↓↓↓|【|】', '', cleaned_content)

    # 移除以"L"开头的类似短语，如“L科普一下的微博视频”
    cleaned_content = re.sub(r'L[\u4e00-\u9fff]+的微博视频', '', cleaned_content)

    # 将多余的空格合并为0个
    cleaned_content = re.sub(r'\s+', '', cleaned_content)

    # 删除开头和结尾多余的空格
    cleaned_content = cleaned_content.strip()

    # 去除句首的无效符号
    cleaned_content = re.sub(r'^[\s.,;:，。；：【】！▲]+', '', cleaned_content)

    return cleaned_content


# 比较两条内容的主要部分是否相同
def is_similar_content(content1, content2):
    # 去掉来源等差异化信息，仅保留主要部分进行比较
    main_part1 = re.sub(r'（.*?）', '', content1)
    main_part2 = re.sub(r'（.*?）', '', content2)

    # 移除所有空格，进行简单字符串比较
    main_part1 = re.sub(r'\s+', '', main_part1)
    main_part2 = re.sub(r'\s+', '', main_part2)

    return main_part1 == main_part2


# 定义处理整个微博数据并保存结果的函数
def process_weibo_data(input_file, output_file):
    # 读取JSON文件中的微博数据
    with open(input_file, 'r', encoding='utf-8') as f:
        weibo_data = json.load(f)

    all_segments = []  # 用于存储所有去重后的片段
    seen_segments = set()  # 用于跟踪已经处理过的片段，保证去重

    for item in weibo_data:
        # 如果转发数是"转发"，则跳过这条数据
        if item.get('转发数') == '转发':
            continue

        # 对微博内容进行清洗
        cleaned_content = clean_content(item['内容'])

        # 如果清洗后的内容为空，则跳过
        if not cleaned_content:
            continue

        # 检查是否有与当前内容相似的片段已经存在，若有则跳过
        is_duplicate = any(is_similar_content(cleaned_content, segment) for segment in seen_segments)

        if not is_duplicate:
            all_segments.append(cleaned_content)
            seen_segments.add(cleaned_content)

    # 去除可能存在的连续空行，只保留一个换行符
    result_content = '\n'.join([segment for segment in all_segments if segment.strip()])

    # 将清洗后的内容写入txt文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result_content + '\n')

    print(f"清洗后的内容已保存到 {output_file}.")


# 示例调用
if __name__ == "__main__":
    # 指定输入的JSON文件路径和输出的txt文件路径
    input_file = '../../data/weibo_contents.json'  # 替换为你的输入文件路径
    output_file = '../../data/cleaned_weibo_contents_metric.txt'

    # 处理并保存清洗后的内容
    process_weibo_data(input_file, output_file)

    print(f"清洗后的内容已保存到 {output_file}.")
