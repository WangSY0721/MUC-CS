def to_weird_case(s):
    result = ""  # 初始化结果字符串
    is_start_of_word = True  # 初始化一个标志，用来指示当前字符是否是一个单词的开始

    for char in s:
        if char.isalpha():  # 检查当前字符是否是字母
            if is_start_of_word:  # 如果当前位置是单词的开始，则将字符转换为大写
                result += char.upper()
            else:  # 如果不是单词的开始，则将字符转换为小写
                result += char.lower()
            is_start_of_word = False  # 既然当前字符是字母，那么我们还在单词中，因此设置标志为False
        else:  # 如果当前字符不是字母，我们将其添加到结果字符串，并将标志重置为True，因为下一个字母将是新单词的开始
            result += char
            is_start_of_word = True
    return result

user_input = input("请输入一段文本：")
print(to_weird_case(user_input))
