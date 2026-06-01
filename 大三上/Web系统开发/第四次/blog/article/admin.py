from django.contrib import admin
from article.models import User,Article
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=('username','email')
    list_filter=('username','email')
    search_fields=(['username','email'])

class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','content','publish_date')
    list_filter=('title',)
    search_fields=('title',)


admin.site.register(User,UserAdmin)
admin.site.register(Article,ArticleAdmin)#绑定 User 模型到 UserAdmimn管理后台