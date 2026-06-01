# download
# from modelscope import snapshot_download, AutoModel, AutoTokenizer
# import os
# # 第一个参数表示下载模型的型号，第二个参数是下载后存放的缓存地址，第三个表示版本号，默认 master
# model_dir = snapshot_download('Qwen/Qwen2-1.5B-Instruct', cache_dir='qwen2chat_src', revision='master')

# int4
# from ipex_llm.transformers import AutoModelForCausalLM
# from transformers import  AutoTokenizer
# import os
# if __name__ == '__main__':
#     model_path = os.path.join(os.getcwd(),"qwen2chat_src/Qwen/Qwen2-1___5B-Instruct")
#     model = AutoModelForCausalLM.from_pretrained(model_path, load_in_low_bit='sym_int4', trust_remote_code=True)
#     tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
#     model.save_low_bit('qwen2chat_int4')
#     tokenizer.save_pretrained('qwen2chat_int4')