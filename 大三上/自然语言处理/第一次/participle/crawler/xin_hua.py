import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 设置 Chrome 浏览器选项
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 运行无界面浏览器

# 启动浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 打开目标网页
base_url = "http://info.search.news.cn/#search/0/%E4%B8%AD%E5%9B%BD%E5%88%B6%E9%80%A0/page={page}/0"

# 循环生成 URL
urls = []
for page in range(1, 100):  # 可修改页面范围，3只是示例
    url = base_url.format(page=page)
    urls.append(url)

visited_urls = set()  # 保存已访问过的 URL
content_set = set()  # 保存已抓取过的内容（基于前几个字符进行去重）
listContent = []  # 保存内容

for url1 in urls:
    driver.get(url1)
    try:
        list1 = []
        # 等待元素加载并获取元素
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '/html/body/div/div/div[2]/div[3]/div/div/div/div[3]/div[1]/div/div[1]/a'))
        )

        # 提取所有元素的 href 属性
        for element in elements:
            href_value = element.get_attribute('href')
            # 如果 URL 已经访问过，则跳过
            if href_value not in visited_urls:
                visited_urls.add(href_value)
                list1.append(href_value)

        for url in list1:
            # 增加重试机制
            for attempt in range(3):  # 尝试最多 3 次
                try:
                    # 访问每个 URL 页面
                    driver.get(url)

                    # 等待页面完全加载
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH,
                                                             '/html/body/div[13]/div[1]/div[1]/span/p | '
                                                             '/html/body/div[9]/div/div/span/p | /html/body/div[11]/div/div[1]/span/p'))
                    )

                    # 初始化 content 变量
                    content = ""

                    # 获取所有匹配的元素
                    text_elements = driver.find_elements(By.XPATH,
                                                         '/html/body/div[13]/div[1]/div[1]/span/p | /html/body/div[9]/div/div/span/p | /html/body/div[11]/div/div[1]/span/p')

                    # 提取并连接文本内容
                    for item in text_elements:
                        content += item.text + " "  # 添加一个空格分隔每段文本

                    # 通过前100个字符检查是否重复
                    if content[:100] not in content_set:
                        content_set.add(content[:100])  # 保存前100个字符作为标识
                        listContent.append(content)  # 保存完整内容
                        print(content)
                        print('----------------------------------------------------')

                    # 成功处理后跳出重试循环
                    break

                except Exception as e:
                    print(f"Error occurred while processing URL {url} (attempt {attempt + 1}): {e}")
                    # 等待一段时间后重试
                    time.sleep(5)

    except Exception as e:
        print(f"Error occurred while processing URL {url1}: {e}")

# 输出到 txt 文件
with open('output.txt', 'w', encoding='utf-8') as file:
    for content in listContent:
        file.write(content + '\n')
