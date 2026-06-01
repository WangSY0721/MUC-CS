import pickle


def load_pkl_file(file_path):
    """
    加载.pkl文件并返回反序列化的对象。

    参数:
    file_path (str): .pkl文件的路径。

    返回:
    object: .pkl文件中序列化的对象。
    """
    try:
        with open(file_path, 'rb') as file:
            # 使用pickle.load()函数加载.pkl文件
            data = pickle.load(file)
            return data
    except Exception as e:
        print(f"无法加载文件：{e}")
        return None


# 使用示例
file_path = 'three_matrix.pkl'  # 替换为你的.pkl文件路径
loaded_data = load_pkl_file(file_path)

if loaded_data is not None:
    print("文件已成功加载，内容如下：")
    print(loaded_data)
else:
    print("文件加载失败。")