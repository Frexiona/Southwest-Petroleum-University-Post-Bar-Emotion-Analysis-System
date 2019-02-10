#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector as Sql


# 连接数据库函数
def connectSql():
    conn = Sql.connect(host='127.0.0.1', user='root', password='506825', database='Design')
    return conn


# 填充首页信息函数
def insertIndexValues(TitleUrl):
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('insert into Index_Information values(\'%s\',\'no\')' % TitleUrl)
        conn.commit()
    except Exception as e:
        print(e)
        print('insertIndexValues函数错误')
    finally:
        cur.close()
        conn.close()


# 取出还没有被分析的首页url
def selectIndexCheckedValues():
    sqlUrl = set()

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select * from Index_Information where urlCheck=\'no\'')
        for i in cur.fetchall():
            sqlUrl.add(i[0])
        return sqlUrl
    except Exception as e:
        print(e)
        print('selectIndexCheckedValues函数错误')
    finally:
        cur.close()
        conn.close()


# 取出首页URL函数
def selectIndexValues():
    sqlUrl = set()

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select titleUrl from Index_Information')
        for i in cur.fetchall():
            sqlUrl.add(i[0])
        return sqlUrl
    except Exception as e:
        print(e)
        print('selectIndexValues函数错误')
    finally:
        cur.close()
        conn.close()


# 更新首页check选项函数
def updateIndexValues(url):
    readingUrl = url
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('update Index_Information set urlCheck=\'yes\' where titleUrl=\'%s\'' % readingUrl)
        conn.commit()
    except Exception as e:
        print(e)
        print('updateIndexValues函数错误')
    finally:
        cur.close()
        conn.close()


# 填充贴子信息函数
def insertPageValues(url, tN, uN, uE, eT, cN):
    titleUrl = url
    titleName = tN
    upName = uN
    upEssay = uE
    essayTime = eT
    commentsNum = cN
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute(
            'insert into Page_Informaion values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%d\',\'no\')' % (
                titleUrl, titleName,
                upName, upEssay,
                essayTime, commentsNum))
        conn.commit()
    except Exception as e:
        print(e)
        print('insertPageValues函数错误')
    finally:
        cur.close()
        conn.close()


# 存储评论函数
def insertCommentsValues(u, c):
    url = u
    comments = c
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('insert into  Comments_Information values(\'%s\',\'%s\',\'no\')' % (url, comments))
        conn.commit()
    except Exception as e:
        print(e)
        print('insertCommentsValues函数错误')
    finally:
        cur.close()
        conn.close()


# 删除无用的url
def deleteIndexUrl(u):
    url = u
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('delete from Index_Information where titleUrl=\'%s\'' % url)
        conn.commit()
    except Exception as e:
        print(e)
        print('deleteIndexUrl函数错误')
    finally:
        cur.close()
        conn.close()


# 正面情感词典的导入
def insertPositiveEmotionValues(i, w):
    wordId = i
    word = w
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('insert into positiveEmotion_Dic values(%s,\'%s\')' % (wordId, word))
        conn.commit()
    except Exception as e:
        print(e)
        print('insertPositiveEmotionValues函数错误')
    finally:
        cur.close()
        conn.close()


# 负面情感词典的导入
def insertNegativeEmotionValues(i, w):
    wordId = i
    word = w
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('insert into negativeEmotion_Dic values(%s,\'%s\')' % (wordId, word))
        conn.commit()
    except Exception as e:
        print(e)
        print('insertNegativeEmotionValues函数错误')
    finally:
        cur.close()
        conn.close()


# 正面评价词典的导入
def insertPositiveEvaluationValues(i, w):
    wordId = i
    word = w
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('insert into positiveEvaluation_Dic values(%s,\'%s\')' % (wordId, word))
        conn.commit()
    except Exception as e:
        print(e)
        print('insertPositiveEvaluationValues函数错误')
    finally:
        cur.close()
        conn.close()


# 负面评价词典的导入
def insertNegativeEvaluationValues(i, w):
    wordId = i
    word = w
    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('insert into negativeEvaluation_Dic values(%s,\'%s\')' % (wordId, word))
        conn.commit()
    except Exception as e:
        print(e)
        print('insertNegativeEvaluationValues函数错误')
    finally:
        cur.close()
        conn.close()


# 正面情感词典的取出
def selectPositiveEmotionValues():
    positiveEmotionValues = set()

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select positiveWord from positiveEmotion_Dic')
        for i in cur.fetchall():
            positiveEmotionValues.add(i[0])
        return positiveEmotionValues
    except Exception as e:
        print(e)
        print('selectPositiveEmotionValues函数错误')
    finally:
        cur.close()
        conn.close()


# 负面情感词典的取出
def selectNegativeEmotionValues():
    negativeEmotionValues = set()

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select negativeWord from negativeEmotion_Dic')
        for i in cur.fetchall():
            negativeEmotionValues.add(i[0])
        return negativeEmotionValues
    except Exception as e:
        print(e)
        print('selectNegativeEmotionValues函数错误')
    finally:
        cur.close()
        conn.close()


# 正面评价词典的取出
def selectPositiveEvaluationValues():
    positiveEvaluationValues = set()

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select positiveWord from positiveEvaluation_Dic')
        for i in cur.fetchall():
            positiveEvaluationValues.add(i[0])
        return positiveEvaluationValues
    except Exception as e:
        print(e)
        print('selectPositiveEvaluationValues函数错误')
    finally:
        cur.close()
        conn.close()


# 负面评价词典的取出
def selectNegativeEvaluationValues():
    negativeEvaluationValues = set()

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select negativeWord from negativeEvaluation_Dic')
        for i in cur.fetchall():
            negativeEvaluationValues.add(i[0])
        return negativeEvaluationValues
    except Exception as e:
        print(e)
        print('selectNegativeEvaluationValues函数错误')
    finally:
        cur.close()
        conn.close()


# 取出还没有被分析的贴子url
def selectPageCheckedValues():
    sqlUrl = set()

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select titleUrl from Page_Informaion where checkId=\'no\'')
        for i in cur.fetchall():
            sqlUrl.add(i[0])
        return sqlUrl
    except Exception as e:
        print(e)
        print('selectPageCheckedValues函数错误')
    finally:
        cur.close()
        conn.close()


# 标题和正文的取出（返回值是字典！！！）
def selectTitleEssayValues(u):
    url = u

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select titleName,upEssay from Page_Informaion where titleUrl=\'%s\'' % url)
        i = cur.fetchall()
        informationDict = {i[0][0]: i[0][1]}

        cur.execute('update Page_Informaion set checkId=\'yes\' where titleUrl=\'%s\'' % url)
        conn.commit()
        return informationDict
    except Exception as e:
        print(e)
        print('selectTitleEssayValues函数错误')
    finally:
        cur.close()
        conn.close()


# 所有评论的取出
def selectCommentsValues(u):
    titleInformation = set()

    url = u

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('select comments from Comments_Information where titleUrl=\'%s\';' % url)
        for i in cur.fetchall():
            titleInformation.add(i[0])
        cur.execute('update Comments_Information set checkId=\'yes\' where titleUrl=\'%s\'' % url)
        conn.commit()
        return titleInformation
    except Exception as e:
        print(e)
        print('selectCommentsValues函数错误')
    finally:
        cur.close()
        conn.close()


# 存储到帖子最终分析结果表
def insertEmotionResultValues(u, tN, tEE, cE):
    url = u
    titleName = tN
    tileEssayEmotion = tEE
    commentsEmotion = cE

    conn = connectSql()
    cur = conn.cursor()
    try:
        cur.execute('insert into pageEmotionResult values(\'%s\',\'%s\',\'%s\',\'%s\')' % (
            url, titleName, tileEssayEmotion, commentsEmotion))
        conn.commit()
    except Exception as e:
        print(e)
        print('insertEmotionResultValues函数错误')
    finally:
        cur.close()
        conn.close()
