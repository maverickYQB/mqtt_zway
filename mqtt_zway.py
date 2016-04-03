#!/usr/bin/env python
'''
Created on Feb 4, 2016

@author: popotvin
'''
import requests, socket

#Search the connected zwave devices on the z-way REST server
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
                if "Multilevel" in data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]:
                    temp_dict["type"] = "SwitchMultilevel"
                elif "Binary" in data["devices"][""+i+""]["data"]["deviceTypeString"]["value"]:
                    temp_dict["type"] = "SwitchBinary"
                dev_dict["device_"+i+""] = dict(temp_dict)
        return dev_dict

#Update the zwave light switches values.
def dev_get(ip,port,id,type):
    url = "http://"+ip+":"+port+"/ZWaveAPI/Run/devices["+id+"].instances[0]."+type+".Get()"
    #print url
    response = requests.post(url)
    data = response.json()
    return data
#Read the device level value of the zwave light switches.
def dev_value(ip,port,id,type):
    url = ("http://"+ip+":"+port+"/ZWaveAPI/Run/devices["+id+"].instances[0]."+type+".data.level.value")
    response = requests.post(url)
    value = response.json()
    #print ("value: ""\n""id: "+id+"\n""Value: "+str(value)+"\n")
    return str(value)

#Set the device level value to the zwave light switches.
def dev_set(ip,port,id,type,value):
    url = ("http://"+ip+":"+port+"/ZWaveAPI/Run/devices["+id+"].instances[0]."+type+".Set("+value+")")
    request = requests.post(url)
    data = request.json()
    return str(data)

def server_test(ip, port):
    s = socket.socket()
    try:
        s.connect((ip, int(port)))
        return True
    except Exception as e:
        return False
    finally:
        s.close() # exeption raised [Errno 32] Broken pipe a verifier



    
    


       

