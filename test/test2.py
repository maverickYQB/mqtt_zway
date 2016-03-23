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
    dev_list = dict()
    dev_dict = dict()

#MARCHE PAS revoir le return dict avec les dict des device trouve 
    if data != None:
        for i in data["devices"]:
            if i != "1":    #Device_1 is main controller
                dev_list["id"] = i
                dev_list["type"] = data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]
            dev_dict["device_"+i+""] = dev_list

            print dev_dict

devlist_get("192.168.1.131","8083")