#!/usr/bin/env python
'''
Created on Feb 4, 2016

@author: popotvin
'''
import requests


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
    print url
    response = requests.post(url)
    data = response.json()
    print("Get() id: "+id+ " Value_get: "+str(data))

#Read the device level value of the zwave light switches.
def dev_data(ip,port,id,type):
    url = ("http://"+ip+":"+port+"/ZWaveAPI/Run/devices["+id+"].instances[0]."+type+".data.level.value")
    response = requests.post(url)
    value = response.json()
    #print ("value: ""\n""id: "+id+"\n""Value: "+str(value)+"\n")
    return str(value)

'''

def dev_poll(dev_dict):
    old_payload = []
    new_payload = []
    for key, value in dev_dict.iteritems():
        print ("device: "+key)
        for i,j in value.iteritems():
            if (i =="id"):
                id = j
            elif(i == "type"):
                type = j

        dev_get(id,type,ip,port)
        time.sleep(0.1)
        payload = "nodeID: " +id+ " type: " +type+ " value: "+str(devData(id,type,ip,port))
        print (payload)
        new_payload.append(payload)
        time.sleep(0.1)
    print ("new Payload: "+str(new_payload))
    print ("old Payload: "+str(old_payload))
    if old_payload != new_payload:
        mqttc.publish(topicOutgoing, str(new_payload))
    old_payload = new_payload
    newPayload = []
    time.sleep(3)

to do:Sortir le if new old payload le mettre dans  le main script et retourner un payload a la place

      
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))    
'''

    
    


       

