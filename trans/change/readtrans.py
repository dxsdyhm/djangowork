#!/usr/bin/python
#-*- coding: utf-8-*-
import os
import re

# 遍历Lucy中的中文字符串,如果在result中能够完整找到则保留
# 找不到则写入文本
import shutil

from xlwt import Workbook

from djangowork.settings import BASE_DIR

changeList={}
changePath='/trans/static/result.txt'
stringPath='delete.txt'
allPath='all.xls'
lucy='/trans/static/lucy.txt'
pointPath='point.txt'


zh_pattern=re.compile(u'[\u4e00-\u9fa5]+')

transerrorPath="error.txt"

def contain_zh(word):
    # word=word.decode()
    global zh_pattern
    return zh_pattern.search(word)

def getMark(mark):
    if(mark==0):
        return "小豚当家已完成翻译汇总"
    elif(mark==1):
        return "废弃但已经翻译完成的"
    elif (mark == 2):
        return "未翻译"
    elif (mark == 3):
        return "交集"
    else:
        return mark

def writeExcel(filepath,tran,A):
    book = Workbook(encoding='utf-8')
    sheet1 = book.add_sheet(getMark(0))
    sheet2 = book.add_sheet(getMark(1))
    sheet3 = book.add_sheet(getMark(2))
    rowSheet1=0
    rowSheet2=0
    rowSheet3=0

    for zh in tran:
        # print(zh)
        if zh in A.keys():
            sheet1.write(rowSheet1, 0, zh)
            sheet1.write(rowSheet1, 1, A[zh])
            rowSheet1+=1
        else:
            sheet3.write(rowSheet3, 0, zh)
            rowSheet3+=1

    for zh in A.keys():
        print(zh)
        if zh not in tran:
            sheet2.write(rowSheet2, 0, zh)
            sheet2.write(rowSheet2, 1, A[zh])
            rowSheet2+=1
    book.save(filepath)

    print("1:{0},2:{1},3:{2}".format(rowSheet1,rowSheet2,rowSheet3))

def checkErrorFile(transSet):
    f=open(transerrorPath,"w+")
    for tans in transSet.keys():
        if tans.count("@") != transSet[tans].count("@"):
            f.writelines(tans)
            f.writelines('\n')
            f.writelines(transSet[tans])
            f.writelines('\n')
            f.writelines('\n')
    f.flush()
    f.close()

def checkPointFile(transSet):
    f=open(pointPath,"w+")
    for tans in transSet.keys():
        value=transSet[tans]
        if len(value)<=20 and '.' in value and '...' not in value:
            f.writelines(value)
            transSet[tans]=value.rstrip('.')
            f.writelines('\n')
    f.flush()
    f.close()

def doWork():
    resultSet=set()
    f=open(stringPath,'w+')
    for line in open(changePath,'r'):
        line=line.strip()
        resultSet.add(line)
    print(len(resultSet))

    transResult = getAllTrans()
    print(len(transResult))

    checkErrorFile(transResult)
    checkPointFile(transResult)
    writeExcel(allPath,resultSet,transResult)

def getAllTrans():
    transResult = {}
    lucypath=BASE_DIR+lucy
    flucy = open(lucypath, 'r')
    lines = flucy.readlines()
    count = len(lines)

    for i in range(count - 1):
        key = lines[i]
        values = lines[i + 1]

        key = key.strip()
        values = values.strip()

        if contain_zh(key):
            transResult[key] = values
    return transResult

def getUse():
    resultSet = set()
    lucypath = BASE_DIR + changePath
    for line in open(lucypath, 'r'):
        line = line.strip()
        resultSet.add(line)
    return resultSet