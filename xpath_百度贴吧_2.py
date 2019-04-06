#!/usr/bin/python3
# _*_coding:utf-8_*_
'''
爬取百度贴吧的视频和照片实例
'''
import time
import requests
from lxml import etree


# 获取一级页面信息
def get_page_1(url, headers):
    time.sleep(2)
    request_url_1 = requests.get(url, headers=headers)
    if request_url_1.status_code == 200:
        etree_page_1 = etree.HTML(request_url_1.text)
        etree_info = etree_page_1.xpath(
            '//div[@class="col2_right j_threadlist_li_right "]/div[@class="threadlist_lz clearfix"]/div[@class="threadlist_title pull_left j_th_tit "]/a/@href')
        return etree_info
    else:
        print("您请求的页面不存在")


# 获取二级界面信息
def get_page_2(page_url_2):
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
    }
    time.sleep(3)
    requests_url_2 = requests.get(page_url_2, headers=headers)
    if requests_url_2.status_code == 200:
        etree_page_2 = etree.HTML(requests_url_2.text)
        page_2_info = etree_page_2.xpath(
            '//div[@class="d_post_content j_d_post_content "]//img[@class="BDE_Image"]/@src | //div[@class="d_post_content j_d_post_content  clearfix"]/div[@class="video_src_wrapper"]/div[@class="video_src_wrap_main"]/video/@src')
        for info in page_2_info:
            save_info(info, headers)
    else:
        print('您请求的页面不存在')


# 保存信息
def save_info(info_url, headers):
    time.sleep(2)
    info_request = requests.get(info_url, headers=headers)
    info_request.encoding = 'utf-8'
    if info_request.status_code == 200:
        try:
            with open('{}'.format(info_url[-10:]), 'wb') as f:
                print('正在保存{}'.format(info_url[-10:]))
                f.write(info_request.content)
        except FileNotFoundError as e:
            print(e)
    else:
        print("您请求的页面不存在")


# 主函数
def main(key, page):
    # 常量
    url = "https://tieba.baidu.com/f?kw={}&pn={}".format(key, page)
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
    }
    page_1_url = get_page_1(url, headers)
    for page_2_info in page_1_url:
        # 构造page_2的url
        page_url_2 = 'https://tieba.baidu.com{}'.format(page_2_info)
        get_page_2(page_url_2)


if __name__ == '__main__':
    key = input("请输入要查找的贴吧名:")
    page_begin = int(input('请输入开始查询页数:'))
    page_end = int(input('请输入结束查询页数:'))
    for i in range((page_end - page_begin) * 50 + 1):
        page = i * 50
        print('正在解析第{}个页面'.format(i + 1))
        main(key, page)
