# 当电脑进入睡眠状态时，浏览器和其他应用程序会被暂停，导致正在运行的任务（如浏览器中的脚本或网页）被中断
# 在Windows上，进入“控制面板” > “硬件和声音” > “电源选项”，选择“更改计划设置”，然后确保“使计算机进入睡眠状态”的设置为“从不”。

import json
import os
import random
import time
from DrissionPage import ChromiumPage, WebPage
from DrissionPage.configs.chromium_options import ChromiumOptions
from DrissionPage.configs.session_options import SessionOptions
from bs4 import BeautifulSoup

topic1_list_of_lists = []
# 参数设置
num_Page = 100
base_dir = os.path.dirname(os.path.abspath(__file__))


class Demo(object):
    def __init__(self):
        # do = ChromiumOptions(ini_path=r'configs.ini')
        # so = SessionOptions(ini_path=r'configs.ini')
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ini_path = os.path.join(base_dir, 'configs.ini')
        do = ChromiumOptions(ini_path=ini_path)
        so = SessionOptions(ini_path=ini_path)
        self.page = WebPage(driver_or_options=do, session_or_options=so)
        self.weibourl = 'https://s.weibo.com/weibo?q=%E5%B7%B4%E9%BB%8E%E5%A5%A5%E8%BF%90%E4%BC%9A%EF%BC%8C%E4%B8%AD%E5%9B%BD%E5%88%B6%E9%80%A0&typeall=1&suball=1&timescope=custom%3A2024-07-01%3A2024-08-17&Refer=g&page=1'
        # 巴黎奥运会搜索：https://s.weibo.com/weibo?q=%E5%B7%B4%E9%BB%8E%E5%A5%A5%E8%BF%90%E4%BC%9A
        # 话题：https://s.weibo.com/weibo/%23%E5%B7%B4%E9%BB%8E%E5%A5%A5%E8%BF%90%E4%BC%9A%23
        # 中国制造搜索：'https://s.weibo.com/weibo?q=%23%E4%B8%AD%E5%9B%BD%E5%88%B6%E9%80%A0%23&nodup=1'
        # 话题：https://s.weibo.com/weibo?q=%23%E4%B8%AD%E5%9B%BD%E5%88%B6%E9%80%A0%23

    def get_data(self):
        print(self.weibourl)
        global num_Page
        p = 1
        tweets_list = []  # 创建一个空列表
        id = 1
        while True:
            # url=str(weiboUrl)+'&page='+ str(p)
            url = self.weibourl + '&page=' + str(p)
            # print(url)
            self.page.get(url)
            time.sleep(3)
            bs = BeautifulSoup(self.page.html, 'lxml')
            bs_div = [bd for bd in bs.select('.card') if not bd.find_previous_sibling(class_='card-top')]

            # print(len(bs_div))
            for bd in bs_div:
                try:
                    data = {}
                    try:
                        data['内容'] = bd.select('.txt')[1].text.replace('\n', '').replace('收起d', '').replace(
                            '\u200b', '').strip()

                    except:
                        data['内容'] = bd.select('.txt')[0].text.replace('\n', '').replace('收起d', '').replace(
                            '\u200b', '').strip()
                        data['字数'] = len(bd.select('.txt')[0].text)
                    data['id'] = id
                    id += 1
                    data['转发数'] = bd.select('.card-act li')[0].text.replace('\n', '').strip()
                    data['评论数'] = bd.select('.card-act li')[1].text.replace('\n', '').strip()
                    data['点赞数'] = bd.select('.card-act li')[2].text.replace('\n', '').strip()
                    data['用户ID'] = bd.select('.name')[0].text.replace('\n', '').strip()
                    data['链接'] = 'https:' + bd.select('.from a')[0]['href']
                    print(data)
                    tweets_list.append(data)  # 将第一部字典添加到列表中
                except:
                    pass
            p += 1
            if p > num_Page:
                break
        # 将列表转换为JSON格式的字符串
        json_str = json.dumps(tweets_list, ensure_ascii=False, indent=4)
        # 如果你想将这个JSON字符串写入到一个文件中
        # 文件路径
        file_path = '../../data/weibo_contents.json'
        directory = os.path.dirname(file_path)

        # 如果目录不存在，创建目录
        if not os.path.exists(directory) and directory != '':
            os.makedirs(directory)

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def get_detail(self):
        global topic1_list_of_lists

        with open('../../data/weibo_contents.json', 'r', encoding='utf-8') as f:
            datalist = json.load(f)

        tweets_list = []  # 创建一个空列表

        for data in datalist:
            print(data.get('链接'))
            self.page.get(data.get('链接'))
            time.sleep(random.randint(2, 4))

            # 预处理 HTML 内容以移除或替换有问题的字符
            clean_html = self.page.html.encode('utf-8', 'replace').decode('utf-8')

            # 使用不同的解析器
            bs = BeautifulSoup(clean_html, 'html.parser')

            bs = BeautifulSoup(self.page.html, 'lxml')

            c = {}
            c['id'] = data['id']
            # c['内容'] = data['内容']
            c['内容'] = data['内容'].replace('\ud835', '')  # 移除特定字符
            c['转发数'] = data['转发数']
            c['评论数'] = data['评论数']
            c['点赞数'] = data['点赞数']
            c['用户ID'] = data['用户ID']
            c['发布时间'] = bs.select('.head-info_time_6sFQg')[0].text  # 发布时间
            c['发布者IP属地'] = bs.select('.head-info_ip_3ywCW')[0].text. \
                replace('发布于', '').replace('\n', '').strip()

            c['链接'] = data['链接']
            tweets_list.append(c)
            self.page.scroll.down(500)
            time.sleep(1)

        print(tweets_list)

        json_str = json.dumps(tweets_list, ensure_ascii=False, indent=4)
        # 如果你想将这个JSON字符串写入到一个文件中
        # 文件路径
        file_path = '../../data/weibo_contents.json'
        directory = os.path.dirname(file_path)

        # 如果目录不存在，创建目录
        if not os.path.exists(directory) and directory != '':
            os.makedirs(directory)

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def run(self):
        self.get_data()
        self.get_detail()


# 实例化运行
t = Demo()
t.run()
