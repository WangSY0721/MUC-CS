sorted_list_str = input("请输入已排序的列表，数字之间用空格分隔：")
sorted_list = [int(item) for item in sorted_list_str.split()]

num_to_insert = int(input("请输入需要插入的数值："))

def insert_into_sorted_list(sorted_list, num):
    for i in range(len(sorted_list)):
        if sorted_list[i] >= num:
            sorted_list.insert(i, num)
            return sorted_list
    sorted_list.append(num)
    return sorted_list

updated_list = insert_into_sorted_list(sorted_list, num_to_insert)

print("插入后的列表为：", updated_list)
