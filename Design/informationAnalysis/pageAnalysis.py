#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlConnector import mySql_Connector as sql
import jieba

jieba.load_userdict("F:\Design\Dictionary\正面情感词语（中文）.txt")
jieba.load_userdict("F:\Design\Dictionary\负面情感词语（中文）.txt")
jieba.load_userdict("F:\Design\Dictionary\正面评价词语（中文）.txt")
jieba.load_userdict("F:\Design\Dictionary\负面评价词语（中文）.txt")


class emotionAnalysis():
    def __init__(self):
        pass

    # 得到没有被分析的url（返回形式是集合）
    def getUrl(self):
        urlList = sql.selectPageCheckedValues()
        print('总共有', len(urlList), '条贴子没有被分析')
        return urlList

    # 对正文和标题的情感分析
    def titleAnalysis(self, u):
        # 正面情感计数器
        countPositive = 0
        # 负面情感计数器
        countNegative = 0

        # 正负面情感词典的导入
        dicPositive1 = sql.selectPositiveEmotionValues()
        dicPositive2 = sql.selectPositiveEvaluationValues()
        dicNegative1 = sql.selectNegativeEmotionValues()
        dicNegative2 = sql.selectNegativeEvaluationValues()

        titleEssay = sql.selectTitleEssayValues(u)
        for key in titleEssay.keys():
            TitleName = str(key)
            Essay = str(titleEssay[key])

        # 对标题进行分析
        for word in jieba.cut(TitleName):
            if word in (dicPositive1 or dicPositive2):
                countPositive += 1
            elif word in (dicNegative1 or dicNegative2):
                countNegative += 1

        # 对正文进行分析
        for word in jieba.cut(Essay):
            if word in (dicPositive1 or dicPositive2):
                countPositive += 1
            elif word in (dicNegative1 or dicNegative2):
                countNegative += 1

        if (countPositive > countNegative):
            return '正面情感'
        elif (countPositive < countNegative):
            return '负面情感'
        else:
            return '中性情感'

    # 对评论的情感分析
    def commentsAnalysis(self, u):
        # 正面评价计数器
        countPositive = 0
        # 负面评价计数器
        countNegative = 0

        # 正负面评价词典的导入
        dicPositive = sql.selectPositiveEvaluationValues()
        dicNegative = sql.selectNegativeEvaluationValues()

        comments = sql.selectCommentsValues(u)
        for comment in comments:
            # 对标题进行分析
            for word in jieba.cut(comment):
                if word in dicPositive:
                    countPositive += 1
                elif word in dicNegative:
                    countNegative += 1

        if (countPositive > countNegative):
            return '正面评价'
        elif (countPositive < countNegative):
            return '负面评价'
        else:
            return '中性评价'

    # 存储函数
    def insertValuesIntoMysql(self, url, tEE, cE):
        titleEssayEmotion = tEE
        commentsEmotion = cE
        informationDic = sql.selectTitleEssayValues(url)
        for key in informationDic.keys():
            titleName = str(key)
        sql.insertEmotionResultValues(url, titleName, titleEssayEmotion, commentsEmotion)

    # 主函数
    def main(self):
        urlList = self.getUrl()
        # 计数器
        count = 1
        for i in urlList:
            print('第', count, '条链接正在被分析')
            print(i)
            titileResult = self.titleAnalysis(i)
            commentsResult = self.commentsAnalysis(i)
            self.insertValuesIntoMysql(i, titileResult, commentsResult)
            count += 1


if __name__ == '__main__':
    page = emotionAnalysis()
    page.main()
    print('数据库中未分析链接情感分析完毕')
