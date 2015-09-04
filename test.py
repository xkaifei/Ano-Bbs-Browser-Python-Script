#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys 
import urllib 
import string 
import json
baseUrl = "http://h.nimingban.com/Api"
forumList = [];
def getJsonFromUrl(url):
    resp = urllib.urlopen(url)
    return json.loads(resp.read())


def convert(orig):
    return (re.sub(r'\\u\w{4}',
        lambda e: unichr(int(e.group(0)[2:], 16)).encode('utf-8'), 
        orig))
def cPrint(str):
    print convert(str)

def printHelp():
    print "help"
    
def printForum():
    forumListStr = ""
    for fName in forumList:
        forumListStr += (" [" + fName[0] + ", " + fName[1] + "]")
    cPrint(forumListStr)

def showForum(id, page):
    forumPageJson = getJsonFromUrl(baseUrl + "/showf?id=" + id + "&page=" + page)
    for thread in forumPageJson:
        str = "["
        str += (thread["id"] + " " + thread["replyCount"] + "]" + thread["content"])
        cPrint(str);

def showThread(id, page):
    threadPageJson = getJsonFromUrl(baseUrl + "/thread?id=" + id + "&page=" + page)
    printSingleReply(threadPageJson)
    for reply in threadPageJson["replys"]:
        printSingleReply(reply)

threadProperties = [
    ["now", u"时间"],
    ["title", u"标题"],
    ["img", u"图"],
    ["replyCount", u"回复"],
]

opHisQueue = [["h"]]
opHisPos = 0

def printSingleReply(sJson):
    str = "["
    for prop in threadProperties:
        if sJson.has_key(prop[0]):
            str += (prop[1] + ":" + sJson[prop[0]] + " ")
    str += "]" + sJson[u"content"]
    cPrint(str)

def forumOp(param = "all", page = "1"):
    print u"查看板块id:" + param + u" 第" + page + u"页"
    if param == "all":
        printForum()
    else :
        showForum(param, page)

def threadOp(param = "null", page = "1"):
    print u"查看串:" + param + u" 第" + page + u"页"
    if param == "null":
        print u"请在参数输入串号"
    else :
        showThread(param, page)

def fowardOp():
    global opHisQueue
    global opHisPos
    print u"前进"
    if opHisPos < len(opHisQueue) - 1:
        opHisPos += 1
    return opHisQueue[opHisPos]

def backOp():
    global opHisQueue
    global opHisPos
    print u"后退"
    if opHisPos > 0:
        opHisPos += -1
    return opHisQueue[opHisPos]
    
def prevOp():
    global opHisQueue
    global opHisPos
    print u"前一页"
    inputList = opHisQueue[opHisPos]
    if inputList[0] not in ["F", "t"] or len(inputList) < 2:
        return inputList
    if len(inputList) > 2:
        page = inputList[2]
        del inputList[2]
    else:
        page = 1
    if page > 1:
        inputList.insert(2, str(int(page) - 1))
    return inputList
def nextOp():
    global opHisQueue
    global opHisPos
    print u"后一页"
    inputList = opHisQueue[opHisPos]
    print inputList
    if inputList[0] not in ["F", "t"] or len(inputList) < 2:
        return inputList
    if len(inputList) > 2:
        page = inputList[2]
        del inputList[2]
    else:
        page = 1
    #向后翻页不做限制
    inputList.insert(2, str(int(page) + 1))
    return inputList
def quitOp():
    print u"退出"
    
operationDict = {
    "F":[forumOp, 2],
    "t":[threadOp, 2],
    "q":[quitOp, 0]
}

shortOpDict = {
    "f": fowardOp,
    "b": backOp,
    "p": prevOp,
    "n": nextOp
}
def queueAdd(opList):
    global opHisQueue
    global opHisPos
    opHisQueue = opHisQueue[:opHisPos + 1]
    opHisQueue.append(opList)
    opHisPos += 1
    
def mainLoop():
    input = raw_input()
    while(input != "q"):
        inputList = input.split(" ")
        isNewOp = 1
        if shortOpDict.has_key(inputList[0]):
            if inputList[0] in ["f", "b"]:
                isNewOp = 0
            inputList = shortOpDict[inputList[0]]()
        if not operationDict.has_key(inputList[0]):
            printHelp()
            isNewOp = 0
        elif operationDict[inputList[0]][1] == 2 and len(inputList) == 3:
            operationDict[inputList[0]][0](inputList[1], inputList[2])          
        elif operationDict[inputList[0]][1] > 0 and len(inputList) == 2:
            operationDict[inputList[0]][0](inputList[1])
        else :
            operationDict[inputList[0]][0]()
        if isNewOp:
            queueAdd(inputList)
        
        input = raw_input() 
    
def main():
    forumBigList = getJsonFromUrl(baseUrl + "/getForumList")
    #forumBigList = [{"forums":[{"name":"test", "id":"1"},{"name":"test1", "id":"2"}]}]
    for forums in forumBigList:
        for forum in forums['forums']:
            forumList.append((forum["name"], forum["id"]))
    print "start!"
    mainLoop()

if __name__ == '__main__':
    main()
