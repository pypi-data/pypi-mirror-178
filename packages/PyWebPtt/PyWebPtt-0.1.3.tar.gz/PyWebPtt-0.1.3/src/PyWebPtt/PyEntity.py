# -*- coding: utf-8 -*-

class DataRecordListDict:
    def __init__(self):
        self.dict = dict()#{}

    def add(self, key, data):
        dataList = self.dict.get(key)
        if dataList == None:
            dataList = list()
        dataList.append(data)
        self.dict[key] = dataList #https://selflearningsuccess.com/python-dictionary/#%E4%BD%BF%E7%94%A8setdefault%E6%96%B9%E6%B3%95%E5%A2%9E%E5%8A%A0%E9%A0%85%E7%9B%AE

    def getList(self, key):
        return self.dict.get(key)

    def get(self, key, inex):
        return self.dict.get(key).get(index)

    def keys(self):
        return self.dict.keys()
