from django.db import models

# Create your models here.


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30) #用户名，字符串类型
    email = models.CharField(max_length=30) #邮箱，字符串类型


class Article(models.Model):
    id = models.IntegerField(primary_key=True )
    title = models.CharField(max_length=120)#标题，字符串类型
    content = models.TextField() #内容，文本类型
    publish_date = models.DateTimeField() #出版时间。日期时间类型
    user = models.ForeignKey(User,on_delete=models.CASCADE) #级联外键