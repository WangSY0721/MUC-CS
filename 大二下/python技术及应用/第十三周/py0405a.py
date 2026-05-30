import pymysql
db = pymysql.connect(host="localhost", port=3306, user="root", passwd="Shuman2009", charset="utf8",db="homework")
cur = db.cursor()

try:
    cur.execute("create table stu(id int, name varchar(20), class varchar(30), age varchar(10))")
except:
    print("错误：该表可能已存在，不能创建！")
sql = "insert into stu(id,name,class,age) values (%s,%s,%s,%s)"
values = (2100000,"徐大侠","22计算机",99)
try:
    cur.execute(sql,values)
except:
    print("错误：该ID可能已经存在，不能插入数据！")
else:
    db.commit()

cur.execute("select * from stu")
result = cur.fetchall()
for row in result:
    print(row)

cur.close()
db.close()

