'''
Created on Mar 1, 2016

@author: maverick
'''
import requests
import json
'''
def devdict_get(ip,port):
    url = "http://"+ip+":"+port+"/ZWaveAPI/Data/*"
    response = requests.post(url)
    data = response.json()
    temp_dict = {}
    dev_dict = {}

    if data != None:
        for i in data["devices"]:
            if i != "1":    #Device_1 is main controller
                temp_dict["id"] = i
                temp_dict["type"] = data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]
                dev_dict["device_"+i+""] = dict(temp_dict)
        return dev_dict

print devdict_get("192.168.1.131","8083")
'''