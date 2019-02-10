#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import bs4
from sqlConnector import mySql_Connector as sql

key = "User-Agent"
value = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"

# title_List = set()
title_UrlList = set()


class indexSpider:
    # 初始化函数
    def __init__(self):
        pass

    # 下载网页函数
    def urlOpen(self, url):
        req = urllib.request.Request(url)
        # req.add_header(key, value)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        titleHtml = bs4.BeautifulSoup(html, 'html5lib')

        return titleHtml

    '''
    # 标题爬取函数
    def titleScrap(title):
        global title_List
        titles = title.findAll("a", {"class": "j_th_tit "})
        for t in titles:
            if t not in title_List:
                title_List.add(t)

        return title_List
    '''

    # url爬取函数
    def titleUrl(self, titleHtml):
        global title_UrlList
        # 用于过滤首页前三个置顶帖（没有爬取的必要）的count参数
        count = 0;
        title_Url = titleHtml.findAll('a', {'class': 'j_th_tit '})
        sqlUrlList = set(sql.selectIndexValues())

        for t in title_Url:
            newUrl = 'http://tieba.baidu.com' + t.attrs['href']
            if newUrl not in sqlUrlList:
                if count >= 3:
                    title_UrlList.add(newUrl)
                count = count + 1

        print('新添加了', count - 3, '个链接')

        sqlUrlList.clear()

        return title_UrlList

    # 主函数
    def main(self):
        global title_UrlList
        # url为西南石油大学贴吧首页的地址
        url = "http://tieba.baidu.com/f?kw=%CE%F7%C4%CF%CA%AF%D3%CD%B4%F3%D1%A7&fr=ala0&tpl=5"
        title = self.urlOpen(url)
        # 抓取标题函数取消
        # titleScrap(title)
        for i in self.titleUrl(title):
            sql.insertIndexValues(i)

        title_UrlList.clear()


if __name__ == '__main__':
    index = indexSpider()
    index.main()
    print("总共有 2 个更新操作")
