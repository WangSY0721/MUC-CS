from django.http import HttpResponse
from datetime import datetime

def article_list(request):
    return HttpResponse('article_list函数')


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