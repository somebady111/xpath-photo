#!/usr/bin/python3
# _*_coding:utf-8_*_
'''
xpath爬取糗事百科
'''
from lxml import etree
from bs4 import BeautifulSoup
import lxml
import requests
import csv
import time


# 获取信息
def get_info(url, headers):
    time.sleep(2)
    # 获取页面
    info = requests.get(url, headers=headers)
    info.encoding = 'utf-8'
    # 解析页面信息
    etree_info = etree.HTML(info.text)
    # etree_info构建的对象
    nickname = etree_info.xpath('//div[@id="content-left"]//div[@class="author clearfix"]//img/@alt')
    content = etree_info.xpath('//div[@class="content"]/span/text()')
    count_laught = etree_info.xpath('//div[@class="stats"]/span[@class="stats-vote"]/i[@class="number"]/text()')
    count_communt = etree_info.xpath('//span[@class="stats-comments"]//i[@class="number"]/text()')
    d = {
        'nickname': nickname,
        'content': content,
        'count_laught': count_laught,
        'count_communt': count_communt,
    }
    return d


# 保存信息
def save_info(info_list, page):
    for i in info_list['content']:
        with open('第{}页发帖.txt'.format(page // 25), 'w', encoding='utf-8') as f:
            f.write(i)


# 主函数
def main(page):
    # 参数
    url = "https://www.qiushibaike.com/text/page/{}/".format(page)
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
    }
    # 代理
    proxies = {
        "http": "",
        "https": ""
    }
    info_list = get_info(url, headers)
    save_info(info_list, page)


if __name__ == "__main__":
    n = int(input('请输入查询的页数:'))
    for i in range(1, n + 1):
        page = i * 25
        print("正在解析第{}页".format(page // 25))
        main(page)
