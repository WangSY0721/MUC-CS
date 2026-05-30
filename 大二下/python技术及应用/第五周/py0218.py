string = input("请输入一个字符串：")

word_count = len(string.split())

letter_count = {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}
for char in string:
    if char.isalpha():
        char = char.lower()  # 统一转换为小写字母
        letter_count[char] += 1

unique_letters = sorted(set(char.lower() for char in string if char.isalpha()))

print("单词个数:", word_count)
print("每个字母出现次数:", letter_count)
print("出现的字母:", unique_letters)
