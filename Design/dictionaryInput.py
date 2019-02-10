#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlConnector import mySql_Connector as sql


# 正面情感词典（中文）导入数据库
def positiveEmotionDicInput():
    fileObj = open('F:\Design\Dictionary\正面情感词语（中文）.txt', 'r')
    try:
        text = fileObj.read()
        textList = text.split('\n')
        wordId = 0
        for i in textList:
            wordId += 1
            sql.insertPositiveEmotionValues(wordId, i.strip())

        print('正面情感词典导入完毕')
        print('总共添加', wordId, '个正面情感词汇')
    except Exception as e:
        print(e)
    finally:
        fileObj.close()


# 负面情感词典（中文）导入数据库
def negativeEmotionDicInput():
    fileObj = open('F:\Design\Dictionary\负面情感词语（中文）.txt', 'r')
    try:
        text = fileObj.read()
        textList = text.split('\n')
        wordId = 0
        for i in textList:
            wordId += 1
            sql.insertNegativeEmotionValues(wordId, i.strip())

        print('负面情感词典导入完毕')
        print('总共添加', wordId, '个负面情感词汇')
    except Exception as e:
        print(e)
    finally:
        fileObj.close()


# 正面评价词典（中文）导入数据库
def positiveEvaluationDicInput():
    fileObj = open('F:\Design\Dictionary\正面评价词语（中文）.txt', 'r')
    try:
        text = fileObj.read()
        textList = text.split('\n')
        wordId = 0
        for i in textList:
            wordId += 1
            sql.insertPositiveEvaluationValues(wordId, i.strip())

        print('正面评价词典导入完毕')
        print('总共添加', wordId, '个正面评价词汇')
    except Exception as e:
        print(e)
    finally:
        fileObj.close()


# 负面评价词典（中文）导入数据库
def negativeEvaluationDicInput():
    fileObj = open('F:\Design\Dictionary\负面评价词语（中文）.txt', 'r')
    try:
        text = fileObj.read()
        textList = text.split('\n')
        wordId = 0
        for i in textList:
            wordId += 1
            sql.insertNegativeEvaluationValues(wordId, i.strip())

        print('负面评价词典导入完毕')
        print('总共添加', wordId, '个负面评价词汇')
    except Exception as e:
        print(e)
    finally:
        fileObj.close()


if __name__ == '__main__':
    positiveEmotionDicInput()
    negativeEmotionDicInput()
    positiveEvaluationDicInput()
    negativeEvaluationDicInput()
