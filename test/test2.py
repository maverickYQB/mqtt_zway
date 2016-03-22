'''
Created on Mar 1, 2016

@author: maverick
'''
import requests
import json

def devFind(ip,port):
    url = "http://"+ip+":"+port+"/ZWaveAPI/Data/*"
    response = requests.post(url)
    data = response.json()
    devList = {}

    if data != None:
        for i in data["devices"]:
            if i != "1":    #Device_1 is main controller
                devList["id"] = i
                devList["type"] = data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]
                devList["updateTime"] = data["devices"][""+i+""]["data"]["updateTime"]
                print devList
                return devList


print(devFind("192.168.1.131","8083"))
