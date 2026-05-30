def read_and_sort_students(filename):
    try:
        with open(filename, 'r', encoding='GBK') as file:
            students = [line.strip().split(',') for line in file]
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='ISO-8859-1') as file:
            students = [line.strip().split(',') for line in file]

    students.sort(key=lambda student: int(student[0]))
    return students

def write_sorted_students(filename, sorted_students):
    with open(filename, 'w', encoding='GBK') as file:
        for student in sorted_students:
            file.write(','.join(student) + '\n')

unsorted_file = '名单 未排序.txt'
sorted_file = '名单 已排序.txt'

sorted_students = read_and_sort_students(unsorted_file)

write_sorted_students(sorted_file, sorted_students)

print(f"Sorted student list has been saved to {sorted_file}")
