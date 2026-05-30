import datetime

def calculate_age(birthdate):
    today = datetime.date.today()
    birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d").date()
    age_in_days = (today - birthdate).days
    return age_in_days

birthdate_input = input("请输入您的出生日期（格式:YYYY-MM-DD）:")
age_in_days = calculate_age(birthdate_input)
print("您的年龄是：{} 天".format(age_in_days))
