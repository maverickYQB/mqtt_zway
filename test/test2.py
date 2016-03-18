'''
Created on Mar 1, 2016

@author: maverick
'''
import requests
import json

def devFind(ip,port):
    url = "http://192.168.1.131:8083/ZWaveAPI/Data/*"
    url2 = "http://"+ip+":"+port+"/ZWaveAPI/Data/*"
    print (url)
    print (url2)
    response = requests.post(url)
    data = response.json()
    devList = {}
    
    if data != None:
        for i in data["devices"]:
            if i != "1":    #Device_1 is main controller
                devList[i] = data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]
                
        return (devList)
    
print(devFind("192.168.1.131","8083"))    