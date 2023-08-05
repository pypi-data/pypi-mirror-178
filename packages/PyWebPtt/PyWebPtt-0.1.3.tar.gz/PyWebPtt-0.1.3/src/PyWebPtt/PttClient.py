# -*- coding: utf-8 -*-

from WebLib import HtmlClient
from PyEntity import DataRecordListDict
import re

class PttClient:
    def __init__(self):
        self.htmlClient = HtmlClient()

    def getPttArticle(self, url: str): #-> PttArticle:
        parsedData = self.htmlClient.getHtml(url)
        return PttArticle(parsedData)


class PttArticle:
    def __init__(self, htmlData=None) -> None:
        self.htmlData = htmlData
        self.htmlPttPushData = None
        self.pttPushList = None

        self.__doSetupPttPushList()

    # def __doSetupPttArticle__(self):
    def __doSetupPttPushList(self) -> None:
        if self.htmlData != None:
            self.pttPushList = []
            self.personalPushDict = DataRecordListDict()

            #self.htmlPttPushData = self.htmlData.find_all(class_='push')
            self.htmlPttPushData = self.htmlData.find(text="※ 文章網址: ").findAllNext(class_='push')

            htmlPushList = self.htmlPttPushData
            for htmlPush in htmlPushList:
                pttPush = PttPush(htmlPush)
                self.pttPushList.append(pttPush)

                userId = pttPush.userId
                self.personalPushDict.add(userId, pttPush)

    def getHtmlData(self):
        return self.htmlData

    def getHtmlPttPushData(self):
        return self.htmlPttPushData

    def getPttPush(self, level): #-> PttPush:
        if level == None:
            print("Level is None")
        else:
            #index = len(self.pttPushList) - level - 1
            if level >= 1:
                index = level - 1
                #print(index)
                return self.pttPushList[index]
            else:
                #throw exception
                return None

    def getPttPushList(self) -> list:
        return self.pttPushList

    def getPttPusherIdList(self):
        return self.personalPushDict.keys()

    def getPttPushListByUserId(self, userId) -> list:
        return self.personalPushDict.getList(userId)


class PttPush:
    def __init__(self, htmlData=None):
        self.htmlData = htmlData
        self.tag = None
        self.userId = None
        self.content = None
        self.ipDateTime = None
        self.contentRegExp = None
        self.__doSetupPushContentRegExpProcessor()
        self.__doSetupPttPush()

    def __doSetupPushContentRegExpProcessor(self):
        self.contentRegExp = re.compile('^: ') #推文內容解析出來，最前面會「: 」，需要regExp幫忙拿除

    def __doSetupPttPush(self):
        if self.htmlData != None:
            self.tag = self.htmlData.find(class_='push-tag').getText()
            self.userId = self.htmlData.find(class_='push-userid').getText()
            self.content = self.contentRegExp.sub('', self.htmlData.find(class_='push-content').getText())
            self.ipDateTime = self.htmlData.find(class_='push-ipdatetime').getText()

    def getHtmlData(self):
        return self.htmlData

    def getTag(self):
        return self.tag

    def getUserId(self):
        return self.userId

    def getContent(self):
        return self.content

    def getIpDateTime(self):
        return self.ipDateTime

    def __str__(self) -> str:
        str = ""
        str += "評分 : " + self.tag + "\r\n"
        str += "使用者： " + self.userId + "\r\n"
        str += "內容： " + self.content + "\r\n"
        str += "IP與時間 : " + self.ipDateTime + "\r\n"
        return str
