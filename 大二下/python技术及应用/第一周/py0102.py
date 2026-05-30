def is_leap_year(year):  # 判断是否为闰年
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def days_in_month(year, month):  # 月份对应的天数
    days_in_month = 31
    if month in [4, 6, 9, 11]:
        days_in_month = 30
    elif month == 2:
        if is_leap_year(year):
            days_in_month = 29
        else:
            days_in_month = 28
    return days_in_month

year = int(input("请输入年份："))
month = int(input("请输入月份："))

num_days = days_in_month(year, month)
print(f"{year}年{month}月有{num_days}天。")
