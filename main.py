from selenium import webdriver
import time
import datetime
import os
import logging
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def page(x):
    page_list = driver.find_elements_by_class('num')
    print(page_list[x].text)

def news(n, z, c):#id 耗时 次数
    news_list = driver.find_elements_by_id(n) #找到对应日期元素组，注意是elements
    
    f = open('./log.txt', 'r')
    t = f.read().replace('\n','')
    b = 0
    reads = 0
    for y,index in enumerate(range(0,20)):
        if news_list[y].text in t:
            print('已读文章，跳过')
            reads = reads + 1
            pass
        else:
            print('{}阅读>>{}'.format(index + 1 - reads, news_list[y].text))
            logging.info('{}'.format(news_list[y].text))
            news_list[y].click()
            time.sleep(1)
            b = b + 1
            if b == c:
                print('已经阅读至上限数量，跳出，等待页面耗时完毕')
                break
    if b < c:
        print('>>没有读够，但是当前页面文章都读过了')
        next_list = driver.find_element_by_xpath("//*[@class='next']")
        print('>>翻到下一页继续读')
        next_list.click()
        news(n, z, c - b)

    MainPage = driver.current_window_handle
    AllPage = driver.window_handles
    body = driver.find_element_by_class_name('content')
    for i in AllPage:
        if i != MainPage:
            driver.switch_to.window(i)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            print('请等待，正在计时')
            time.sleep(z * 60 + 5)            
login_url = 'https://pc.xuexi.cn/points/login.html'
zhxw_url = 'https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html'
xwlb_url = 'https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html'
xxjf_url = 'https://pc.xuexi.cn/points/my-points.html'
test_url = 'https://www.xuexi.cn/cc61a68c398ea999913e937a8d8f1d11/e43e220633a65f9b6d8b53712cba9caa.html'
driver = webdriver.Chrome()
driver.set_window_size(450, 450)
#https://pc.xuexi.cn/points/my-study.html
#https://pc.xuexi.cn/points/my-points.html
print('>>打开学习首页')
driver.get(login_url)
##滚动到二维码
qr = driver.find_element_by_id('ddlogin-iframe')
for i in range(24):
    qr.send_keys(Keys.DOWN)
for i in range(10):
    qr.send_keys(Keys.RIGHT)
#driver.execute_script(js)
while True:
    try:
        verror = driver.find_element_by_class_name('text-title')
        if verror:
            print('登录成功，即将开始学习')
            time.sleep(1)
            break
    except NoSuchElementException:
        print('等待扫描二维码登录<<')
        time.sleep(2)

logging.basicConfig(filename='log.txt',level=logging.INFO)

#综合新闻 4分钟以上加1分，上限8分
driver.get(zhxw_url)
news('Ca4gvo4bwg7400', 4, 8)
#视频 5分钟以上加1分，上限10分
driver.get(xwlb_url)
news('Ck3ln2wlyg3k00', 4, 10)
driver.get(xxjf_url)
score = driver.find_elements_by_class_name('my-points-points') #积分元素切片
print('学习完毕，今日积分：{}'.format(score[1].text))
driver.quit()
