import re

def keep_chinese_and_replace_non_chinese(input_file, output_file):
    # 定义一个正则表达式，匹配所有非中文字符
    non_chinese_pattern = re.compile(r'[^\u4e00-\u9fa5]+')

    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()

    # 将所有非中文字符替换为换行符
    modified_content = re.sub(non_chinese_pattern, '\n', content)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(modified_content)

    print(f"处理完毕，结果已保存至 {output_file}")


# 示例使用
input_file = 'cleaned_weibo_contents_metric.txt'  # 输入文件名
output_file = 'data.txt'  # 输出文件名
keep_chinese_and_replace_non_chinese(input_file, output_file)
