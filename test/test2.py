'''
Created on Mar 1, 2016

@author: maverick
'''
import requests
import json

def devlist_get(ip,port):
    url = "http://"+ip+":"+port+"/ZWaveAPI/Data/*"
    response = requests.post(url)
    data = response.json()
    dev_list = []
    dev_dict = {}

#MARCHE PAS revoir le return dict avec les dict des device trouve
    if data != None:
        for i in data["devices"]:
            if i != "1":    #Device_1 is main controller
                dev_dict["id"] = i
                dev_dict["type"] = data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]
                dev_list.append(dict(dev_dict))
        return dev_list