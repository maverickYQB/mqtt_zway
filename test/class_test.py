#!/usr/bin/env python
'''
Created on Juin 5th 2016
    Test class

@author: popotvin
'''

import requests, socket

class zway_devList:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def dev_dict(self):
        temp_dict = {}
        dev_dict = {}
        url = "http://"+self.ip+":"+self.port+"/ZWaveAPI/Data/*"
        response = requests.post(url)
        data = response.json()
        if data != None:
            for i in data["devices"]:
                if i != "1":    #Device_1 is main controller
                    temp_dict["id"] = i
                    if "Multilevel" in data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]:
                        temp_dict["type"] = "SwitchMultilevel"
                    elif "Binary" in data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]:
                        temp_dict["type"] = "SwitchBinary"
                    dev_dict["device_"+i+""] = dict(temp_dict)
            return dict(dev_dict)

#Update the zwave light switches values.
    def dev_get(self,dev_id,dev_type):
        self.dev_id = dev_id
        self.dev_type = dev_type
        url = "http://"+self.ip+":"+self.port+"/ZWaveAPI/Run/devices["+self.dev_id+"].instances[0]."+self.dev_type+".Get()"
        #print "url %s" % (url)
        response = requests.post(url)
        data = response.json()
        return data

#Read the device level value of the zwave light switches.
    def dev_value(self,dev_id,dev_type):
        self.dev_id = dev_id
        self.dev_type = dev_type
        url = ("http://"+self.ip+":"+self.port+"/ZWaveAPI/Run/devices["+self.dev_id+"].instances[0]."+self.dev_type+".data.level.value")
        response = requests.post(url)
        value = response.json()
        #print ("value: ""\n""dev_id: "+dev_id+"\n""Value: "+str(value)+"\n")
        return str(value)

    def dev_set(self,dev_id,dev_type,dev_value):
        self.dev_id = dev_id
        self.dev_type = dev_type
        self.dev_value = dev_value
        url = ("http://"+self.ip+":"+self.port+"/ZWaveAPI/Run/devices["+self.dev_id+"].instances[0]."+self.dev_type+".Set("+self.dev_value+")")
        request = requests.post(url)
        data = request.json()
        return str(data)

