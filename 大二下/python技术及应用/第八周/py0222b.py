# 1、日龄功能
def calculate_age_in_days(start_date, end_date):
    def is_leap(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def days_in_month(month, year):
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            return 29 if is_leap(year) else 28
        else:
            return 0

    def days_since_year_start(date):
        year, month, day = map(int, date.split('-'))
        days = sum(days_in_month(m, year) for m in range(1, month)) + day
        return days if not is_leap(year) or month < 3 else days - 1

    start_year, start_month, start_day = map(int, start_date.split('-'))
    end_year, end_month, end_day = map(int, end_date.split('-'))

    days_start = days_since_year_start(start_date)
    days_end = days_since_year_start(end_date)

    total_days = sum(365 + is_leap(y) for y in range(start_year, end_year))
    total_days += days_end
    total_days -= days_start

    return total_days

# 2、闰年功能
is_leap_year = lambda year: (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

start_date = input("请输入起始日期，格式为YYYY-MM-DD: ")
end_date = input("请输入结束日期，格式为YYYY-MM-DD: ")
print("日期间的日龄差为:", calculate_age_in_days(start_date, end_date))

# 接收用户输入的年份并检查是否为闰年
input_year = int(input("请输入一个年份来检查是否为闰年: "))
print(f"{input_year}年是闰年吗?", is_leap_year(input_year))
