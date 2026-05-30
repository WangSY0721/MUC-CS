def merge_dicts(list_of_dicts):
    result = {}
    for d in list_of_dicts:
        result.update(d)
    return result

list_of_dicts = [{6: [1, 2, 3]}, {28: [1, 2, 4, 7, 14]}, {496: [1, 2, 4, 8, 16, 31, 62, 124, 248]}]
print(merge_dicts(list_of_dicts))
