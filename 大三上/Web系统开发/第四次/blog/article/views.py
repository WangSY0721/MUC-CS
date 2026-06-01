from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import datetime

from article.models import Article,User
from django.views import View
from article.forms import LoginForm

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})
    # return HttpResponse('article_list函数')


def year_archive(request, year):
    return HttpResponse(f'year_archive 函数接受参数 year:{year}')


def month_archive(request, year, month):
    return HttpResponse(f'month_archive 函数接受参数 year: {year} ,month: {month}')


def article_detail(request, year, month, slug):
    return HttpResponse(f'article detail 函数接受参数 year: {year},month: {month},slug:{slug}')


def article_re(request,year):
    return HttpResponse(f'正则表达式year is {year}')

def get_current_datetime(request):
    today = datetime.today()
    formatted_today = today.strftime('%Y-%m-%d')
    html=f"<html><body>今天是{formatted_today}</body></html>"
    return HttpResponse(html)

class LoginFormView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'login.html',{'form':LoginForm()})

    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            return HttpResponse(f'用户名:{username}, 邮箱:{email}')
        else:
            return render(request,'login.html',{'form':form})