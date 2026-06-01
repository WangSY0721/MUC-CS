import os
import time
import pandas as pd
import torch
from transformers import AutoTokenizer, TextStreamer
from ipex_llm.transformers import AutoModelForCausalLM
import re  # 导入正则表达式库


# 加载模型路径
load_path = "qwen2chat_int4"

# 加载4位量化的Qwen模型
model = AutoModelForCausalLM.load_low_bit(load_path, trust_remote_code=True)

# 加载对应的tokenizer，用于分词和编码
tokenizer = AutoTokenizer.from_pretrained(load_path, trust_remote_code=True)

# 创建文本流式输出器（可选，如果需要实时显示生成内容）
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

# 读取txt文件，每一行作为一个文本
file_path = r"D:\王世屹\大学\计算机\自然语言处理\第一次\qwenLLM\1.txt"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 将读取的文本数据存入DataFrame
df = pd.DataFrame(lines, columns=['内容'])
result = ''
# 使用推理模式关闭梯度计算，加快推理速度
with torch.inference_mode():
    # 记录推理开始时间
    st = time.time()
    # 遍历txt文件中每一行内容
    for index, text in enumerate(df['内容']):
        print(f"Processing row {index}...")

        # 构建输入的消息，用户角色为文本分析小助手，提示生成分词
        messages = [
            {"role": "user",
             "content": "对这段文本进行分词,并且一定只输出分词结果，分词词语之间用空格分隔：\n" + text},
        ]

        # 将消息应用聊天模板，并添加生成提示
        text_input = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        # 对输入文本进行编码，转换为模型的输入格式
        model_inputs = tokenizer([text_input], return_tensors="pt")

        # 使用模型生成结果，限制生成的最大token数目为1000
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=2048,  # 限制生成的token数目
        )

        # 将生成的token解码为文本
        generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

        # 指定提取的标记（模型生成的文本以'assistant\n'为标记）
        start_marker = "assistant\n"

        # 查找最后一次标记的位置
        start_index = generated_text.rfind(start_marker)

        # 如果找到标记，提取标记之后的文本，作为模型的最终输出
        if start_index != -1:
            extracted_text = generated_text[start_index + len(start_marker):].strip()
            # 清理生成结果中的多余字符，比如重复的“么”
            extracted_text = extracted_text.replace("么么", "么")

            # 通过正则表达式提取标点符号，并确保其作为独立的分词结果
            # 将中文标点符号（包括逗号、句号、问号、括号等）和英文标点符号单独提取出来
            extracted_text = re.sub(r'([，。！？（）《》【】、“”‘’])', r' \1 ', extracted_text)
            extracted_text = re.sub(r'([\(\)\[\]\{\},.!?])', r' \1 ', extracted_text)

            # 将多个空格替换为单个空格
            extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()

            print(f"Extracted text: {extracted_text}")
        else:
            print("Start marker not found in generated text.")
            extracted_text = ""  # 若未找到标记，则将提取文本设为空

        # 追加结果并换行，以防止不同行的结果粘连
        result += extracted_text + '\n'

# 记录推理结束时间，并打印推理耗时
end = time.time()
print(f'Inference time for row {index}: {end - st:.2f} s')

# 保存带有生成结果和分词结果的新的txt文件，分隔符为制表符（Tab）
output_path = r"D:\王世屹\大学\计算机\自然语言处理\第一次\qwenLLM\1done.txt"

# 使用 with 语句来确保文件正确关闭
with open(output_path, "w", encoding="utf-8") as file:
    file.write(result)
print("Processing complete. Results saved to txt file.")
