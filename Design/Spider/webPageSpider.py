#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib.request
import bs4
import re
from sqlConnector import mySql_Connector as sql


class webPageSpider:
    # 初始化函数
    def __init__(self):
        pass

    # 字符串过滤函数
    def checkStr(self, String):
        try:
            # python UCS-4 build的处理方式
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            # python UCS-2 build的处理方式
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

        resovle_value = highpoints.sub(u'', String)
        return resovle_value

    # 下载贴吧网页
    def urlOpen(self, url):
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8', 'ignore')
        bsHtml = bs4.BeautifulSoup(html, 'html5lib')
        return bsHtml

    # 验证urlopen函数
    def checkedUrlOpen(self, url):
        bsHtml = self.urlOpen(url)
        if bsHtml == 404:
            return 404
        elif bsHtml.find('body', {'class': 'page404'}):
            return 404
        else:
            return bsHtml

    # 楼主的一切所需要的信息爬取
    def webPageUpInformation(self, bsHtml, url):
        # 贴子标题
        web_titleName = bsHtml.find('h1', {'class': {'core_title_txt ', 'core_title_txt member_thread_title_pb '}})
        titleName = self.checkStr(web_titleName.get_text(strip=True))
        # 发帖人
        web_upName = bsHtml.find('a',
                                 {'class': {'p_author_name j_user_card', 'p_author_name sign_highlight j_user_card'}})
        upName = self.checkStr(web_upName.get_text(strip=True))
        # 贴子正文
        web_upEssay = bsHtml.find('div', {'class': 'd_post_content j_d_post_content clearfix'})
        upEssay = self.checkStr(web_upEssay.get_text(strip=True))
        # 发帖时间
        web_essayTime = bsHtml.find('div', {'class': 'l_post j_l_post l_post_bright noborder '})
        web_essayTimeJson = json.loads(web_essayTime['data-field'])
        essayTime = web_essayTimeJson.get('content').get('date')

        # 回复数量
        web_commentsNum = bsHtml.find('li', {'class': 'l_reply_num'}).find('span', {'style': 'margin-right:3px'})
        commentsNum = int(web_commentsNum.get_text(strip=True))

        # 打印标题
        print(titleName)

        # 存入数据库
        sql.insertPageValues(url, titleName, upName, upEssay, essayTime, commentsNum)

    # 所有评论的爬取（可判断翻页）
    def webPageCommentsInformation_crossPage(self, bsHtml, url):
        commentsList = set()
        web_pageNum = bsHtml.find('li', {'class': 'l_reply_num'}).findAll('span', {'class': 'red'})
        pageNum = int(web_pageNum[1].get_text(strip=True))

        # 打印页数
        print('总共有' + str(pageNum) + '页')

        for i in range(pageNum + 1):
            if (i > 0 and pageNum < 10):
                pageUrl = url + '?pn=' + str(i)
                bsHtml2 = self.urlOpen(pageUrl)
                if i == 1:
                    count = 0
                    web_comments = bsHtml2.findAll('div', {'class': 'd_post_content j_d_post_content clearfix'})
                    for comments in web_comments:
                        if count >= 1:
                            if len(self.checkStr(comments.get_text(strip=True))) != 0:
                                commentsList.add(self.checkStr(comments.get_text(strip=True)))
                        count = count + 1
                else:
                    web_comments = bsHtml2.findAll('div', {'class': 'd_post_content j_d_post_content clearfix'})
                    for comments in web_comments:
                        if len(self.checkStr(comments.get_text(strip=True))) != 0:
                            commentsList.add(self.checkStr(comments.get_text(strip=True)))
            elif (i > 0 and pageNum > 20):
                print('评论页数大于10，只选择最后10页作为信息参考')
                for i in range(pageNum + 1):
                    if i > (pageNum - 10):
                        pageUrl = url + '?pn=' + str(i)
                        bsHtml2 = self.urlOpen(pageUrl)
                        web_comments = bsHtml2.findAll('div', {'class': 'd_post_content j_d_post_content clearfix'})
                        for comments in web_comments:
                            if len(self.checkStr(comments.get_text(strip=True))) != 0:
                                commentsList.add(self.checkStr(comments.get_text(strip=True)))

        # 存储进入数据库：
        for i in commentsList:
            sql.insertCommentsValues(url, i)

    # 主函数
    def main(self):
        # 计数器
        count = 1
        sqlUrlList = sql.selectIndexCheckedValues()
        if len(sqlUrlList) == 0:
            print('没有网页未爬取的网页在数据库中，终止爬取')
        else:
            for i in sqlUrlList:
                print('第', count, '个网页正在爬取存储中')
                print(i)
                bsHtml = self.checkedUrlOpen(i)
                if bsHtml == 404:
                    sql.deleteIndexUrl(i)
                    print('此网页被删除或无法访问，跳过此网页')
                    continue
                else:
                    self.webPageUpInformation(bsHtml, i)
                    self.webPageCommentsInformation_crossPage(bsHtml, i)
                    sql.updateIndexValues(i)
                    count = count + 1
            print("这一轮爬取完毕")


if __name__ == '__main__':
    page = webPageSpider()
    page.main()
